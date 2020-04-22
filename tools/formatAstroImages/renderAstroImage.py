#!/usr/bin/python3.8
# coding: utf8

from __future__ import unicode_literals

import json
import os.path
import datetime
import sys
import math
from PIL import Image, ImageDraw, ImageFont

import logging
logging.basicConfig(format="%(asctime)-15s [%(levelname)s] %(name)s.%(funcName)s: %(message)s", level=logging.INFO)

# Constantes
GLOBAL_MARGE = 10
GLOBAL_TOPINFO_HAUTEUR = 128
GLOBAL_ESPACE_TOPINFO_IMAGE = 25
GLOBAL_ESPACE_BOTTOMIMAGE_DATA = 10
GLOBAL_BOTTOMINFO_HAUTEUR = 66
GLOBAL_CADRE_IMAGE_EPAISSEUR = 1
GLOBAL_MARGE_IMAGE = 5
GLOBAL_SIGNATURE_POS_DEPUIS_BAS_IMAGE = 5
GLOBAL_SIGNATURE_POS_DEPUIS_DROITE_IMAGE = 10
GLOBAL_FONT_TITRE = "cinzel.otf"
GLOBAL_DATA_TITLE_EPHEMERIDE = "EPHEMERIDE"
GLOBAL_DATA_TITLE_HARDWARE  = "MATERIEL"
GLOBAL_DATA_TITLE_CAPTURE    = "CAPTURE"
GLOBAL_DATA_TITLE_PROCESSING = "TRAITEMENT"
GLOBAL_MONTHS = [ "JAN", "FEV", "MAR", "AVR", "MAI", "JUI", "JUL", "AOU", "SEP", "OCT", "NOV", "DEC"]
GLOBAL_MOON_FEATURE_COLOR = [(255, 127, 0), (0, 162, 222), (255, 255, 0), (0, 255, 0), (255, 0, 255), (255, 0, 0)]
GLOBAL_MOON_MINIMAP_ADJUST_LONGITUDE = 5.0
GLOBAL_MOON_MINIMAP_ADJUST_LATITUDE = 0.0
GLOBAL_MOON_MINIMAP_MARKERSIZEINPX = 6

# Values parameters:   ["label", isMandatory, [value1, value2, ...], defaultValue index, {"value1": "shortname", "value2": "shortname", ...}]
PARAM_LABEL = 0
PARAM_MANDATORY = 1
PARAM_VALUES = 2
PARAM_DEFAULT = 3
PARAM_SHORTNAMES = 4
PARAM_OUINON = [None, True, ["oui","non"], 0, None]
PARAM_IMAGETYPE = ["Type de photo", True, ["MOON","PLANET","DEEPSKY"], None, None]
PARAM_FiLENAMEJSON = ["Nom du fichier de paramètres Json", False, None, None, None]
PARAM_FiLENAMEPHOTO = ["Nom du fichier bitmap photo (... x 810 max)", True, None, None, None]
PARAM_FiLENAMEWINJUPOSMINIATURE = ["Nom du fichier bitmap Winjupos (... x 128)", True, None, None, None]
PARAM_IMAGETITLE = ["Titre", True, None, None, None]
PARAM_IMAGELOCATION = ["Lieu", True, ["Plascassier (06), France"], 0, None]
PARAM_IMAGEDATE = ["Date AAAA-MM-JJ", True, None, None, None]
PARAM_IMAGETIME = ["Heure HH:MM GMT", True, None, None, None]
PARAM_IMAGEADDITIONALCOMMENT = ["Commentaire additionnel", False, None, None, None]
PARAM_INSTRUMENT = ["Instrument", True, ["Celestron SCT 11  D.280mm F.2800mm", "EF70-300mm f/4-5.6L IS USM"], 0, {"Celestron SCT 11  D.280mm F.2800mm": "C11", "EF70-300mm f/4-5.6L IS USM": "70-300"}]
PARAM_MOUNT = ["Monture", True, ["CGEM"], 0, None]
PARAM_ADC = ["ADC", False, ["ZWO ADC"], None, {"ZWO ADC": "ADC"}]
PARAM_BARLOW = ["Barlow", False, ["Powermate x2", "Powermate x2.5"], None, {"Powermate x2": "BarlowX2", "Powermate x2.5": "BarlowX2.5"}]
PARAM_REDUCER = ["Réducteur", False, ["Celestron Reducer x0.67", "Starizona Night Owl x0.4"], None, {"Celestron Reducer x0.67": "RedX0.67", "Starizona Night Owl x0.4": "RedX0.4"}]
PARAM_FILTER = ["Filtre", False, ["IR642", "IR742", "IR807", "RG610 (rouge+IR)", "#2c (rouge)", "#25 (rouge)", "#23A (rouge)", "#21 (orange)", "#12 (jaune)", "#80A (bleu)", "IR/UV Cut", "UHC", "OIII", "Dual Band"], None, {"IR642": "IR642", "IR742": "IR742", "IR807": "IR807", "RG610 (rouge+IR)": "RG610", "#2c (rouge)": "#2c", "#25 (rouge)": "#25", "#23A (rouge)": "#23A", "#21 (orange)": "#21", "#12 (jaune)": "#12", "#80A (bleu)": "#80A", "IR/UV Cut": "IR/UVCut", "UHC": "UHC", "OIII": "OIII", "Dual Band": "DualB"}]
PARAM_CAMERA = ["Caméra", True, ["ZWO ASI120MM", "ZWO ASI224MC", "ZWO ASI178MM", "ZWO ASI533MC", "Samsung Galaxy Note 3", "Samsung Galaxy Note 9"], 3, {"ZWO ASI120MM": "ASI120MM", "ZWO ASI224MC": "ASI224MC", "ZWO ASI178MM": "ASI178MM", "ZWO ASI533MC": "ASI533MC", "Samsung Galaxy Note 3": "Note3", "Samsung Galaxy Note 9": "Note9"}]
PARAM_SOFTWARECAPTURE = ["Logiciel ... capture", True, ["Firecapture", "ASIcap", "Sharpcap", "Astro Photography Tool (APT)", "Samsung Photo"], 0, None]
PARAM_SOFTWAREPREPROCESS = ["Logiciel ... pré-traitement", False, ["PIPP"], None, None]
PARAM_SOFTWARESTACK = ["Logiciel ... empilement", False, ["Autostakkert!2", "Autostakkert!3", "Registax6", "Astrosurface", "Siril", "Deep Sky Stacker"], 3, None]
PARAM_SOFTWAREPROCESS = ["Logiciel ... traitement", False, ["Registax6", "Astrosurface", "Siril", "Deep Sky Stacker"], 1, None]
PARAM_SOFTWAREPOSTPROCESS = ["Logiciel ... post-traitement", False, ["DxO Photolab", "Photoshop", "Lightroom"], 0, None]
PARAM_CAMERABINNING = ["Réglages caméra... binning", True, ["bin x1", "bin x2", "bin x4"], 0, None]
PARAM_CAMERABITS = ["Réglages camera... bits", True, ["8 bits", "16 bits"], 0, None]
PARAM_CAMERAGAIN = ["Réglages camera... gain", True, None, None, None]
PARAM_CAMERAEXPO = ["Réglages camera... Exposition (avec unité)", True, None, None, None]
PARAM_CAMERAFPS = ["Réglages camera... FPS", True, None, None, None]
PARAM_CAMERATOTALEXPO = ["Réglages camera... Exposition totale (avec unité)", True, None, None, None]
PARAM_PROCESSSTACKFRAME = ["Processing... Stacking (nb / total)", False, None, None, None]
PARAM_PROCESSPOSTCOMMENT = ["Processing... Post-process commentaire (resize,...)", False, None, None, None]
PARAM_MOONAGE = ["Age de la lune (en jours)", True, None, None, None]
PARAM_MOONPOSANGLE = ["Position Angle de la lune (en deg)", True, None, None, None]
PARAM_MOONCOLONG = ["Colongitude de la lune (en deg)", True, None, None, None]
PARAM_MOONILLUM = ["Illumination de la lune (en %)", True, None, None, None]
PARAM_PLANET = ["Planète", True, ["Mercure","Venus","Mars","Jupiter","Saturne","Uranus","Neptune"], None, None]

# Fonts
FONT_TECHNICAL_INFO = ImageFont.truetype("PCNavita-Regular.ttf", 12)
FONT_SIGNATURE = ImageFont.truetype("Sugar Candy.ttf", 18)
FONT_TITLE = ImageFont.truetype("COPRGTL.TTF", 36)
FONT_ADDITIONAL_COMMENT = ImageFont.truetype("georgiai.ttf", 16)
FONT_SUBTITLE = ImageFont.truetype("georgiai.ttf", 20)
FONT_LUNARFEATURE_NAME = ImageFont.truetype("PCNavita-Regular.ttf", 12)
FONT_LUNARFEATURE_DATA = ImageFont.truetype("PCNavita-Regular.ttf", 12)


class Tools:
    @staticmethod
    def getRectangularCoordXYFromLunarLongLat(fLongitude, fLatitude, iBitmapSize):
        fLongitude = fLongitude - 90.0
        x = iBitmapSize / 2 + (iBitmapSize / 2 * math.cos(math.radians(fLongitude)) * math.cos(math.radians(fLatitude)))
        y = iBitmapSize / 2 - (iBitmapSize / 2 * math.sin(math.radians(fLatitude)))
        return x, y
    @staticmethod
    def getdatafromkeyboard(arrParam = None, label=None, ismandatory=None, possiblevalues=None, defaultvalue=None) -> str:
        logger = logging.getLogger("getdatafromkeyboard")
        # get parameters from arrParam if nt None, an override with other parameters
        if arrParam is not None:
            if label is None and arrParam[PARAM_LABEL] is not None: label = arrParam[PARAM_LABEL]
            if ismandatory is None and arrParam[PARAM_MANDATORY] is not None: ismandatory = arrParam[PARAM_MANDATORY]
            if possiblevalues is None and arrParam[PARAM_VALUES] is not None: possiblevalues = arrParam[PARAM_VALUES]
            if defaultvalue is None and possiblevalues is not None and arrParam[PARAM_DEFAULT] is not None: defaultvalue = possiblevalues[arrParam[PARAM_DEFAULT]]
        # init valid input
        svalidinput = None
        # format label for input with possible and default values
        sdisplaylabel = label
        if possiblevalues is not None and len(possiblevalues) > 0: sdisplaylabel += "... ({}) ".format(", ".join(possiblevalues))
        sdisplaylabel += "... "
        if defaultvalue is not None:  sdisplaylabel += " [{}]   ".format(defaultvalue)
        # read input from keyboard until a valid value is entered
        bvalidvalueentered = False
        while not bvalidvalueentered:
            keyboardinput = input(sdisplaylabel)
            # validate input against possible values
            svalidinput = keyboardinput
            if keyboardinput == "-":
                svalidinput = ""
                if not ismandatory: bvalidvalueentered = True
                logger.debug("keyboard entry is '-'' (mandatory:{}, defaultvalue:{}) => valid={}".format(str(ismandatory), "yes" if defaultvalue is not None else "No", str(bvalidvalueentered)))
            elif keyboardinput == "":
                if defaultvalue is not None:
                    svalidinput = defaultvalue
                    bvalidvalueentered = True
                    logger.debug("keyboard entry is empty (mandatory:{}, defaultvalue:{}) => valid={}".format(str(ismandatory), "yes" if defaultvalue is not None else "No", str(bvalidvalueentered)))
                else:
                    if not ismandatory: bvalidvalueentered = True
                    logger.debug("keyboard entry is empty (mandatory:{}, defaultvalue:{}) => valid={}".format(str(ismandatory), "yes" if defaultvalue is not None else "No", str(bvalidvalueentered)))
            elif possiblevalues is not None and len(possiblevalues) > 0:
                # find correspondance between keyboard input and possible values
                lowerkeyboardvalue = keyboardinput.lower()
                nbcorresp = 0
                logger.debug("check against possible values...")
                iter = 0
                nbcorresp = 0
                itervalid = -1
                while iter < len(possiblevalues):
                    if possiblevalues[iter].lower().find(lowerkeyboardvalue) > -1:
                        nbcorresp += 1
                        itervalid = iter
                        logger.debug("   --> {}, nbcorresp={}".format(possiblevalues[iter], str(nbcorresp)))
                    else:
                        logger.debug("       {}, nbcorresp={}".format(possiblevalues[iter], str(nbcorresp)))
                    iter += 1
                if nbcorresp == 1:
                    svalidinput = possiblevalues[itervalid]
                    bvalidvalueentered = True
                    logger.debug("       valid!!")
            else:
                logger.debug("       valid!!")
                bvalidvalueentered = True
        # display value
        print("     --> {}".format(svalidinput))
        # return input
        return svalidinput


class ParameterInput:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("")

    def getData(self, arrParam = None, label = None, ismandatory=None, possiblevalues=None, defaultvalue=None):
        return Tools.getdatafromkeyboard(arrParam, label, ismandatory, possiblevalues, defaultvalue)

    # basic fields
    def getimagetype(self): return self.getData(arrParam=PARAM_IMAGETYPE)
    def getfilenamejson(self): return self.getData(arrParam=PARAM_FiLENAMEJSON)
    def getyesno(self, sLabel): return self.getData(arrParam=PARAM_IMAGETYPE, label=sLabel)
    # Common fields
    def getfilenamepicture(self): return self.getData(arrParam=PARAM_FiLENAMEPHOTO)
    def getfilenamewinjuposminiature(self): return self.getData(arrParam=PARAM_FiLENAMEWINJUPOSMINIATURE)
    def getimagetitle(self): return self.getData(arrParam=PARAM_IMAGETITLE)
    def getimagelocation(self): return self.getData(arrParam=PARAM_IMAGELOCATION)
    def getimagetime(self): return self.getData(arrParam=PARAM_IMAGETIME)
    def getimagedate(self): return self.getData(arrParam=PARAM_IMAGEDATE)
    def getimageadditionalcomment(self): return self.getData(arrParam=PARAM_IMAGEADDITIONALCOMMENT)
    def getmaterialinstrument(self): return self.getData(PARAM_INSTRUMENT)
    def getmaterialmount(self): return self.getData(PARAM_MOUNT)
    def getmaterialadc(self): return self.getData(PARAM_ADC)
    def getmaterialbarlow(self): return self.getData(PARAM_BARLOW)
    def getmaterialreducer(self): return self.getData(PARAM_REDUCER)
    def getmaterialfilter(self): return self.getData(PARAM_FILTER)
    def getmaterialcamera(self): return self.getData(PARAM_CAMERA)
    def getsoftwarecapture(self): return self.getData(PARAM_SOFTWARECAPTURE)
    def getsoftwarepreprocessing(self): return self.getData(PARAM_SOFTWAREPREPROCESS)
    def getsoftwarestacking(self): return self.getData(PARAM_SOFTWARESTACK)
    def getsoftwareprocessing(self): return self.getData(PARAM_SOFTWAREPROCESS)
    def getsoftwarepostprocessing(self): return self.getData(PARAM_SOFTWAREPOSTPROCESS)
    def getcamerasettingbinning(self): return self.getData(PARAM_CAMERABINNING)
    def getcamerasettingbits(self): return self.getData(PARAM_CAMERABITS)
    def getcamerasettinggain(self): return self.getData(PARAM_CAMERAGAIN)
    def getcamerasettingexpo(self): return self.getData(PARAM_CAMERAEXPO)
    def getcamerasettingfps(self): return self.getData(PARAM_CAMERAFPS)
    def getcamerasettingtotalexpo(self): return self.getData(PARAM_CAMERATOTALEXPO)
    def getprocessstackframe(self): return self.getData(PARAM_PROCESSSTACKFRAME)
    def getprocesspostcomment(self): return self.getData(PARAM_PROCESSPOSTCOMMENT)
    # Moon specific fields
    def getmoonposangleindeg(self): return self.getData(PARAM_MOONPOSANGLE)
    def getmooncolongindeg(self): return self.getData(PARAM_MOONCOLONG)
    def getmoonilluminpct(self): return self.getData(PARAM_MOONILLUM)
    def getmoonageindays(self): return self.getData(PARAM_MOONAGE)
    # Planet specific fields
    def getplanetname(self): return self.getData(PARAM_PLANET)


class ImageData:
    def __init__(self, sJsonFilename = None):
        self._logger = logging.getLogger("ImageData")
        self._JsonFilename = sJsonFilename
        if self._JsonFilename is not None:
            print("Init from Json file   {}".format(self._JsonFilename))
            # read parameters
            with open(sJsonFilename, 'r') as fp:
                self._dicParameters = json.load(fp)
        else:
            self._dicParameters = {}
    def isFromJsonFile(self): return (self._JsonFilename is not None)
    def setValue(self, sKey, sValue):
        self._dicParameters[sKey] = sValue
    def getValue(self, sKey):
        if sKey in self._dicParameters:
            return self._dicParameters[sKey]
        else:
            return ""

    def inputdatafiles(self):
        theparam = ParameterInput()
        self.setValue("imagefilenamepicture", theparam.getfilenamepicture())

    def inputdatacommon(self):
        theparam = ParameterInput()
        self.setValue("imagetitle", theparam.getimagetitle())
        self.setValue("imagelocation", theparam.getimagelocation())
        self.setValue("imagedate", theparam.getimagedate())
        self.setValue("imagetime", theparam.getimagetime())
        self.setValue("imageadditionalcomment", theparam.getimageadditionalcomment())

    def inputdatamaterial(self):
        theparam = ParameterInput()
        self.setValue("materialinstrument", theparam.getmaterialinstrument())
        self.setValue("materialmount", theparam.getmaterialmount())
        self.setValue("materialadc", theparam.getmaterialadc())
        self.setValue("materialbarlow", theparam.getmaterialbarlow())
        self.setValue("materialreducer", theparam.getmaterialreducer())
        self.setValue("materialfilter", theparam.getmaterialfilter())
        self.setValue("materialcamera", theparam.getmaterialcamera())

    def inputdatasoftware(self):
        theparam = ParameterInput()
        self.setValue("softwarecapture", theparam.getsoftwarecapture())
        self.setValue("softwarepreprocessing", theparam.getsoftwarepreprocessing())
        self.setValue("softwarestacking", theparam.getsoftwarestacking())
        self.setValue("processstackframe", theparam.getprocessstackframe())
        self.setValue("softwareprocessing", theparam.getsoftwareprocessing())
        self.setValue("softwarepostprocessing", theparam.getsoftwarepostprocessing())
        self.setValue("processpostcomment", theparam.getprocesspostcomment())

    def inputdatacamerasettings(self):
        theparam = ParameterInput()
        self.setValue("camerasettingbinning", theparam.getcamerasettingbinning())
        self.setValue("camerasettingbits", theparam.getcamerasettingbits())
        self.setValue("camerasettinggain", theparam.getcamerasettinggain())
        self.setValue("camerasettingexpo", theparam.getcamerasettingexpo())
        self.setValue("camerasettingfps", theparam.getcamerasettingfps())
        self.setValue("camerasettingtotalexpo", theparam.getcamerasettingtotalexpo())

    def getOutputFilename(self):
        # Compute output file name
        sOutputFileName = self.getValue("imagetype") + " - " + self.getValue("imagedate").replace("-", "") + self.getValue("imagetime").replace(":", "")
        sOutputFileName += " - ["
        sOutputFileName += PARAM_INSTRUMENT[PARAM_SHORTNAMES][self.getValue("materialinstrument")]
        sOutputFileName += "-" + PARAM_CAMERA[PARAM_SHORTNAMES][self.getValue("materialcamera")]
        if self.getValue("materialadc") != "": sOutputFileName += "-" + PARAM_ADC[PARAM_SHORTNAMES][self.getValue("materialadc")]
        if self.getValue("materialbarlow") != "": sOutputFileName += "-" + PARAM_BARLOW[PARAM_SHORTNAMES][self.getValue("materialbarlow")]
        if self.getValue("materialreducer") != "": sOutputFileName += "-" + PARAM_REDUCER[PARAM_SHORTNAMES][self.getValue("materialreducer")]
        if self.getValue("materialfilter") != "": sOutputFileName += "-" + PARAM_FILTER[PARAM_SHORTNAMES][self.getValue("materialfilter")]
        sOutputFileName +=  "]"
        sOutputFileName +=  " - " + self.getValue("imagetitle")
        return sOutputFileName

    def getEphemerideData(self):
        ephemerideData = self.getValue("imagedate")[-2:] + " " + GLOBAL_MONTHS[int(self.getValue("imagedate")[5:7]) - 1] + " " + self.getValue("imagedate")[:4]
        ephemerideData += "  " + self.getValue("imagetime") + " GMT"
        ephemerideData += " - " + self.getValue("imagelocation")
        return ephemerideData

    def getHardwareData(self):
        hardwareData = self.getValue("materialinstrument")
        hardwareData += " - " + self.getValue("materialmount")
        if self.getValue("materialadc") != "": hardwareData += " - " + self.getValue("materialadc")
        if self.getValue("materialbarlow") != "": hardwareData += " - " + self.getValue("materialbarlow")
        if self.getValue("materialreducer") != "": hardwareData += " - " + self.getValue("materialreducer")
        if self.getValue("materialfilter") != "": hardwareData += " - Filtre " + self.getValue("materialfilter")
        hardwareData += " - Camera " + self.getValue("materialcamera")
        return hardwareData

    def getCaptureData(self):
        captureData = self.getValue("softwarecapture")
        captureData += " - " + self.getValue("camerasettingbinning")
        captureData += " / " + self.getValue("camerasettingbits")
        if self.getValue("camerasettinggain") != "": captureData += " / Gain " + self.getValue("camerasettinggain")
        if self.getValue("camerasettingexpo") != "": captureData += " / Exp. " + self.getValue("camerasettingexpo")
        if self.getValue("camerasettingfps") != "": captureData += " / " + self.getValue("camerasettingfps") + " FPS"
        if self.getValue("camerasettingtotalexpo") != "": captureData += " / Total Exp. " + self.getValue("camerasettingtotalexpo")
        return captureData

    def getProcessingData(self):
        processingData = ""
        if self.getValue("softwarepreprocessing") != "": processingData += self.getValue("softwarepreprocessing")
        if self.getValue("softwarestacking") != "": processingData += (" - " + self.getValue("softwarestacking")) if processingData != "" else self.getValue("softwarestacking")
        if self.getValue("processstackframe") != "" and self.getValue("softwarestacking") != "": processingData += (" (" + self.getValue("processstackframe")) + ")"
        if self.getValue("softwareprocessing") != "": processingData += (" - " + self.getValue("softwareprocessing")) if processingData != "" else self.getValue("softwareprocessing")
        if self.getValue("softwarepostprocessing") != "": processingData += (" - " + self.getValue("softwarepostprocessing")) if processingData != "" else self.getValue("softwarepostprocessing")
        if self.getValue("processpostcomment") != "": processingData += (" - " + self.getValue("processpostcomment")) if processingData != "" else self.getValue("processpostcomment")
        return processingData

    def saveDataToJson(self):
        sOutputFileName = self.getOutputFilename()
        # Save parameters in JSON file if not a json file in input
        with open(sOutputFileName + '.json', 'w') as fp:
            try:
                json.dump(self._dicParameters, fp)
                print(" --> fichier  {}.json  créé.".format(sOutputFileName))
            except:
                print(" --> ERREUR !!! fichier Json  {}.json   non créé !!".format(sOutputFileName))


class ImageDataMoon(ImageData):
    def __init__(self, sJsonFilename = None):
        self._logger = logging.getLogger(self.__class__.__name__)
        super().__init__(sJsonFilename)
        self.setValue("imagetype", "MOON")

    def initdata(self):
        # get generic info & moon specific infos
        if not self.isFromJsonFile():
            theparam = ParameterInput()
            super().inputdatafiles()
            self.setValue("filenameminiature", theparam.getfilenamewinjuposminiature())
            super().inputdatacommon()
            self.setValue("moonageindays", theparam.getmoonageindays())  # get specific lunar info
            self.setValue("moonilluminpct", theparam.getmoonilluminpct())  # get specific lunar info
            self.setValue("mooncolongindeg", theparam.getmooncolongindeg())  # get specific lunar info
            self.setValue("moonposangleindeg", theparam.getmoonposangleindeg())  # get specific lunar info
            super().inputdatamaterial()
            super().inputdatasoftware()
            super().inputdatacamerasettings()
            self.inputLunarFeatureData()
            super().saveDataToJson()

    def getEphemerideData(self):
        ephemerideData = super().getEphemerideData()
        if self.getValue("moonageindays") != "": ephemerideData += " - Lune age: " + self.getValue("moonageindays") + "j"
        if self.getValue("moonilluminpct") != "": ephemerideData += " - Illum " + self.getValue("moonilluminpct") + "%"
        if self.getValue("mooncolongindeg") != "": ephemerideData += " - Colong " + self.getValue("mooncolongindeg") + "°"
        if self.getValue("moonposangleindeg") != "": ephemerideData += " - Pos Angle " + self.getValue("moonposangleindeg") + "°"
        return ephemerideData

    def inputLunarFeatureData(self):
        # Read Lunar Features
        with open("FormatAstroImages_LunarFeatures.json", 'r') as fp:
            dicLunarFeatures = json.load(fp)

        # read lunar features
        arrLunarFeature = []
        bContinue = True
        iFeatureId = 1
        while (bContinue and iFeatureId < 7):
            sLunarFeatueName = Tools.getdatafromkeyboard(None, label="Formation Lunaire... nom:", ismandatory=False, possiblevalues=None, defaultvalue=None)
            if sLunarFeatueName != "":
                if sLunarFeatueName.upper() in dicLunarFeatures:
                    sDefaultLongitude = None
                    sDefaultLatitude = None
                    sDefaultHeight = None
                    sDefaultWidth = None
                    sDefaultLength = None
                    sDefaultDepth = None
                    sDefaultDiameter = None
                    if dicLunarFeatures[sLunarFeatueName.upper()]["LongitudeInDeg"] is not None: sDefaultLongitude = str(dicLunarFeatures[sLunarFeatueName.upper()]["LongitudeInDeg"])
                    if dicLunarFeatures[sLunarFeatueName.upper()]["LatitudeInDeg"] is not None: sDefaultLatitude = str(dicLunarFeatures[sLunarFeatueName.upper()]["LatitudeInDeg"])
                    if dicLunarFeatures[sLunarFeatueName.upper()]["LengthInKm"] is not None: sDefaultLength = str(dicLunarFeatures[sLunarFeatueName.upper()]["LengthInKm"])
                    if dicLunarFeatures[sLunarFeatueName.upper()]["WidthInKm"] is not None: sDefaultWidth = str(dicLunarFeatures[sLunarFeatueName.upper()]["WidthInKm"])
                    if dicLunarFeatures[sLunarFeatueName.upper()]["HeightInM"] is not None: sDefaultHeight = str(dicLunarFeatures[sLunarFeatueName.upper()]["HeightInM"])
                    sDefaultLunarFeatureValues = "          Formation Lunaire '{}' ... ".format(sLunarFeatueName.upper())
                    if sDefaultLongitude is not None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Longitude: {}".format(str(sDefaultLongitude))
                    if sDefaultLatitude is not None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Latitude: {}".format(str(sDefaultLatitude))
                    if sDefaultLength is not None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Largeur: {} km".format(str(sDefaultLength))
                    if sDefaultWidth is not None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Longueur: {} km".format(str(sDefaultWidth))
                    if sDefaultHeight is not None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Hauteur: {} m".format( str(sDefaultHeight))
                    print (sDefaultLunarFeatureValues)

                    if not sDefaultWidth is None and sDefaultLength is not None:
                        if sDefaultLength != 0.0:
                            if float(sDefaultWidth) / float(sDefaultLength) > 0.9:
                                sDefaultDiameter = sDefaultWidth
                                if sDefaultHeight is not None: sDefaultDepth = sDefaultHeight
                                sDefaultWidth = None
                                sDefaultLength = None
                                sDefaultHeight = None
                    if sDefaultDiameter is not None: sDefaultDiameter = sDefaultDiameter + " km"
                    if sDefaultWidth is not None: sDefaultWidth = sDefaultWidth + " km"
                    if sDefaultLength is not None: sDefaultLength = sDefaultLength + " km"
                    if sDefaultHeight is not None: sDefaultHeight = sDefaultHeight + " m"
                    if sDefaultDepth is not None:sDefaultDepth = sDefaultDepth + " m"
                else:
                    sDefaultLongitude = ""
                    sDefaultLatitude = ""
                    sDefaultHeight = ""
                    sDefaultWidth = ""
                    sDefaultLength = ""
                    sDefaultDepth = ""
                    sDefaultDiameter = ""

                self.setValue("LunarFeatureName_{}".format(str(iFeatureId)), sLunarFeatueName)
                self.setValue("LunarFeatureLongitude_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     longitude:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultLongitude))
                self.setValue("LunarFeatureLatitude_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     latitude:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultLatitude))
                self.setValue("LunarFeatureDiameter_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     diamètre:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultDiameter))
                self.setValue("LunarFeatureWidth_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     Largeur:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultWidth))
                self.setValue("LunarFeatureLength_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     Longueur:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultLength))
                self.setValue("LunarFeatureDepth_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     Profondeur:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultDepth))
                self.setValue("LunarFeatureHeight_{}".format(str(iFeatureId)), Tools.getdatafromkeyboard(None, label="                     Hauteur:", ismandatory=False, possiblevalues=None, defaultvalue=sDefaultHeight))
            else:
                bContinue = False
            iFeatureId += 1

        self.setValue("imagesubtitle_0", self.getValue("LunarFeatureName_1"))
        if self.getValue("LunarFeatureName_2") != "": self.setValue("imagesubtitle_0", (self.getValue("imagesubtitle_0") + " - " + self.getValue("LunarFeatureName_2")))
        if self.getValue("LunarFeatureName_3") != "": self.setValue("imagesubtitle_0", (self.getValue("imagesubtitle_0") + " - " + self.getValue("LunarFeatureName_3")))
        if self.getValue("LunarFeatureName_4") != "": self.setValue("imagesubtitle_1", self.getValue("LunarFeatureName_4"))
        if self.getValue("LunarFeatureName_5") != "": self.setValue("imagesubtitle_1", (self.getValue("imagesubtitle_1") + " - " + self.getValue("LunarFeatureName_5")))
        if self.getValue("LunarFeatureName_6") != "": self.setValue("imagesubtitle_1", (self.getValue("imagesubtitle_1") + " - " + self.getValue("LunarFeatureName_6")))

    def getOutputFilename(self):
        sOutputFilename = super().getOutputFilename()
        for iRow in range(1, 4):
            for iCol in range(1, 3):
                iFeatureId = (iCol - 1) * 3 + iRow
                if self.getValue("LunarFeatureName_{}".format(str(iFeatureId))) != "":
                    sOutputFilename += " - {}".format(self.getValue("LunarFeatureName_{}".format(str(iFeatureId))))
        return sOutputFilename


class ImageDataPlanet(ImageData):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("")
        super().__init__()

    def getplanetname(self): return self._planetname

    def initdata(self):
        # get generic info
        super().initdata()
        # get specific lunar info
        theparam = ParameterInput()
        self._planetname = theparam.getplanetname()


class ImageDataDeepsky(ImageData):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("")
        super().__init__()


class ImageRegion:
    def __init__(self, posStartX, posEndX, posStartY, posEndY):
        self._height = 0
        self._width = 0
        self._posStartX = posStartX
        self.setEndPosX(posEndX)
        self._posStartY = posStartY
        self.setEndPosY(posEndY)
    def getStartPosX(self): return self._posStartX
    def getStartPosY(self): return self._posStartY
    def getEndPosX(self): return self._posEndX
    def getEndPosY(self): return self._posEndY
    def getHeight(self): return self._height
    def getWidth(self): return self._width
    def setStartPosX(self, iPos):
        self._posStartX = iPos
        self._posEndX =  self._posStartX + self._width - 1
    def setStartPosY(self, iPos):
        self._posStartY = iPos
        self._posEndY = self._posStartY + self._height - 1
    def setEndPosX(self, iPos):
        self._posEndX = iPos
        self._width = iPos - self._posStartX + 1
    def setEndPosY(self, iPos):
        self._posEndY = iPos
        self._height = iPos - self._posStartY + 1
    def setHeight(self, iValue):
        self._height = iValue
        self._posEndY = self._posStartY + self._height - 1
    def setWidth(self, iValue):
        self._width = iValue
        self._posEndX = self._posStartX + self._width - 1
    def moveTo(self, posX, posY):
        self.setStartPosX(posX)
        self.setStartPosY(posY)


class ImageRenderer:
    def __init__(self, theImageData):
        self._logger = logging.getLogger("ImageRenderer")
        self._logger.debug("")
        self._imagedata = theImageData
        self._imgPhotoFilename = theImageData.getValue("imagefilenamepicture")
        self._imgPhoto = None
        self._imgPhotoWidth = None
        self._imgPhotoHeight = None
        self._imgPhotoMiniature = None
        self._imgPhotoMiniatureWidth = None
        self._imgPhotoMiniatureHeight = None
        self._regionPhotoMiniature = None
        self._imgWinjuposMiniature = None
        self._imgWinjuposMiniatureWidth = None
        self._imgWinjuposMiniatureHeight = None
        self._regionPhoto = None
        self._regionPhotoWithBorder = None
        self._regionSignature = None
        self._regionTitle = None
        self._regionAdditionalComment = None
        self._regionWinjuposMiniature = None
        self._pilFinalImageDraw = None
        self._pilFinalImageImg = None
        self._finalImageWidth = 0
        self._finalImageHeight = 0
        self._topInfoLeftMargin = 0
        self._topInfoWidth = 0
        # load photo and initialize bitmap for final image
        self._imgPhoto, self._imgPhotoWidth, self._imgPhotoHeight = self._loadimage("Photo", self._imgPhotoFilename)
        self._createFinalImage()
    def getPilFinalImageDraw(self): return self._pilFinalImageDraw
    def setPilFinalImageDraw(self, oPilDraw): self._pilFinalImageDraw = oPilDraw
    def getPilFinalImageImg(self): return self._pilFinalImageImg
    def setPilFinalImageImg(self, oPilImg): self._pilFinalImageImg = oPilImg
    def getFinalImageWidth(self): return self._finalImageWidth
    def getFinalImageHeight(self): return self._finalImageHeight
    def getImgPhotoFilename(self): return self._imgPhotoFilename
    def getImgPhoto(self): return self._imgPhoto
    def getImgPhotoWidth(self): return self._imgPhotoWidth
    def getImgPhotoHeight(self): return self._imgPhotoHeight
    def getImgWinjuposMiniature(self): return self._imgWinjuposMiniature
    def getImgWinjuposMiniatureWidth(self): return self._imgWinjuposMiniatureWidth
    def getImgWinjuposMiniatureHeight(self): return self._imgWinjuposMiniatureHeight
    def setImgPhoto(self, oImgPhoto): self._imgPhoto = oImgPhoto
    def getRegionPhoto(self): return self._regionPhoto
    def getRegionWinjuposMiniature(self): return self._regionWinjuposMiniature
    def getRegionPhotoWithBorder(self): return self._regionPhotoWithBorder
    def getRegionSignature(self): return self._regionSignature
    def getRegionTitle(self): return self._regionTitle
    def getRegionAdditionalComment(self): return self._regionAdditionalComment

    def getdata(self): return   self._imagedata

    def _loadimage(self, sLabel, sFilename):
        oImg = Image.open(sFilename)
        iWidth, iHeight = oImg.size
        print("   --> {} size: {} x {}".format(sLabel, str(iWidth), str(iHeight)))
        return oImg, iWidth, iHeight

    def _createFinalImage(self):
        # create final image
        self._finalImageWidth = GLOBAL_MARGE + GLOBAL_CADRE_IMAGE_EPAISSEUR + GLOBAL_MARGE_IMAGE + self._imgPhotoWidth + GLOBAL_MARGE_IMAGE + GLOBAL_CADRE_IMAGE_EPAISSEUR + GLOBAL_MARGE
        self._finalImageHeight = GLOBAL_MARGE + GLOBAL_TOPINFO_HAUTEUR + GLOBAL_ESPACE_TOPINFO_IMAGE + GLOBAL_CADRE_IMAGE_EPAISSEUR + GLOBAL_MARGE_IMAGE + self._imgPhotoHeight + GLOBAL_MARGE_IMAGE + GLOBAL_CADRE_IMAGE_EPAISSEUR + GLOBAL_ESPACE_BOTTOMIMAGE_DATA + GLOBAL_BOTTOMINFO_HAUTEUR + GLOBAL_MARGE
        self._pilFinalImageImg = Image.new('RGBA', (self._finalImageWidth, self._finalImageHeight), (0, 0, 0, 255))
        self._pilFinalImageDraw = ImageDraw.Draw(self._pilFinalImageImg)

    def renderTechnicalInfo(self, sTitle, sInfo, iRow):
        iDataRowHeight = self._pilFinalImageDraw.textsize(sTitle, font=FONT_TECHNICAL_INFO)[1]
        iTitleWidth = 65#self._pilFinalImageDraw.textsize(sTitle, font=FONT_TECHNICAL_INFO)[0]
        # Position
        iStartPositionX = GLOBAL_MARGE
        iStartPositionY = self._regionPhotoWithBorder.getEndPosY() + 10 + (iRow - 1) * (iDataRowHeight + 3)
        # draw text
        self._pilFinalImageDraw.text((iStartPositionX, iStartPositionY), sTitle, (176,176,176), font=FONT_TECHNICAL_INFO)
        self._pilFinalImageDraw.text((iStartPositionX + iTitleWidth + 15, iStartPositionY), sInfo, (96,96,96), font=FONT_TECHNICAL_INFO)

    def renderPhotoAndSignature(self):
        # Compute position photo on final image
        self._regionPhoto = ImageRegion(0, self._imgPhotoWidth, 0, self._imgPhotoHeight)
        self._regionPhoto.moveTo(GLOBAL_MARGE + GLOBAL_CADRE_IMAGE_EPAISSEUR + GLOBAL_MARGE_IMAGE + 1, GLOBAL_MARGE + GLOBAL_TOPINFO_HAUTEUR + GLOBAL_ESPACE_TOPINFO_IMAGE + GLOBAL_CADRE_IMAGE_EPAISSEUR + GLOBAL_MARGE_IMAGE + 1)
        # draw border around photo
        self._regionPhotoWithBorder = ImageRegion(0, self._regionPhoto.getWidth() + 2*GLOBAL_MARGE_IMAGE, 0, self._regionPhoto.getHeight() + 2*GLOBAL_MARGE_IMAGE)
        self._regionPhotoWithBorder.moveTo(self._regionPhoto.getStartPosX() - GLOBAL_MARGE_IMAGE - 1, self._regionPhoto.getStartPosY() - GLOBAL_MARGE_IMAGE - 1)
        self._pilFinalImageDraw.rectangle((self._regionPhotoWithBorder.getStartPosX(), self._regionPhotoWithBorder.getStartPosY(), self._regionPhotoWithBorder.getEndPosX(), self._regionPhotoWithBorder.getEndPosY()), outline=(255, 255, 255))
        # position signature
        sField_Signature = "PhilippeLarosa"
        theColorSignature = (228, 228, 228, 255)
        theColorSignatureShadow = (32, 32, 32)
        self._regionSignature = ImageRegion(0, self._pilFinalImageDraw.textsize(sField_Signature, font=FONT_SIGNATURE)[0], 0, self._pilFinalImageDraw.textsize(sField_Signature, font=FONT_SIGNATURE)[1])
        self._regionSignature.moveTo(self._regionPhotoWithBorder.getEndPosX() - self._regionSignature.getWidth() - GLOBAL_MARGE, self._regionPhotoWithBorder.getEndPosY() - self._regionSignature.getHeight() / 3)
        # Draw black rectangle to erase border at signature position
        self._pilFinalImageDraw.rectangle((self._regionSignature.getStartPosX() - 10, self._regionSignature.getStartPosY(), self._regionSignature.getEndPosX(), self._regionSignature.getEndPosY()), outline=(0, 0, 0), fill=(0, 0, 0))
        # Display photo
        self._pilFinalImageImg.paste(self._imgPhoto, (self._regionPhoto.getStartPosX(), self._regionPhoto.getStartPosY()))
        # Display Signature with shadow
        self._pilFinalImageDraw.text((self._regionSignature.getStartPosX(), self._regionSignature.getStartPosY()), sField_Signature, theColorSignatureShadow, font=FONT_SIGNATURE)
        self._pilFinalImageDraw.text((self._regionSignature.getStartPosX() - 1, self._regionSignature.getStartPosY() - 1), sField_Signature, theColorSignatureShadow, font=FONT_SIGNATURE)
        self._pilFinalImageDraw.text((self._regionSignature.getStartPosX() - 2, self._regionSignature.getStartPosY() - 2), sField_Signature, theColorSignature, font=FONT_SIGNATURE)

    def renderWinjuposMiniature(self):
        # # Read miniature image
        self._imgWinjuposMiniature, self._imgWinjuposMiniatureWidth, self._imgWinjuposMiniatureHeight = self._loadimage("Winjupos miniature", self._imagedata.getValue("filenameminiature"))
        if self._imgWinjuposMiniatureHeight != GLOBAL_TOPINFO_HAUTEUR:
            # Resize to GLOBAL_TOPINFO_HAUTEUR pixel height maxi
            fCoeff = float(GLOBAL_TOPINFO_HAUTEUR) / float(self._imgWinjuposMiniatureHeight)
            self._regionWinjuposMiniature = ImageRegion(0, int(float(self._imgWinjuposMiniatureWidth) * fCoeff), 0, int(float(self._imgWinjuposMiniatureHeight) * fCoeff))
            self._imgWinjuposMiniature.thumbnail((self._regionWinjuposMiniature.getWidth(), self._regionWinjuposMiniature.getHeight()), Image.ANTIALIAS)
            print("   --> Winjupos miniature resized to: {} x {}".format(str(self._regionWinjuposMiniature.getWidth()), str(self._regionWinjuposMiniature.getHeight())))
        else:
            self._regionWinjuposMiniature = ImageRegion(0, 128, 0, 128)
        # position winjupos miniature on final image
        self._regionWinjuposMiniature.moveTo(GLOBAL_MARGE, GLOBAL_MARGE)
        self._pilFinalImageImg.paste(self._imgWinjuposMiniature, (self._regionWinjuposMiniature.getStartPosX(), self._regionWinjuposMiniature.getStartPosY()))

    def renderTitle(self):
        # position title on final image
        self._regionTitle = ImageRegion(0, self._pilFinalImageDraw.textsize(self._imagedata.getValue("imagetitle"), font=FONT_TITLE)[0], 0, self._pilFinalImageDraw.textsize(self._imagedata.getValue("imagetitle"), font=FONT_TITLE)[1])
        self._topInfoWidth = self.getFinalImageWidth() - GLOBAL_MARGE * 2
        self._topInfoLeftMargin = GLOBAL_MARGE
        if self._imgPhotoMiniature is not None:
            self._topInfoWidth -= (self._regionPhotoMiniature.getWidth() + GLOBAL_MARGE)
            if self._imgWinjuposMiniature is not None:
                self._topInfoWidth -= (self._regionWinjuposMiniature.getWidth() + GLOBAL_MARGE)
                self._topInfoLeftMargin = self._regionWinjuposMiniature.getEndPosX() + GLOBAL_MARGE
        iPositionX = self._topInfoLeftMargin + self._topInfoWidth / 2 - self._regionTitle.getWidth() / 2
        self._regionTitle.moveTo(self._regionWinjuposMiniature.getEndPosX() + GLOBAL_MARGE, GLOBAL_MARGE) # (iPositionX, GLOBAL_MARGE)
        self._pilFinalImageDraw.text((self._regionTitle.getStartPosX(), self._regionTitle.getStartPosY()), self._imagedata.getValue("imagetitle"), (255, 255, 255), font=FONT_TITLE)

    def renderAdditionalComment(self):
        if self._imagedata.getValue("imageadditionalcomment") != "":
            self._regionAdditionalComment = ImageRegion(0, self._pilFinalImageDraw.textsize(self._imagedata.getValue("imageadditionalcomment"), font=FONT_ADDITIONAL_COMMENT)[0], 0, self._pilFinalImageDraw.textsize(self._imagedata.getValue("imageadditionalcomment"), font=FONT_ADDITIONAL_COMMENT)[1])
            self._regionAdditionalComment.moveTo(self._regionWinjuposMiniature.getEndPosX() + GLOBAL_MARGE*2 , \
                                                 self._regionPhotoWithBorder.getStartPosY() - 7 - self._regionAdditionalComment.getHeight())
            self._pilFinalImageDraw.text((self._regionAdditionalComment.getStartPosX(), self._regionAdditionalComment.getStartPosY()), self._imagedata.getValue("imageadditionalcomment"), (127,127,127), font=FONT_ADDITIONAL_COMMENT)

    def renderSubTitles(self):
        for i in range(0,3):
            sSubtitle = self._imagedata.getValue("imagesubtitle_{}".format(str(i)))
            if sSubtitle != "":
                iRowHeight = self._pilFinalImageDraw.textsize(sSubtitle, font=FONT_SUBTITLE)[1]
                self._pilFinalImageDraw.text(
                    (self._regionWinjuposMiniature.getEndPosX() + GLOBAL_MARGE*2, self._regionTitle.getEndPosY() + 10 + i*(iRowHeight + 7)), sSubtitle, (127, 127, 127), font=FONT_SUBTITLE)

    def render(self):
        self._logger.debug("")
        # position photo on final image
        self.renderPhotoAndSignature()

        # position title on final image
        self.renderTitle()

        # position title on final image
        self.renderSubTitles()

        # position additional comment
        self.renderAdditionalComment()

        # position data Rows
        theFinalDraw = self.renderTechnicalInfo(GLOBAL_DATA_TITLE_EPHEMERIDE, self._imagedata.getEphemerideData(), 1)
        theFinalDraw = self.renderTechnicalInfo(GLOBAL_DATA_TITLE_HARDWARE, self._imagedata.getHardwareData(), 2)
        theFinalDraw = self.renderTechnicalInfo(GLOBAL_DATA_TITLE_CAPTURE, self._imagedata.getCaptureData(), 3)
        theFinalDraw = self.renderTechnicalInfo(GLOBAL_DATA_TITLE_PROCESSING, self._imagedata.getProcessingData(), 4)


class ImageRenderMoon(ImageRenderer):
    def __init__(self, theImageData):
        super().__init__(theImageData)
        self._regionPhotoMiniature = None

    def addLocationMarkerOnWinjuposImage(self, iFeatureId):
        # read parameters
        iMoonPositionAngle = float(self._imagedata.getValue("moonposangleindeg"))
        fMoonFeatureLongitude = float(self._imagedata.getValue("LunarFeatureLongitude_{}".format(str(iFeatureId)))) + GLOBAL_MOON_MINIMAP_ADJUST_LONGITUDE
        fMoonFeatureLatitude = float(self._imagedata.getValue("LunarFeatureLatitude_{}".format(str(iFeatureId)))) + GLOBAL_MOON_MINIMAP_ADJUST_LATITUDE
        # Compute position of the feature in the image
        # Draw a tupColor dot of size iMarkerSizeInPx at the position of the feature
        imgNewWinjupos = Image.new('RGBA', (GLOBAL_TOPINFO_HAUTEUR, GLOBAL_TOPINFO_HAUTEUR), (255, 255, 255, 0))  # create a new black image
        iPosX, iPosY = Tools.getRectangularCoordXYFromLunarLongLat(fMoonFeatureLongitude, fMoonFeatureLatitude, GLOBAL_TOPINFO_HAUTEUR)
        drawWinjuposMinimap = ImageDraw.Draw(imgNewWinjupos)
        drawWinjuposMinimap.ellipse((iPosX - int(GLOBAL_MOON_MINIMAP_MARKERSIZEINPX / 2), iPosY - int(GLOBAL_MOON_MINIMAP_MARKERSIZEINPX / 2),
                                     iPosX + int(GLOBAL_MOON_MINIMAP_MARKERSIZEINPX / 2), iPosY + int(GLOBAL_MOON_MINIMAP_MARKERSIZEINPX / 2)),
                                    fill=GLOBAL_MOON_FEATURE_COLOR[iFeatureId - 1], outline=GLOBAL_MOON_FEATURE_COLOR[iFeatureId - 1])
        # Rotate minimap by PositionAngle of the Moon
        imgNewWinjupos = imgNewWinjupos.rotate(iMoonPositionAngle, Image.BILINEAR)  # Image.NEAREST, Image.BICUBIC, Image.BILINEAR
        # merge moon minimap with original bitmap
        self._pilFinalImageImg.paste(imgNewWinjupos, (self._regionWinjuposMiniature.getStartPosX(), self._regionWinjuposMiniature.getStartPosY()), imgNewWinjupos)

    def renderLunarFeaturesInfo(self):
        colorBoxSize = 4
        iNbFeatures = 0
        iMaxFeatureInfoWidth = 0
        arrFeatureInfos = []
        for iFeatureId in range(1, 7):
            if self._imagedata.getValue("LunarFeatureName_{}".format(str(iFeatureId))) != "":
                sFeatureName = self._imagedata.getValue("LunarFeatureName_{}".format(str(iFeatureId)))
                sDataLunarFeature = ""
                sValue = self._imagedata.getValue("LunarFeatureDiameter_{}".format(str(iFeatureId)))
                if sValue != "": sDataLunarFeature = "Diam {}".format(str(round(float(sValue.split(" ")[0]))) + " " + sValue.split(" ")[1])
                sValue = self._imagedata.getValue("LunarFeatureWidth_{}".format(str(iFeatureId)))
                if sValue != "": sDataLunarFeature += "{}Larg {}".format(",  " if sDataLunarFeature != "" else "", str(round(float(sValue.split(" ")[0]))) + " " + sValue.split(" ")[1])
                sValue = self._imagedata.getValue("LunarFeatureLength_{}".format(str(iFeatureId)))
                if sValue != "": sDataLunarFeature += "{}Long {}".format(",  " if sDataLunarFeature != "" else "", str(round(float(sValue.split(" ")[0]))) + " " + sValue.split(" ")[1])
                sValue = self._imagedata.getValue("LunarFeatureDepth_{}".format(str(iFeatureId)))
                if sValue != "": sDataLunarFeature += "{}Prof {}".format(",  " if sDataLunarFeature != "" else "", sValue)
                sValue = self._imagedata.getValue("LunarFeatureHeight_{}".format(str(iFeatureId)))
                if sValue != "": sDataLunarFeature += "{}Haut {}".format(",  " if sDataLunarFeature != "" else "", sValue)

                ifeaturenameheight = self._pilFinalImageDraw.textsize(sFeatureName, font=FONT_LUNARFEATURE_NAME)[1]
                ifeaturenamewidth = self._pilFinalImageDraw.textsize(sFeatureName, font=FONT_LUNARFEATURE_NAME)[0]
                ifeatureinfoheight = self._pilFinalImageDraw.textsize(sFeatureName, font=FONT_LUNARFEATURE_DATA)[1]
                iFeatureInfoWidth = colorBoxSize + 5 + ifeaturenamewidth + 7 + self._pilFinalImageDraw.textsize(sDataLunarFeature, font=FONT_LUNARFEATURE_DATA)[0]
                arrFeatureInfos.append(sFeatureName + "|" + sDataLunarFeature)
                if iFeatureInfoWidth > iMaxFeatureInfoWidth: iMaxFeatureInfoWidth = iFeatureInfoWidth

        iStartPositionX = self._regionPhotoMiniature.getStartPosX() - iMaxFeatureInfoWidth - 5

        for iFeatureId in range(0, len(arrFeatureInfos)):
            # Position
            iStartPositionY = self._regionPhotoMiniature.getEndPosY() - abs(iFeatureId - (len(arrFeatureInfos)-1)) * (ifeaturenameheight + 7) - ifeatureinfoheight
            # draw colored box
            self._pilFinalImageDraw.rectangle((iStartPositionX, iStartPositionY + ifeaturenameheight/2 - colorBoxSize/2, iStartPositionX + colorBoxSize, iStartPositionY + ifeaturenameheight/2 + colorBoxSize), fill=GLOBAL_MOON_FEATURE_COLOR[iFeatureId], outline=GLOBAL_MOON_FEATURE_COLOR[iFeatureId])
            # draw text
            self._pilFinalImageDraw.text((iStartPositionX + colorBoxSize + 5, iStartPositionY), arrFeatureInfos[iFeatureId].split("|")[0], (180,180,180), font=FONT_LUNARFEATURE_NAME)
            self._pilFinalImageDraw.text((iStartPositionX + colorBoxSize + 5 + self._pilFinalImageDraw.textsize(arrFeatureInfos[iFeatureId].split("|")[0], font=FONT_LUNARFEATURE_NAME)[0] + 5, 1 + iStartPositionY + ifeaturenameheight - ifeatureinfoheight), arrFeatureInfos[iFeatureId].split("|")[1], (120,120,120), font=FONT_LUNARFEATURE_DATA)
            # display location on winjupos miniature
            self.addLocationMarkerOnWinjuposImage(iFeatureId + 1)

    def render(self):
        # Render winjupos miniature
        self.renderWinjuposMiniature()

        # position miniature of photo on final image if at least one lunar feature is detailed
        self._regionPhotoMiniature = ImageRegion(0, 0, 0, 0)
        if self._imagedata.getValue("LunarFeatureName_1") != "":
            self._imgPhotoMiniature,  self._imgPhotoMiniatureWidth,  self._imgPhotoMiniatureHeight = self._loadimage("Photo miniature", self._imagedata.getValue("imagefilenamepicture"))
            # Resize to GLOBAL_TOPINFO_HAUTEUR pixel height maxi
            fCoeff = float(GLOBAL_TOPINFO_HAUTEUR) / float(self._imgPhotoMiniatureHeight)
            self._regionPhotoMiniature = ImageRegion(0, int(float(self._imgPhotoMiniatureWidth) * fCoeff), 0, int(float(self._imgPhotoMiniatureHeight) * fCoeff))
            self._imgPhotoMiniature.thumbnail((self._regionPhotoMiniature.getWidth(), self._regionPhotoMiniature.getHeight()), Image.ANTIALIAS)
            print("   --> Photo miniature resized to: {} x {}".format(str(self._regionPhotoMiniature.getWidth()), str(self._regionPhotoMiniature.getHeight())))
            # position photo miniature on final image
            self._regionPhotoMiniature.moveTo(self._finalImageWidth - GLOBAL_MARGE - self._regionPhotoMiniature.getWidth(), GLOBAL_MARGE)
            self._pilFinalImageImg.paste(self._imgPhotoMiniature, (self._regionPhotoMiniature.getStartPosX(), self._regionPhotoMiniature.getStartPosY()))
            # draw border around miniature
            self._pilFinalImageDraw.rectangle((self._regionPhotoMiniature.getStartPosX(), self._regionPhotoMiniature.getStartPosY(), self._regionPhotoMiniature.getEndPosX(), self._regionPhotoMiniature.getEndPosY()), outline=(200, 200, 200))

        super().render()


        # print("title: {}".format(self.getdata().getimagetitle()))
        # print("moon age in days: {}".format(super().getdata().getmoonageindays()))

        # position 6 rows lunar features
        self.renderLunarFeaturesInfo()

        # Save image
        sOutputFileName = self._imagedata.getOutputFilename()
        self._pilFinalImageImg.save(sOutputFileName + ".png", "PNG")
        print(" --> created picture: {}.png".format(sOutputFileName))


class ImageRenderPlanet(ImageRenderer):
    def render(self):
        print("Title: {}".format(super().getdata().gettitle()))


class ImageRenderDeepsky(ImageRenderer):
    def render(self):
        print("Title: {}".format(super().getdata().gettitle()))


def main():
    # get image type
    theparam = ParameterInput()
    imagetype = theparam.getimagetype()
    JsonFilename = theparam.getfilenamejson()
    if JsonFilename == "": JsonFilename = None

    # get image data & renderer
    if imagetype == "MOON":
        theimagedata = ImageDataMoon(JsonFilename)
        theimagedata.initdata()
        theimagerenderer = ImageRenderMoon(theimagedata)
    elif imagetype == "PLANET":
        theimagedata = ImageDataPlanet(JsonFilename)
        theimagedata.initdata()
        theimagerenderer = ImageRenderPlanet(theimagedata)
    elif imagetype == "DEEPSKY":
        theimagedata = ImageDataDeepsky(JsonFilename)
        theimagedata.initdata()
        theimagerenderer = ImageRenderDeepsky(theimagedata)
    else:
        raise Exception("wrong image type")

    # render image
    theimagerenderer.render()
    print ("output file name: {}".format(theimagedata.getOutputFilename()))


if __name__ == "__main__":
    main()

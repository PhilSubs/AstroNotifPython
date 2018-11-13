#!/usr/bin/python2.7
# -*-coding:Latin-1 -*


# minimap.png ... correspond to the minimap bitmap  128x128 pixels
    
import json
import os.path
import datetime
from PIL import Image, ImageDraw, ImageFont

def printDicInput(dicInputValues):
    print ""
    print ""
    print ""
    print "Subject"
    print "-------"
    print "Subject........................ " + dicInputValues["Subject_Type"]
    print "Title.......................... " + dicInputValues["Subject_Title"]
    print "Moon Age....................... " + dicInputValues["Info_MoonAge"]
    print "Moon Illumination.............. " + dicInputValues["Info_MoonIllumination"]
    print "Moon Colongitude............... " + dicInputValues["Info_MoonColongitude"]
    if dicInputValues["Subject_Type"] == "Moon":
        for i in range(0,6):
            sFeatureID = str(i).strip()
            if dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] != "":
                print "Feature " + sFeatureID + " Name................. " + dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"]
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Diameter"] != "": print "Diameter....................... " + dicInputValues["Info_MoonFeature" + sFeatureID + "_Diameter"]
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Height"]   != "": print "Height......................... " + dicInputValues["Info_MoonFeature" + sFeatureID + "_Height"]
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Length"]   != "": print "Length......................... " + dicInputValues["Info_MoonFeature" + sFeatureID + "_Length"]
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Width"]    != "": print "Width.......................... " + dicInputValues["Info_MoonFeature" + sFeatureID + "_Width"]
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Depth"]    != "": print "Depth.......................... " + dicInputValues["Info_MoonFeature" + sFeatureID + "_Depth"]
        print "Additional information......... " + dicInputValues["Info_Additional"]
    elif dicInputValues["Subject_Type"] == "Planet":
        print "Planet Diameter................ " + dicInputValues["Info_Planet_Diameter"]
        print "Planet Altitude................ " + dicInputValues["Info_Planet_Altitude"]
        print "Planet Magnitude............... " + dicInputValues["Info_Planet_Magnitude"]
        print "Planet CMI..................... " + dicInputValues["Info_Planet_CMI"]
        print "Planet CMII.................... " + dicInputValues["Info_Planet_CMII"]
        print "Planet CMIII................... " + dicInputValues["Info_Planet_CMIII"]
        print "Planet Focal Length............ " + dicInputValues["Info_Planet_FocalLength"]
        print "Planet Focal Ratio............. " + dicInputValues["Info_Planet_FocalRatio"]
        print "Planet Resolution.............. " + dicInputValues["Info_Planet_Resolution"]
    elif dicInputValues["Subject_Type"] == "Deep Sky":
        print "Deep Sky Object Type........... " + dicInputValues["Info_DeepSky_Type"]
        print "Deep Sky Object Distance....... " + dicInputValues["Info_DeepSky_Distance"]
        print "Deep Sky Object Apparent Diam.. " + dicInputValues["Info_DeepSky_Diameter"]
        print "Deep Sky object Magnitude...... " + dicInputValues["Info_DeepSky_Magnitude"]
    print ""
    print "Pictures"
    print "--------"
    print "Minimap file name.............. " + dicInputValues["Bitmap_MinimapFileName"]   
    print "Picture file name.............. " + dicInputValues["Bitmap_PictureFileName"]
    print ""
    print "Time & Location"
    print "---------------"
    print "Date........................... " + dicInputValues["TimeLoc_Date"]
    print "Time (UT)...................... " + dicInputValues["TimeLoc_Time"]
    print "Location....................... " + dicInputValues["TimeLoc_Location"]
    print ""
    print "Hardware"
    print "--------"
    print "Scope.......................... " + dicInputValues["Hardware_Optic"]
    print "Mount.......................... " + dicInputValues["Hardware_Mount"]
    print "ADC............................ " + dicInputValues["Hardware_ADC"]
    print "Focal Reducer.................. " + dicInputValues["Hardware_Reducer"]
    print "Barlow......................... " + dicInputValues["Hardware_Barlow"]
    print "Filter......................... " + dicInputValues["Hardware_Filter"]
    print "Camera......................... " + dicInputValues["Hardware_Camera"]
    print ""
    print "Capture"
    print "-------"
    print "Software....................... " + dicInputValues["Capture_Software"]
    print "Bin............................ " + dicInputValues["Capture_Bin"]
    print "Gain........................... " + dicInputValues["Capture_Gain"]
    print "Bits (8/16).................... " + dicInputValues["Capture_Bits"]
    print "Exposition (ms)................ " + dicInputValues["Capture_Exposition"]
    print "Rate (fps)..................... " + dicInputValues["Capture_Rate"]
    print "Total Exposure (s)............... " + dicInputValues["Capture_TotalExposure"]
    print ""
    print "Processing"
    print "----------"
    print "Stacking Software.............. " + dicInputValues["Processing_StackingSoftware"]
    print "Images Processed.(detailed).... " + dicInputValues["Processing_ImagesProcessed"]
    print "Processing Software............ " + dicInputValues["Processing_ProcessingSoftware"]
    print "Rendering Software............. " + dicInputValues["Processing_RenderingSoftware"]
    print "Additional Info................ " + dicInputValues["Processing_AdditionalInfo"]
    print ""
    print ""
    print ""

def getEmptyDicInput():
    dicInput = {}
    dicInput["Bitmap_MinimapFileName"] = ""
    dicInput["Bitmap_PictureFileName"] = ""
    dicInput["Subject_Type"] = ""
    dicInput["Subject_Title"] = ""
    dicInput["Info_MoonAge"] = ""
    dicInput["Info_MoonIllumination"] = ""
    dicInput["Info_MoonColongitude"] = ""
    for i in range(0,6):
        sFeatureID = str(i).strip()
        dicInput["Info_MoonFeature" + sFeatureID + "_Name"] = ""
        dicInput["Info_MoonFeature" + sFeatureID + "_Diameter"] = ""
        dicInput["Info_MoonFeature" + sFeatureID + "_Height"] = ""
        dicInput["Info_MoonFeature" + sFeatureID + "_Length"] = ""
        dicInput["Info_MoonFeature" + sFeatureID + "_Width"] = ""
        dicInput["Info_MoonFeature" + sFeatureID + "_Depth"] = ""
    dicInput["Info_Additional"] = ""
    dicInput["Info_Planet_Diameter"] = ""
    dicInput["Info_Planet_Altitude"] = ""
    dicInput["Info_Planet_Magnitude"] = ""
    dicInput["Info_Planet_CMI"] = ""
    dicInput["Info_Planet_CMII"] = ""
    dicInput["Info_Planet_CMIII"] = ""
    dicInput["Info_Planet_FocalLength"] = ""
    dicInput["Info_Planet_FocalRatio"] = ""
    dicInput["Info_Planet_Resolution"] = ""
    dicInput["Info_DeepSky_Type"] = ""
    dicInput["Info_DeepSky_Distance"] = ""
    dicInput["Info_DeepSky_Diameter"] = ""
    dicInput["Info_DeepSky_Magnitude"] = ""
    dicInput["TimeLoc_Date"] = ""
    dicInput["TimeLoc_Time"] = ""
    dicInput["TimeLoc_Location"] = ""
    dicInput["Hardware_Optic"] = ""
    dicInput["Hardware_Mount"] = ""
    dicInput["Hardware_ADC"] = ""
    dicInput["Hardware_Reducer"] = ""
    dicInput["Hardware_Barlow"] = ""
    dicInput["Hardware_Camera"] = ""
    dicInput["Hardware_Filter"] = ""
    dicInput["Capture_Software"] = ""
    dicInput["Capture_Bin"] = ""
    dicInput["Capture_Gain"] = ""
    dicInput["Capture_Bits"] = ""
    dicInput["Capture_Exposition"] = ""
    dicInput["Capture_Rate"] = ""
    dicInput["Capture_TotalExposure"] = ""
    dicInput["Processing_StackingSoftware"] = ""
    dicInput["Processing_ImagesProcessed"] = ""
    dicInput["Processing_Pre-processingSoftware"] = ""
    dicInput["Processing_ProcessingSoftware"] = ""
    dicInput["Processing_RenderingSoftware"] = ""
    dicInput["Processing_AdditionalInfo"] = ""
    return dicInput
    
def addInfoToString(sInfoToBeAdded, sLabel, sUnit,  sInitialString, sSeparator):
    sReturnValue = sInitialString
    if sInfoToBeAdded != "":
        if sReturnValue != "":
            sReturnValue = sReturnValue + sSeparator
        sReturnValue = sReturnValue + sLabel + sInfoToBeAdded
        if sUnit != "":
            sReturnValue = sReturnValue + sUnit
    return sReturnValue
        
def getOccurrencesInStringList(sStringList, sSearchString):
    arrList = sStringList.split(",")
    iNbOccMatch = 0
    iNbOccExactMatch = 0
    for i in range(0, len(arrList)):
        if sSearchString.lower().strip() == arrList[i].lower().strip(): 
            iNbOccExactMatch = iNbOccExactMatch + 1
            sReturnValueExactMatch = arrList[i]
        elif sSearchString.lower() in arrList[i].lower(): 
            iNbOccMatch = iNbOccMatch + 1
            sReturnValueMatch = arrList[i]
    if iNbOccMatch != 1 and iNbOccExactMatch != 1: 
        sReturnValue = None
        iReturnOcc = iNbOccMatch
    elif iNbOccExactMatch == 1:
        sReturnValue = sReturnValueExactMatch
        iReturnOcc = iNbOccExactMatch
    elif iNbOccMatch == 1:
        sReturnValue = sReturnValueMatch
        iReturnOcc = iNbOccMatch
    return iReturnOcc, sReturnValue
    
def requestValue(sType, sPrompt, sDefaultValue, bIsMandatory, sPossibleValuesList):
    # compute prompt
    sPromptDisplayed = (sPrompt + "...................................................................")[:60]
    if not sPossibleValuesList is None:
        sPromptDisplayed = sPromptDisplayed + " [" + sPossibleValuesList + "] "
    if not bIsMandatory and not sDefaultValue is None:
        sPromptDisplayed = sPromptDisplayed + " (/ si aucun)"
    if not sDefaultValue is None:
        sPromptDisplayed = sPromptDisplayed + "  --> " + sDefaultValue + " ?"
    sPromptDisplayed = sPromptDisplayed + "   "
    # loop until valid answer
    bAnswerIsValid = False
    while not bAnswerIsValid:
        sValue = raw_input(sPromptDisplayed)
        if sValue == "" and not sDefaultValue is None: sValue = sDefaultValue  # empty answer are replaced with default value
        if sValue == "/": sValue = ""                                          # n/a is replaced with empty answer
        if sValue == "":
            if bIsMandatory:
                bAnswerIsValid = False
                print "  ERREUR: cette donnée est obigatoire !"
            else:
                bAnswerIsValid = True
        else:
            # Checks
            if sType == "Filename":
                if not sPossibleValuesList is None:
                    if not sPossibleValuesList.lower() in sValue.lower(): sValue = sValue + sPossibleValuesList
                if os.path.isfile(sValue):
                    bAnswerIsValid = True
                else:
                    bAnswerIsValid = False
                    print "  ERREUR: le fichier  '" + sValue + "'  est introuvable !"
            elif sType == "StringFromList":
                iNbOcc, sValueSelected = getOccurrencesInStringList(sPossibleValuesList, sValue)
                if iNbOcc == 1:
                    sValue = sValueSelected
                    bAnswerIsValid = True
                else:
                    bAnswerIsValid = False
                    print "  ERREUR: la valeur doit être dans la liste:  " + sPossibleValuesList + " !"
            elif sType == "DateAAAA-MM-JJ":
                try:
                    aDate = datetime.datetime(int(sValue[0:4]), int(sValue[5:7]), int(sValue[8:]), 0, 0, 0)
                    if sValue[4:5] != "-" or sValue[7:8] != "-":
                        bAnswerIsValid = False
                    else:
                        bAnswerIsValid = True
                except:
                    bAnswerIsValid = False
            elif sType == "TimeHH:MM":
                try:
                    iHour = int(sValue[0:2])
                    iMinute = int(sValue[4:6])
                    if sValue[2:3] != ":" or iHour < 0 or iHour > 23:
                        bAnswerIsValid = False
                    else:
                        bAnswerIsValid = True
                except:
                    bAnswerIsValid = False
            elif sType == "String":
                bAnswerIsValid = True
                    
    return sValue

    
# Value lists    
LIST_OPTIC = 'Celestron SCT 11" 280/2800,EF70-300mm f/4-5.6L IS USM'
LIST_MOUNT = '/,CGEM'
LIST_YESNO = "Y,N"
LIST_ADC = "/,ASI ADC"
LIST_BARLOW = "/,Powermate x2,Powermate x2.5"
LIST_REDUCER = "/,Celestron Reducer x0.67"
LIST_CAMERA = "ASI 224MC,ASI 178MM,ASI 120MM,CANON EOS 450D"
LIST_FILTER = "IR6,IR7,IR8,RG610,#23A,#25,UV/IR Cut,UHC,OIII"
LIST_CAPTURE_SOFTWARE = "Firecapture,Sharpcap"
LIST_CAPTURE_BIN = "Bin x1,Bin x2"
LIST_CAPTURE_BITS = "8,16"
LIST_PREPROCESSING_SOFTWARE = "PIPP"
LIST_PROCESSING_STACKING_SOFTWARE = "Autostakkert!2,Autostakkert!3,Deep Sky Staker,SIRIL"
LIST_PROCESSING_SOFTWARE = "Registax6,Deep Sky Staker,Siril"
LIST_PROCESSING_RENDERING_SOFTWARE = "Photoshop,Lightroom"

DEFAULT_YES = "Y"
DEFAULT_NO = "N"
DEFAULT_LOCATION = "Plascassier (06), France"
DEFAULT_MOUNT = 'CGEM'
DEFAULT_OPTIC = 'Celestron SCT 11" 280/2800'
DEFAULT_ADC = "ASI ADC"
DEFAULT_BARLOW = "Powermate x2"
DEFAULT_REDUCER = "Celestron Reducer x0.67"
DEFAULT_UVFILTER = "UV/IR Cut"
DEFAULT_CAPTURE_SOFTWARE = "Firecapture"
DEFAULT_CAPTURE_BIN = "Bin x1"
DEFAULT_CAPTURE_BITS = "8"
DEFAULT_PROCESSING_STACKING_SOFTWARE = "Autostakkert!3"
DEFAULT_PROCESSING_SOFTWARE = "Registax6"
DEFAULT_PROCESSING_RENDERING_SOFTWARE = "Photoshop"

# Constants
iFinalPictureMarginWidth = 20 # Margin for the final picture         
iMarginPicture = 10           # Margin around the picture, inside the border   
iMarginTopPicture = 20        # Margin above the picture, below the title/subtitle 
iMarginBottomPicture = 10     # Margin below the picture, above the logo and data 
iBorderSize = 1               # Border around the picture
iDataInfoHeight = 300         # height of data info display at the bottom    
iPositionMinimapX = 200       # position of the minimap, from the right edge (+margin)    
iPositionMinimapY = 100       # position of the minimap, from  the border around the picture (+ margin)   
iDataTextInterligne = 3       # interline in pixel between data text lines
iMarginSignature = 5          # Margin for signature related to inside border of picture

DATA_TITLE_TELESCOPE = "MATERIEL  "
DATA_TITLE_CAMERA = "CAMERA  "
DATA_TITLE_CAPTURE = "CAPTURE  "
DATA_TITLE_PROCESSING = "TRAITEMENT  "



print ""
print ""
sJsonFilename = requestValue("Filename", "Name of PJSON parameters file to use ", None, False, ".json")
if sJsonFilename != "":
    with open(sJsonFilename, 'r') as fp:
        dicInputValues = json.load(fp)
else:
    dicInputValues = getEmptyDicInput() 
    print ""
    print ""
    print "Pictures"
    print "--------"
    dicInputValues["Bitmap_MinimapFileName"] = requestValue("Filename", "Name of PNG file for minimap (128x128) ", "minimap.png", False, ".png")
    dicInputValues["Bitmap_PictureFileName"] = requestValue("Filename", "Name of PNG file for picture ", None, True, ".png")
    print ""
    print "Subject"
    print "-------"
    dicInputValues["Subject_Type"]  = (requestValue("StringFromList", "Object type: Moon, Planet, Deep Sky ", None, True, "M,P,DS")).upper()
    dicInputValues["Subject_Title"] = requestValue("String", "Title ", None, True, None)
    if dicInputValues["Subject_Type"] == "M":  dicInputValues["Subject_Type"] = "Moon"
    if dicInputValues["Subject_Type"] == "P":  dicInputValues["Subject_Type"] = "Planet"
    if dicInputValues["Subject_Type"] == "DS": dicInputValues["Subject_Type"] = "Deep Sky"
    if dicInputValues["Subject_Type"] == "Moon":
        dicInputValues["Info_MoonAge"]          = requestValue("String", "Moon Age ", None, False, None) 
        dicInputValues["Info_MoonIllumination"] = requestValue("String", "Moon Illumination (%) ", None, False, None) 
        dicInputValues["Info_MoonColongitude"]  = requestValue("String", "Moon Colongitude (deg) ", None, False, None) 
        bAllFeaturesFilled = False
        for i in range(0,6):
            sFeatureID = str(i).strip()
            dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] = ""
            if not bAllFeaturesFilled:
                dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] = requestValue("String", "    Feature " + sFeatureID + " Name ", None, False, None)
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] != "":
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Diameter"] = requestValue("String", "        Diameter (+ unit) ", None, False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Height"]   = requestValue("String", "        Height (+ unit) ", None, False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Length"]   = requestValue("String", "        Length  (+ unit)", None, False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Width"]    = requestValue("String", "        Width (+ unit) ", None, False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Depth"]    = requestValue("String", "        Depth (+ unit) ", None, False, None)
                else:
                    bAllFeaturesFilled = True
        dicInputValues["Info_Additional"] = requestValue("String", "Additional comment ", None, False, None)
    elif dicInputValues["Subject_Type"] == "Planet":
        dicInputValues["Info_Planet_Diameter"]    = requestValue("String", "Planet Diameter (sec) ", None, False, None) 
        dicInputValues["Info_Planet_Altitude"]    = requestValue("String", "Planet Altitude (deg) ", None, False, None) 
        dicInputValues["Info_Planet_Magnitude"]   = requestValue("String", "Planet Magnitude ", None, False, None) 
        dicInputValues["Info_Planet_CMI"]         = requestValue("String", "Planet CMI (deg) ", None, False, None) 
        dicInputValues["Info_Planet_CMII"]        = requestValue("String", "Planet CMII (deg) ", None, False, None) 
        dicInputValues["Info_Planet_CMIII"]       = requestValue("String", "Planet CMIII (deg) ", None, False, None) 
        dicInputValues["Info_Planet_FocalLength"] = requestValue("String", "Planet Focal Length (mm) ", None, False, None) 
        dicInputValues["Info_Planet_FocalRatio"]  = requestValue("String", "Planet Focal Ratio (F/..) ", None, False, None) 
        dicInputValues["Info_Planet_Resolution"]  = requestValue("String", "Planet Resolution (sec) ", None, False, None) 
    elif dicInputValues["Subject_Type"] == "Deep Sky":
        dicInputValues["Info_DeepSky_Type"]      = requestValue("String", "Object Type ", None, False, None) 
        dicInputValues["Info_DeepSky_Distance"]  = requestValue("String", "Object Distance (+ unit) ", None, False, None) 
        dicInputValues["Info_DeepSky_Diameter"]  = requestValue("String", "Object Diameter (+ unit) ", None, False, None) 
        dicInputValues["Info_DeepSky_Magnitude"] = requestValue("String", "Object Magnitude ", None, False, None) 
    print ""
    print "Time & Location"
    print "---------------"
    dicInputValues["TimeLoc_Date"]     = requestValue("DateAAAA-MM-JJ", "Date       [AAAA-MM-JJ] ", None, True, None)
    dicInputValues["TimeLoc_Time"]     = requestValue("TimeHH:MM",      "Time GMT   [HH:MM] ", None, True, None)
    dicInputValues["TimeLoc_Location"] = requestValue("String",         "Location ", DEFAULT_LOCATION, True, None)
    print ""
    print "Hardware"
    print "--------"
    dicInputValues["Hardware_Optic"]   = requestValue("StringFromList", "Optical instrument ", DEFAULT_OPTIC, True, LIST_OPTIC)
    dicInputValues["Hardware_Mount"]   = requestValue("String", "Mount ", DEFAULT_MOUNT, True, LIST_MOUNT)
    dicInputValues["Hardware_ADC"]     = requestValue("StringFromList", "Accessory: ADC ?", DEFAULT_ADC, False, LIST_ADC)
    dicInputValues["Hardware_Reducer"] = requestValue("StringFromList", "Accessory: Reducer ?", DEFAULT_REDUCER, False, LIST_REDUCER)
    dicInputValues["Hardware_Barlow"]  = requestValue("StringFromList", "Accessory: Barlow ?", DEFAULT_BARLOW, False, LIST_BARLOW)
    dicInputValues["Hardware_Camera"]  = (requestValue("StringFromList", "Camera ", None, True, LIST_CAMERA)).upper()
    if dicInputValues["Hardware_Camera"] == "ASI 224MC":
        dicInputValues["Hardware_Filter"]   = requestValue("StringFromList", "Filter ", DEFAULT_UVFILTER, False, LIST_FILTER)
    else:
        dicInputValues["Hardware_Filter"]   = requestValue("StringFromList", "Filter ", None, False, LIST_FILTER)
    print ""
    print "Capture"
    print "-------"
    dicInputValues["Capture_Software"]      = requestValue("StringFromList", "Capture software ", DEFAULT_CAPTURE_SOFTWARE, True, LIST_CAPTURE_SOFTWARE)
    dicInputValues["Capture_Bin"]           = requestValue("StringFromList", "Bin setting ", DEFAULT_CAPTURE_BIN, True, LIST_CAPTURE_BIN)
    dicInputValues["Capture_Gain"]          = requestValue("String", "Gain setting ", None, True, None)
    dicInputValues["Capture_Bits"]          = requestValue("StringFromList", "Bits setting ", DEFAULT_CAPTURE_BITS, True, LIST_CAPTURE_BITS)
    dicInputValues["Capture_Exposition"]    = requestValue("String", "Exposition (+ unit) ", None, True, None)
    dicInputValues["Capture_Rate"]          = requestValue("String", "Frame rate (fps) ", None, False, None)
    dicInputValues["Capture_TotalExposure"] = requestValue("String", "Total Exposure (+ unit) ", None, True, None)
    print ""
    print "Processing"
    print "----------"
    dicInputValues["Processing_Pre-processingSoftware"] = requestValue("StringFromList", "Pre-processing software ", None, False, LIST_PREPROCESSING_SOFTWARE)
    dicInputValues["Processing_StackingSoftware"]       = requestValue("StringFromList", "Stacking software ", DEFAULT_PROCESSING_STACKING_SOFTWARE, False, LIST_PROCESSING_STACKING_SOFTWARE)
    dicInputValues["Processing_ImagesProcessed"]        = requestValue("String", "# images processed (detailed captured, stacked, darks,...) ", None, True, None)
    dicInputValues["Processing_ProcessingSoftware"]     = requestValue("StringFromList", "Processing software ", DEFAULT_PROCESSING_SOFTWARE, False, LIST_PROCESSING_SOFTWARE)
    dicInputValues["Processing_RenderingSoftware"]      = requestValue("StringFromList", "Final rendering software ", DEFAULT_PROCESSING_RENDERING_SOFTWARE, False, LIST_PROCESSING_RENDERING_SOFTWARE)
    dicInputValues["Processing_AdditionalInfo"]         = requestValue("String", "Additional info (resize,...) ", None, False, None)

printDicInput(dicInputValues)

print ""
sOk = (requestValue("StringFromList", "Ok to proceed ? ", DEFAULT_NO, True, LIST_YESNO)).upper()
if sOk == "N":
    print ""
    print "Aborted."
    print ""
else:
    print ""
    print "Processing..."
    print ""

    # Compute output file name
    sOutputFileName = dicInputValues["TimeLoc_Date"].replace("-","") + dicInputValues["TimeLoc_Time"].replace(":","") + " - " + dicInputValues["Subject_Type"] + " - " + dicInputValues["Subject_Title"]

    # Save parameters in JSON file
    if sJsonFilename == "":
        with open(sOutputFileName[0:12] + '.json', 'w') as fp:
            try:
                json.dump(dicInputValues, fp)
            except:
                pass
                print ""
            print " --> created json file: " + sOutputFileName[0:12] + ".json"
    
    # create temporary bitmap (for computing text size)
    theTempImg = Image.new( 'RGBA', (1920, 100), (0, 0, 0, 255))
    theTempDraw = ImageDraw.Draw(theTempImg)
    
    # Font size
    iFontSizeTitle     = 30
    iFontSizeSubtitle  = 16
    iFontSizeDataText  = 14
    iFontSizeSignature = 18
            
    # Set colors
    theColorTitle           = (255,255,255)
    theColorSubTitle        = (164,164,164)
    theColorDataText        = (96,96,96)
    theColorDataTitle       = (128,128,128)
    theColorSignature       = (228,228,228)
    theColorSignatureShadow = (32,32,32)
    
    # Set fonts
    theDataFont      = ImageFont.truetype("PCNavita-Regular.ttf", iFontSizeDataText)
    theTitleFont     = ImageFont.truetype("georgia.ttf", iFontSizeTitle)
    theSubTitleFont  = ImageFont.truetype("georgia.ttf", iFontSizeSubtitle)
    theSignatureFont = ImageFont.truetype("Sugar Candy.ttf", iFontSizeSignature)

    # get pictures size
    imgPicture = Image.open(dicInputValues["Bitmap_PictureFileName"])
    iPictureWidth, iPictureHeight = imgPicture.size
    iPictureWidthAdjustBorder = 0
    if iPictureWidth < 1000 and dicInputValues["Subject_Type"] == "Deep Sky": 
        iPictureWidthAdjustBorder = (1000 - iPictureWidth) / 2
        print ">>> Adjusted image width to 1000 instead of " + str(iPictureWidth) + " (border: " + str(iPictureWidthAdjustBorder) + ")"
        iPictureWidth = 1000

    print "Picture size: " + str(iPictureWidth) + "x" + str(iPictureHeight)
    imgMinimap = None
    if dicInputValues["Bitmap_MinimapFileName"] != "":
        imgMinimap = Image.open(dicInputValues["Bitmap_MinimapFileName"])
        iMinimapWidth, iMinimapHeight = imgMinimap.size
        print "Minimap size: " + str(iMinimapWidth) + "x" + str(iMinimapHeight)

    # Compute fields to be displayed
    sField_Signature = "PhilippeLarosa"
    sField_Date      = dicInputValues["TimeLoc_Date"][8:] + " " + ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'][int(dicInputValues["TimeLoc_Date"][5:7])-1] + " " + dicInputValues["TimeLoc_Date"][0:4] + "  " + dicInputValues["TimeLoc_Time"] + " GMT"
    sField_Location  = dicInputValues["TimeLoc_Location"]
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonAge"], "Lune: age ", "", "", "")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonIllumination"], "illum. ", "%", sField_MoonEphem, " - ")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonColongitude"], "colong. ", " deg", sField_MoonEphem, " - ")
    sField_Title     = dicInputValues["Subject_Title"]
    if dicInputValues["Subject_Type"] == "Moon":
        sField_SubTitle1 = ""
        sField_SubTitle2 = ""
        sField_SubTitle3 = ""
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Name"], "", ": ", "", "")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Diameter"], "Diametre ", "", sField_Object_Data_1, "  ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Width"], "Largeur ", "", sField_Object_Data_1, "  ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Length"], "Longueur ", "", sField_Object_Data_1, "  ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Depth"], "Profondeur ", "", sField_Object_Data_1, "  ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Height"], "Hauteur ", "", sField_Object_Data_1, "  ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Name"], "", ": ", "", "")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Diameter"], "Diametre ", "", sField_Object_Data_2, "  ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Width"], "Largeur ", "", sField_Object_Data_2, "  ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Length"], "Longueur ", "", sField_Object_Data_2, "  ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Depth"], "Profondeur ", "", sField_Object_Data_2, "  ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Height"], "Hauteur ", "", sField_Object_Data_2, "  ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Name"], "", ": ", "", "")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Diameter"], "Diametre ", "", sField_Object_Data_3, "  ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Width"], "Largeur ", "", sField_Object_Data_3, "  ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Length"], "Longueur ", "", sField_Object_Data_3, "  ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Depth"], "Profondeur ", "", sField_Object_Data_3, "  ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Height"], "Hauteur ", "", sField_Object_Data_3, "  ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Name"], "", ": ", "", "")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Diameter"], "Diametre ", "", sField_Object_Data_4, "  ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Width"], "Largeur ", "", sField_Object_Data_4, "  ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Length"], "Longueur ", "", sField_Object_Data_4, "  ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Depth"], "Profondeur ", "", sField_Object_Data_4, "  ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Height"], "Hauteur ", "", sField_Object_Data_4, "  ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Name"], "", ": ", "", "")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Diameter"], "Diametre ", "", sField_Object_Data_5, "  ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Width"], "Largeur ", "", sField_Object_Data_5, "  ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Length"], "Longueur ", "", sField_Object_Data_5, "  ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Depth"], "Profondeur ", "", sField_Object_Data_5, "  ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Height"], "Hauteur ", "", sField_Object_Data_5, "  ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Name"], "", ": ", "", "")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Diameter"], "Diametre ", "", sField_Object_Data_6, "  ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Width"], "Largeur ", "", sField_Object_Data_6, "  ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Length"], "Longueur ", "", sField_Object_Data_6, "  ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Depth"], "Profondeur ", "", sField_Object_Data_6, "  ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Height"], "Hauteur ", "", sField_Object_Data_6, "  ")
    elif dicInputValues["Subject_Type"] == "Planet":
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Diameter"], "Diametre ", '"', "", "")
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Magnitude"], "Magnitude ", "", sField_SubTitle1, " - ")
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Altitude"], "Altitude ", "deg", sField_SubTitle1, " - ")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_Planet_CMI"], "CMI ", "deg", "", "")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_Planet_CMII"], "CMII ", "deg", sField_SubTitle2, " - ")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_Planet_CMIII"], "CMIII ", "deg", sField_SubTitle2, " - ")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_Planet_FocalLength"], "Focal ", "", "", "")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_Planet_FocalRatio"], "F/", "", sField_SubTitle3, " - ")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_Planet_Resolution"], "Resolution  ", '"', sField_SubTitle3, " - ")
        sField_Object_Data_1 = ""
        sField_Object_Data_2 = ""
        sField_Object_Data_3 = ""
        sField_Object_Data_4 = ""
        sField_Object_Data_5 = ""
        sField_Object_Data_6 = ""
    elif dicInputValues["Subject_Type"] == "Deep Sky":
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_DeepSky_Distance"], "Distance ", "", "", "")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_DeepSky_Diameter"], "Diametre ", "", "", "")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_DeepSky_Magnitude"], "Magnitude ", "", "", "")
        sField_Object_Data_1 = ""
        sField_Object_Data_2 = ""
        sField_Object_Data_3 = ""
        sField_Object_Data_4 = ""
        sField_Object_Data_5 = ""
        sField_Object_Data_6 = ""
    sField_Data_Optic = addInfoToString(dicInputValues["Hardware_Optic"], DATA_TITLE_TELESCOPE, "", "", "")
    sField_Data_Optic = addInfoToString(dicInputValues["Hardware_Mount"], "", "", sField_Data_Optic, " - ")
    sField_Data_Optic = addInfoToString(dicInputValues["Hardware_ADC"], "ADC ", "", sField_Data_Optic, " - ")
    sField_Data_Optic = addInfoToString(dicInputValues["Hardware_Reducer"], "", "", sField_Data_Optic, " - ")
    sField_Data_Optic = addInfoToString(dicInputValues["Hardware_Barlow"], "Barlow ", "", sField_Data_Optic, " - ")
    sField_Data_Optic = addInfoToString(dicInputValues["Hardware_Filter"], "Filtre ", "", sField_Data_Optic, " - ")
    sField_Data_Camera = addInfoToString(dicInputValues["Hardware_Camera"], DATA_TITLE_CAMERA, "", "", "")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Software"], DATA_TITLE_CAPTURE, "", "", "")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Bin"], "", "", sField_Data_Capture, " - ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Bits"], "", " bits", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Gain"], "Gain ", "", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Exposition"], "Exp. ", "", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Rate"], "", " fps", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_TotalExposure"], "Total ", "", sField_Data_Capture, " - ")
    sField_Data_Processing = addInfoToString(DATA_TITLE_PROCESSING, "", "", "", "")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_ImagesProcessed"], "", "", sField_Data_Processing, "")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_Pre-processingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_StackingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_ProcessingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_RenderingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_AdditionalInfo"], "", "", sField_Data_Processing, " - ")
    
    print ""
    print ""
    print "FIELDS"
    print "------"
    print ""
    print "sField_Date: " + sField_Date
    print "sField_Location: " + sField_Location
    print "sField_MoonEphem: " + sField_MoonEphem
    print "sField_Title: " + sField_Title
    print "sField_SubTitle1: " + sField_SubTitle1
    print "sField_SubTitle2: " + sField_SubTitle2
    print "sField_SubTitle3: " + sField_SubTitle3
    print "sField_Data_Optic: " + sField_Data_Optic
    print "sField_Data_Camera: " + sField_Data_Camera
    print "sField_Data_Capture: " + sField_Data_Capture
    print "sField_Data_Processing: " + sField_Data_Processing
    print "sField_Object_Data_1: " + sField_Object_Data_1
    print "sField_Object_Data_2: " + sField_Object_Data_2
    print "sField_Object_Data_3: " + sField_Object_Data_3
    print "sField_Object_Data_4: " + sField_Object_Data_4
    print "sField_Object_Data_5: " + sField_Object_Data_5
    print "sField_Object_Data_6: " + sField_Object_Data_6
    print ""
    print ""
    
    # compute objects size and position
    iTitleAndSubtitleHeight = theTempDraw.textsize(sField_Title, font=theTitleFont)[1] + iDataTextInterligne * 5  
    iTitleAndSubtitleHeight = iTitleAndSubtitleHeight + theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[1] + iDataTextInterligne
    iTitleAndSubtitleHeight = iTitleAndSubtitleHeight + theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[1] + iDataTextInterligne
    iTitleAndSubtitleHeight = iTitleAndSubtitleHeight + theTempDraw.textsize(sField_SubTitle3, font=theSubTitleFont)[1]
    if not imgMinimap is None:                      
        iMoonMinimapHeight = iMinimapHeight
    else:
        iMoonMinimapHeight = 0
    iDateLocationMoonEphemHeight = theTempDraw.textsize(sField_Date, font=theDataFont)[1] + iDataTextInterligne
    iDateLocationMoonEphemHeight = theTempDraw.textsize(sField_Location, font=theDataFont)[1] + iDataTextInterligne
    iDateLocationMoonEphemHeight = theTempDraw.textsize(sField_MoonEphem, font=theDataFont)[1]
    
    iTopInfoHeight = iDateLocationMoonEphemHeight
    if iTitleAndSubtitleHeight > iTopInfoHeight: iTopInfoHeight = iTitleAndSubtitleHeight
    if iMoonMinimapHeight > iTopInfoHeight: iTopInfoHeight = iMoonMinimapHeight
    
    print "Top Info Height: " + str(iTopInfoHeight) + "   (Date/Location/Moon ephem: " + str(iDateLocationMoonEphemHeight) + ", Title/Subtitle: " + str(iTitleAndSubtitleHeight) + ", Minimap: " + str(iMoonMinimapHeight)
    
    iObjectDataInfoHeight = theTempDraw.textsize(sField_Object_Data_1, font=theDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_2, font=theDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_3, font=theDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_4, font=theDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_5, font=theDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_6, font=theDataFont)[1]
    iTechnicalDataInfoHeight = theTempDraw.textsize(sField_Data_Optic,             font=theDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Data_Camera,            font=theDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Data_Capture,           font=theDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Data_Processing,        font=theDataFont)[1]
    if iObjectDataInfoHeight > iTechnicalDataInfoHeight:
        iDataInfoHeight = iObjectDataInfoHeight
    else:
        iDataInfoHeight = iTechnicalDataInfoHeight
    print "Data Info Height: " + str(iDataInfoHeight)
    iPictureWithBorderWidth  = iBorderSize + iMarginPicture + iPictureWidth  + iMarginPicture + iBorderSize
    iPictureWithBorderHeight = iBorderSize + iMarginPicture + iPictureHeight + iMarginPicture + iBorderSize
    print "Picture With Border Width x Height: " + str(iPictureWithBorderWidth) + " x " + str(iPictureWithBorderHeight)
    iFinalImageWidth  = iFinalPictureMarginWidth + iPictureWithBorderWidth + iFinalPictureMarginWidth
    iFinalImageHeight = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture + iDataInfoHeight + iFinalPictureMarginWidth
    print "Final Image Width x Height: " + str(iFinalImageWidth) + " x " + str(iFinalImageHeight)
    
    if not imgMinimap is None:
        iMinimapPositionX = iFinalImageWidth - iMinimapWidth - iFinalPictureMarginWidth
        iMinimapPositionY = iFinalPictureMarginWidth
    iPictureFramePositionX = iFinalPictureMarginWidth
    iPictureFramePositionY = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture
    iPicturePositionX = iPictureFramePositionX + iMarginPicture 
    iPicturePositionY = iPictureFramePositionY + iMarginPicture

    # Compute fields' position
    iField_Signature_X = iPicturePositionX + iPictureWidth - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[0] - iMarginSignature
    iField_Signature_Y = iPicturePositionY + iPictureHeight - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] - iMarginSignature

    iField_Date_X      = iFinalPictureMarginWidth
    iField_Date_Y      = iFinalPictureMarginWidth
    iField_Location_X  = iFinalPictureMarginWidth
    iField_Location_Y  = iField_Date_Y + theTempDraw.textsize(sField_Date, font=theDataFont)[1] + iDataTextInterligne
    iField_MoonEphem_X  = iFinalPictureMarginWidth
    iField_MoonEphem_Y  = iField_Location_Y + theTempDraw.textsize(sField_Location, font=theDataFont)[1] + iDataTextInterligne

    iField_Title_X     = (iPictureWithBorderWidth - theTempDraw.textsize(sField_Title, font=theTitleFont)[0]) / 2
    iField_Title_Y     = iFinalPictureMarginWidth + (iTopInfoHeight - iTitleAndSubtitleHeight) / 2
    iField_SubTitle1_X = (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[0]) / 2
    iField_SubTitle1_Y = iField_Title_Y + theTempDraw.textsize(sField_Title, font=theTitleFont)[1] + iDataTextInterligne * 5
    iField_SubTitle2_X = (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[0]) / 2
    iField_SubTitle2_Y = iField_SubTitle1_Y + theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[1] + iDataTextInterligne
    iField_SubTitle3_X = (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle3, font=theSubTitleFont)[0]) / 2
    iField_SubTitle3_Y = iField_SubTitle2_Y + theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[1] + iDataTextInterligne

    iField_Object_Data_1_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_1, font=theDataFont)[0]
    iField_Object_Data_1_Y = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Object_Data_2_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_2, font=theDataFont)[0]
    iField_Object_Data_2_Y = iField_Object_Data_1_Y + theTempDraw.textsize(sField_Object_Data_1, font=theDataFont)[1] + iDataTextInterligne
    iField_Object_Data_3_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_3, font=theDataFont)[0]
    iField_Object_Data_3_Y = iField_Object_Data_2_Y + theTempDraw.textsize(sField_Object_Data_2, font=theDataFont)[1] + iDataTextInterligne
    iField_Object_Data_4_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_4, font=theDataFont)[0]
    iField_Object_Data_4_Y = iField_Object_Data_3_Y + theTempDraw.textsize(sField_Object_Data_3, font=theDataFont)[1] + iDataTextInterligne
    iField_Object_Data_5_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_5, font=theDataFont)[0]
    iField_Object_Data_5_Y = iField_Object_Data_4_Y + theTempDraw.textsize(sField_Object_Data_4, font=theDataFont)[1] + iDataTextInterligne
    iField_Object_Data_6_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_6, font=theDataFont)[0]
    iField_Object_Data_6_Y = iField_Object_Data_5_Y + theTempDraw.textsize(sField_Object_Data_5, font=theDataFont)[1] + iDataTextInterligne

    iField_Data_Optic_X             = iFinalPictureMarginWidth
    iField_Data_Optic_Y             = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Data_Camera_X            = iFinalPictureMarginWidth
    iField_Data_Camera_Y            = iField_Data_Optic_Y + theTempDraw.textsize(sField_Data_Optic, font=theDataFont)[1] + iDataTextInterligne
    iField_Data_Capture_X           = iFinalPictureMarginWidth
    iField_Data_Capture_Y           = iField_Data_Camera_Y + theTempDraw.textsize(sField_Data_Camera, font=theDataFont)[1] + iDataTextInterligne
    iField_Data_Processing_X        = iFinalPictureMarginWidth
    iField_Data_Processing_Y        = iField_Data_Capture_Y + theTempDraw.textsize(sField_Data_Capture, font=theDataFont)[1] + iDataTextInterligne

    # Display psitions and sizes
    print ""
    print ""
    print "Image final width: " + str(iFinalImageWidth) + " = " + str(iFinalPictureMarginWidth) + " (left margin) + " + str(iMarginPicture) + " (image border) + " + str(iPictureWidth) + " (image width) + " + str(iMarginPicture) + " (image border) + " + str(iFinalPictureMarginWidth) + " (right margin)"
    print "Image final height: " + str(iFinalImageHeight) + " = " + str(iFinalPictureMarginWidth) + " (top margin) + " + str(iTopInfoHeight) + " (Title/Subtitle/Minimap height) + " + str(iMarginTopPicture) + " (top image margin) + " + str(iMarginPicture) + " (image border) + " + str(iPictureHeight) + " (image height) + " + str(iMarginPicture) + " (image border) + " + str(iMarginBottomPicture) + " (bottom image margin) + " + str(iDataInfoHeight) + " (Data Info Height)"
    print "Field Data Optic Y: " + str(iField_Data_Optic_Y)
    print ""
    print ""
    
    # create new bitmap
    theFinalImg = Image.new( 'RGBA', (iFinalImageWidth, iFinalImageHeight), (0, 0, 0, 255))
    theFinalDraw = ImageDraw.Draw(theFinalImg)
    
    # paste minimap             
    if dicInputValues["Bitmap_MinimapFileName"] != "":
        theFinalImg.paste(imgMinimap, (iMinimapPositionX, iMinimapPositionY))
    
    # Display fields
    theFinalDraw.text((iField_Date_X,      iField_Date_Y),      sField_Date,      theColorDataText, font=theDataFont)
    theFinalDraw.text((iField_Location_X,  iField_Location_Y),  sField_Location,  theColorDataText, font=theDataFont)
    theFinalDraw.text((iField_MoonEphem_X, iField_MoonEphem_Y), sField_MoonEphem, theColorDataText, font=theDataFont)
    theFinalDraw.text((iField_Title_X,     iField_Title_Y),     sField_Title,     theColorTitle,    font=theTitleFont)
    theFinalDraw.text((iField_SubTitle1_X, iField_SubTitle1_Y), sField_SubTitle1, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_SubTitle2_X, iField_SubTitle2_Y), sField_SubTitle2, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_SubTitle3_X, iField_SubTitle3_Y), sField_SubTitle3, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_Object_Data_1_X, iField_Object_Data_1_Y), sField_Object_Data_1, theColorDataText, font=theDataFont)
    if sField_Object_Data_1 != "" and dicInputValues["Subject_Type"] == "Moon": theFinalDraw.text((iField_Object_Data_1_X, iField_Object_Data_1_Y), dicInputValues["Info_MoonFeature0_Name"], theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Object_Data_2_X, iField_Object_Data_2_Y), sField_Object_Data_2, theColorDataText, font=theDataFont)
    if sField_Object_Data_2 != "" and dicInputValues["Subject_Type"] == "Moon": theFinalDraw.text((iField_Object_Data_2_X, iField_Object_Data_2_Y), dicInputValues["Info_MoonFeature1_Name"], theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Object_Data_3_X, iField_Object_Data_3_Y), sField_Object_Data_3, theColorDataText, font=theDataFont)
    if sField_Object_Data_3 != "" and dicInputValues["Subject_Type"] == "Moon": theFinalDraw.text((iField_Object_Data_3_X, iField_Object_Data_3_Y), dicInputValues["Info_MoonFeature2_Name"], theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Object_Data_4_X, iField_Object_Data_4_Y), sField_Object_Data_4, theColorDataText, font=theDataFont)
    if sField_Object_Data_4 != "" and dicInputValues["Subject_Type"] == "Moon": theFinalDraw.text((iField_Object_Data_4_X, iField_Object_Data_4_Y), dicInputValues["Info_MoonFeature3_Name"], theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Object_Data_5_X, iField_Object_Data_5_Y), sField_Object_Data_5, theColorDataText, font=theDataFont)
    if sField_Object_Data_5 != "" and dicInputValues["Subject_Type"] == "Moon": theFinalDraw.text((iField_Object_Data_5_X, iField_Object_Data_5_Y), dicInputValues["Info_MoonFeature4_Name"], theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Object_Data_6_X, iField_Object_Data_6_Y), sField_Object_Data_6, theColorDataText, font=theDataFont)
    if sField_Object_Data_6 != "" and dicInputValues["Subject_Type"] == "Moon": theFinalDraw.text((iField_Object_Data_6_X, iField_Object_Data_6_Y), dicInputValues["Info_MoonFeature5_Name"], theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Data_Optic_X,             iField_Data_Optic_Y),             sField_Data_Optic,             theColorDataText,  font=theDataFont)
    if sField_Data_Optic != "": theFinalDraw.text((iField_Data_Optic_X,             iField_Data_Optic_Y),             DATA_TITLE_TELESCOPE,          theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Data_Camera_X,            iField_Data_Camera_Y),            sField_Data_Camera,            theColorDataText,  font=theDataFont)
    if sField_Data_Camera != "": theFinalDraw.text((iField_Data_Camera_X,            iField_Data_Camera_Y),            DATA_TITLE_CAMERA,             theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Data_Capture_X,           iField_Data_Capture_Y),           sField_Data_Capture,           theColorDataText,  font=theDataFont)
    if sField_Data_Capture != "": theFinalDraw.text((iField_Data_Capture_X,           iField_Data_Capture_Y),           DATA_TITLE_CAPTURE,            theColorDataTitle, font=theDataFont)
    theFinalDraw.text((iField_Data_Processing_X,        iField_Data_Processing_Y),        sField_Data_Processing,        theColorDataText,  font=theDataFont)
    if sField_Data_Processing != "": theFinalDraw.text((iField_Data_Processing_X,        iField_Data_Processing_Y),        DATA_TITLE_PROCESSING,         theColorDataTitle, font=theDataFont)
    
    # Draw border around the picture
    theFinalDraw.rectangle((iPictureFramePositionX, iPictureFramePositionY, iPictureFramePositionX + iMarginPicture * 2 + iBorderSize + iPictureWidth , iPictureFramePositionY + iMarginPicture * 2 + iBorderSize + iPictureHeight ), outline=(255, 255, 255, 255), fill=(0, 0, 0, 255))
    
    # paste picture             
    theFinalImg.paste(imgPicture, (iPicturePositionX + iPictureWidthAdjustBorder, iPicturePositionY ))
        
    # Signature
    theFinalDraw.text((iField_Signature_X,     iField_Signature_Y),     sField_Signature, theColorSignatureShadow, font=theSignatureFont)
    theFinalDraw.text((iField_Signature_X - 1, iField_Signature_Y - 1), sField_Signature, theColorSignatureShadow, font=theSignatureFont)
    theFinalDraw.text((iField_Signature_X - 2, iField_Signature_Y - 2), sField_Signature, theColorSignature, font=theSignatureFont)

    # Save image
    theFinalImg.save(sOutputFileName + ".png", "PNG")
    print ""
    print " --> created picture: " + sOutputFileName + ".png"


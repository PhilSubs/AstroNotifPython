#!/usr/bin/python2.7
# coding: utf8 

from __future__ import unicode_literals


# Minimap.png ... correspond to the Winjupos bitmap  128x128 pixels
    
import json
import os.path
import datetime
import math
from PIL import Image, ImageDraw, ImageFont

def getRectangularCoordXYFromLunarLongLat(fLongitude, fLatitude, iBitmapSize): 
    fLongitude = fLongitude - 90.0
    x = iBitmapSize/2 + (iBitmapSize/2 * math.cos(math.radians(fLongitude)) * math.cos(math.radians(fLatitude)))
    y = iBitmapSize/2 - (iBitmapSize/2 * math.sin(math.radians(fLatitude)))
    return x,y

def addLocationMarkerOnWinjuposImage(imgWinjupos, iMoonPositionAngle, fMoonFeatureLongitude, fMoonFeatureLatitude, tupColor, iMoonDiameterInPixel = 128):
    if not(iMoonPositionAngle is None or fMoonFeatureLongitude is None or fMoonFeatureLatitude is None):
        # read parameters
        with open("FormatAstroImages_Settings.json", 'r') as fp:
            dicParameters = json.load(fp)
        fAdjustLongitude = float(dicParameters["CommonValues"]["Minimap_Adjust_Longitude"])
        fAdjustLatitude = float(dicParameters["CommonValues"]["Minimap_Adjust_Latitude"])

        iMoonPositionAngle = float(iMoonPositionAngle)
        fMoonFeatureLongitude = float(fMoonFeatureLongitude) + fAdjustLongitude
        fMoonFeatureLatitude = float(fMoonFeatureLatitude) + fAdjustLatitude
        # Compute position of the feature in the image
        # Draw a tupColor dot of size iMarkerSizeInPx at the position of the feature
        imgNewWinjupos = Image.new( 'RGBA', (iMoonDiameterInPixel, iMoonDiameterInPixel), (255, 255, 255, 0)) # create a new black image
        iMarkerSizeInPx = int(dicParameters["CommonValues"]["Minimap_MarkerSizeInPx"])
        iPosX, iPosY = getRectangularCoordXYFromLunarLongLat(fMoonFeatureLongitude, fMoonFeatureLatitude, iMoonDiameterInPixel)
        drawWinjuposMinimap = ImageDraw.Draw(imgNewWinjupos)
        drawWinjuposMinimap.ellipse((iPosX - int(iMarkerSizeInPx / 2) , iPosY - int(iMarkerSizeInPx / 2), iPosX + int(iMarkerSizeInPx / 2), iPosY + int(iMarkerSizeInPx / 2)), fill=tupColor, outline=tupColor)
        # Rotate minimap by PositionAngle of the Moon
        imgNewWinjupos = imgNewWinjupos.rotate(iMoonPositionAngle, Image.BILINEAR) #Image.NEAREST, Image.BICUBIC, Image.BILINEAR
        
        # merge moon minimap with original bitmap
        imgWinjupos.paste(imgNewWinjupos, (0,0), imgNewWinjupos)

    else:
        print "      Not processed" 
    return imgWinjupos
    
def getEmptyDicInput():
    with open("FormatAstroImages_DataRequest.json", 'r') as fp:
        dicJsonValues = json.load(fp)
    dicInput = {}
    # Loop through DataRequest sections 
#    print "Create Empty Dic:"
    for sKey, aValue in sorted(dicJsonValues.iteritems()): 
#        print "      " + sKey
        # Loop through section's fields
        for i in range(0, len(dicJsonValues[sKey]["Fields"])):
            sSubID = dicJsonValues[sKey]["Fields"][i]["ID"]
            sSubID = sSubID[sSubID.find("-")+1:]
            dicInput[sSubID] = ""
#            print "      (+) " + sSubID
#    print ""
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
    arrList = sStringList.split("|")
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

def getInputValue(sType, sPrompt, aParam1, aParam2):
    # sType: Parameter         aParam1: key from parameter.json   aParam2: override default value
    #                                   (ex.: Hardware/Instrument/Scope)
    #        filename          aParam1: is mandatory (bool)       aParam2: default extension
    #        DateAAAA-MM-JJ    aParam1: is mandatory (bool)       aParam2:  
    #        TimeHH:MM         aParam1: is mandatory (bool)       aParam2:  
    #        String            aParam1: is mandatory (bool)       aParam2: default value
    #        StringFromList    aParam1: is mandatory (bool)       aParam2: possible value list (| delim)
    #        Float             aParam1: is mandatory (bool)       aParam2: default value
    bIsMandatory = False
    theInputValue = None
    theDefaultValue = None
    sPromptDisplayed = (sPrompt + "...................................................................")[:60]
    
    # Compute prompt, default value and flag if mandatory
    if sType == "Parameter":
        # read parameters
        with open("FormatAstroImages_Settings.json", 'r') as fp:
            dicParameters = json.load(fp)
        # Compute prompt
        sKey = aParam1
        theParameterItem = eval('dicParameters["' + sKey.replace("/", '"]["') + '"]')
        bIsMandatory = (theParameterItem["values"][0] != "") # if first value of authorized value list is empty, it means that the field is not mandatory
        theDefaultValue = theParameterItem["default"]
        if not aParam2 is None: theDefaultValue = aParam2 # i param2 is not empty, then it is considered as default value (override)
        if bIsMandatory:
            sPromptDisplayed = sPromptDisplayed + ("  [" + " / ".join(theParameterItem["values"]) + "]")
        else:
            if theDefaultValue != "":
                sPromptDisplayed = sPromptDisplayed + ("  [" + " / ".join(theParameterItem["values"]) + "]").replace("[ / ", "[ - / ")
            else:
                sPromptDisplayed = sPromptDisplayed + ("  [" + " / ".join(theParameterItem["values"]) + "]").replace("[ / ", "[")
    elif sType == "DateAAAA-MM-JJ":
        sPromptDisplayed = sPromptDisplayed + "[AAAA-MM-JJ]"
        bIsMandatory = aParam1
    elif sType == "TimeHH:MM":
        sPromptDisplayed = sPromptDisplayed + "[HH:MM]"
        bIsMandatory = aParam1
    elif sType == "StringFromList":
        sPromptDisplayed = sPromptDisplayed + "[" + aParam2.replace("|", " / ") + "]"
        bIsMandatory = aParam1
    elif sType == "String" and not aParam2 is None:
        theDefaultValue = str(aParam2)
        bIsMandatory = aParam1
    elif sType == "Float" and not aParam2 is None:
        theDefaultValue = str(aParam2)
        bIsMandatory = aParam1
    else:
        bIsMandatory = aParam1
    if not theDefaultValue is None:
        if theDefaultValue != "": sPromptDisplayed = sPromptDisplayed + "  --> " + theDefaultValue
    else:
        theDefaultValue = ""

    #print ":Mandatory:" + str(bIsMandatory)
    #print ":Default:" + theDefaultValue
    
    # loop until a valid answer is read
    bAnswerIsValid = False
    while not bAnswerIsValid:
        theInputValue = raw_input(sPromptDisplayed + "  ")
        if theDefaultValue != "":
            if theInputValue == "":
                if sType == "Float":
                    theInputValue = float(theDefaultValue)
                else:
                    theInputValue = theDefaultValue
            elif theInputValue == "-":
                theInputValue = ""
        
        # check validity
        if theInputValue == "":
            bAnswerIsValid = not bIsMandatory
            #print ":-> valid (default):" + str(bAnswerIsValid)
        elif sType == "Parameter":
            sPossibleValuesList = "|".join(theParameterItem["values"])
            if sPossibleValuesList[0:1] == "|": sPossibleValuesList = sPossibleValuesList[1:]
            iNbOcc, sValueSelected = getOccurrencesInStringList(sPossibleValuesList, theInputValue)
            if iNbOcc == 1:
                theInputValue = sValueSelected
                bAnswerIsValid = True
            else:
                bAnswerIsValid = False
                print "  ERREUR: la valeur doit etre dans la liste:  " + " / ".join(theParameterItem["values"]) + " !"
        elif sType == "Filename":
            if not aParam2 is None:
                if not aParam2.lower() in theInputValue.lower(): theInputValue = theInputValue + aParam2
            if os.path.isfile(theInputValue):
                bAnswerIsValid = True
            else:
                bAnswerIsValid = False
                print "  ERREUR: le fichier  '" + theInputValue + "'  est introuvable !"
        elif sType == "DateAAAA-MM-JJ":
            try:
                if theInputValue.find("-") < 0: theInputValue = theInputValue[0:4] + "-" + theInputValue[4:6] + "-" + theInputValue[6:]
                aDate = datetime.datetime(int(theInputValue[0:4]), int(theInputValue[5:7]), int(theInputValue[8:]), 0, 0, 0)
                if theInputValue[4:5] != "-" or theInputValue[7:8] != "-":
                    bAnswerIsValid = False
                else:
                    bAnswerIsValid = True
            except:
                bAnswerIsValid = False
        elif sType == "TimeHH:MM":
            try:
                if theInputValue.find("-") < 0: theInputValue = theInputValue[0:2] + ":" + theInputValue[2:]
                iHour = int(theInputValue[0:2])
                iMinute = int(theInputValue[4:6])
                if theInputValue[2:3] != ":" or iHour < 0 or iHour > 23:
                    bAnswerIsValid = False
                else:
                    bAnswerIsValid = True
            except:
                bAnswerIsValid = False
        elif sType == "String":
            bAnswerIsValid = True
        elif sType == "Float":
            theInputValue = float(theInputValue)
            bAnswerIsValid = True
        elif sType == "StringFromList":
            iNbOcc, sValueSelected = getOccurrencesInStringList(aParam2, theInputValue)
            if iNbOcc == 1:
                theInputValue = sValueSelected
                bAnswerIsValid = True
            else:
                bAnswerIsValid = False
                print "  ERREUR: la valeur doit etre dans la liste:  " + aParam2.replace("|", " / ") + " !"

    if not theInputValue is None:
        try:
            if theInputValue != "":
                print u"         --> " + theInputValue
        except:
            print u"         --> " + str(theInputValue)

    return theInputValue

def readInputsFromKeyboard():
    dicInputValues = getEmptyDicInput() 

    # Read Lunar Features    
    with open("FormatAstroImages_LunarFeatures.json", 'r') as fp:
        dicLunarFeatures = json.load(fp)
    
    # Use DataRequest json for requesting values
    with open("FormatAstroImages_DataRequest.json", 'r') as fp:
        dicJsonValues = json.load(fp)

    # Loop through DataRequest sections 
    for sKey, aValue in sorted(dicJsonValues.iteritems()): 
        # check if block dependency
        bBlockDependencyVerified = True
        if dicJsonValues[sKey]["Dependency"]["Field"] != "":
            sCondition = 'dicInputValues["' + dicJsonValues[sKey]["Dependency"]["Field"] + '"] ' + dicJsonValues[sKey]["Dependency"]["Operator"] + " " + '"' + dicJsonValues[sKey]["Dependency"]["Value"] + '"'
#            print "       . . . . Block Condition:  " + sCondition
            bCondition = eval(sCondition)
            if not bCondition: bBlockDependencyVerified = False

        if bBlockDependencyVerified:
            print ""
            print ""
            print sKey
            print ("-"*100)[0:len(sKey)]

            for i in range(0, len(dicJsonValues[sKey]["Fields"])):
                # check if field dependency
                bFieldDependencyVerified = True
                if dicJsonValues[sKey]["Fields"][i]["Dependency"]["Field"] != "":
                    sCondition = 'dicInputValues["' + dicJsonValues[sKey]["Fields"][i]["Dependency"]["Field"] + '"] ' + dicJsonValues[sKey]["Fields"][i]["Dependency"]["Operator"] + " " + '"' + dicJsonValues[sKey]["Fields"][i]["Dependency"]["Value"] + '"'
#                    print "       . . . . Field Condition:  " + sCondition
                    bCondition = eval(sCondition)
                    if not bCondition: bFieldDependencyVerified = False

                if bFieldDependencyVerified:
                    sSubID = dicJsonValues[sKey]["Fields"][i]["ID"]
                    sSubID = sSubID[sSubID.find("-")+1:]
                    aParam1 = None
                    if dicJsonValues[sKey]["Fields"][i]["Param1"] != "": aParam1 = dicJsonValues[sKey]["Fields"][i]["Param1"]
                    aParam2 = None
                    if dicJsonValues[sKey]["Fields"][i]["Param2"] != "": aParam2 = dicJsonValues[sKey]["Fields"][i]["Param2"]
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Diameter"  and not sDefaultDiameter  is None: aParam2 = sDefaultDiameter
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Depth"     and not sDefaultDepth     is None: aParam2 = sDefaultDepth
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Height"    and not sDefaultHeight    is None: aParam2 = sDefaultHeight
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Length"    and not sDefaultLength    is None: aParam2 = sDefaultLength
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Width"     and not sDefaultWidth     is None: aParam2 = sDefaultWidth
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Longitude" and not fDefaultLongitude is None: aParam2 = fDefaultLongitude
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Latitude"  and not fDefaultLatitude  is None: aParam2 = fDefaultLatitude
                    sType = dicJsonValues[sKey]["Fields"][i]["Type"]
                    sPrompt = "     "
                    sPrompt = sPrompt + dicJsonValues[sKey]["Fields"][i]["Prompt"]
                    if dicInputValues[sSubID] == "": 
                        dicInputValues[sSubID] = getInputValue(sType, sPrompt, aParam1, aParam2)
                    # if moon feature name, then we take values from the json Lunar Features file if exist
                    if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Name":
                        fDefaultLongitude = None
                        fDefaultLatitude = None
                        sDefaultHeight = None
                        sDefaultWidth = None
                        sDefaultLength = None
                        sDefaultDepth = None
                        sDefaultDiameter = None
                        if dicInputValues[sSubID].upper() in dicLunarFeatures:
                            if not dicLunarFeatures[dicInputValues[sSubID].upper()]["LongitudeInDeg"] is None: fDefaultLongitude = dicLunarFeatures[dicInputValues[sSubID].upper()]["LongitudeInDeg"]
                            if not dicLunarFeatures[dicInputValues[sSubID].upper()]["LatitudeInDeg"]  is None: fDefaultLatitude  = dicLunarFeatures[dicInputValues[sSubID].upper()]["LatitudeInDeg"]
                            if not dicLunarFeatures[dicInputValues[sSubID].upper()]["LengthInKm"]     is None: sDefaultLength    = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["LengthInKm"])
                            if not dicLunarFeatures[dicInputValues[sSubID].upper()]["WidthInKm"]      is None: sDefaultWidth     = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["WidthInKm"])
                            if not dicLunarFeatures[dicInputValues[sSubID].upper()]["HeightInM"]      is None: sDefaultHeight    = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["HeightInM"])
                            sDefaultLunarFeatureValues = "          Lunar Feature Info ..."
                            if not fDefaultLongitude is None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Long: " + str(fDefaultLongitude)
                            if not fDefaultLatitude is None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Lat: "  + str(fDefaultLatitude)
                            if not sDefaultLength   is None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Width: " + str(sDefaultLength) + " km"
                            if not sDefaultWidth   is None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Length: " + str(sDefaultWidth) + " km"
                            if not sDefaultHeight  is None: sDefaultLunarFeatureValues = sDefaultLunarFeatureValues + "  Height: " + str(sDefaultHeight) + " m"
                            print sDefaultLunarFeatureValues
                            if not sDefaultWidth is None and not sDefaultLength is None:
                                if sDefaultLength != 0.0:
                                    if float(sDefaultWidth) / float(sDefaultLength) > 0.9:
                                        sDefaultDiameter = sDefaultWidth
                                        if not sDefaultHeight is None: sDefaultDepth = sDefaultHeight
                                        sDefaultWidth = None
                                        sDefaultLength = None
                                        sDefaultHeight = None
                            if not sDefaultDiameter is None: sDefaultDiameter  = sDefaultDiameter + " km"
                            if not sDefaultWidth    is None: sDefaultWidth     = sDefaultWidth    + " km"
                            if not sDefaultLength   is None: sDefaultLength    = sDefaultLength   + " km"
                            if not sDefaultHeight   is None: sDefaultHeight    = sDefaultHeight   + " m"
                            if not sDefaultDepth    is None: sDefaultDepth     = sDefaultDepth    + " m"
                            
    return dicInputValues    

def loadJsonInputData(sJsonFilename):
    # get empty dictionary
    dicInputValues = getEmptyDicInput() 

    # Read json file
    if sJsonFilename != "":
        with open(sJsonFilename, 'r') as fp:
            dicJsonValues = json.load(fp)
        # override empty dictionary with json values (so missing fields in old JSon will still be in the dictionary with default values)
        for sKey, aValue in dicJsonValues.iteritems(): 
            dicInputValues[sKey] = aValue
    return dicInputValues
    
    
# Constants
iFinalPictureMarginWidth = 20 # Margin for the final picture         
iMarginPicture = 5            # Margin around the picture, inside the border   
iMarginTopPicture = 20        # Margin above the picture, below the additional header info 
iMarginBottomSubtitle = 10    # Margin below the subtitle, above additional header info 
iMarginBottomPicture = 10     # Margin below the picture, above the logo and data 
iBorderSize = 1               # Border around the picture
iPositionWinjuposX = 200      # position of the Winjupos, from the right edge (+margin)    
iPositionWinjuposY = 100      # position of the Winjupos, from  the border around the picture (+ margin)   
iMainTitleTextInterligne = 13 # interline in pixel between Title and Subtitle rows
iTitleTextInterligne = 5      # interline in pixel between Subtitle rows
iDataSectionInterligne = 7    # additional interline between sections in data text
iDataTextRowHeight = 16       # data info text row height (text + interligne)
iMarginSignature = 5          # Margin for signature related to inside border of picture
fMiniatureHeight = 128.0      # Height of miniature image for Moon
iDataTextDotSize = 3          # Size of the dot on each data text line for Lunar features

DATA_TITLE_EPHEMERIDE = "EPHEMERIDE  "
DATA_TITLE_TELESCOPE  = "MATERIEL  "
DATA_TITLE_CAPTURE    = "CAPTURE  "
DATA_TITLE_PROCESSING = "TRAITEMENT  "
arrMonths = [ "JAN", "FEV", "MAR", "AVR", "MAI", "JUI", "JUL", "AOU", "SEP", "OCT", "NOV", "DEC"]

imgWinjupos = None
imgPicture = None

# read parameters
with open("FormatAstroImages_Settings.json", 'r') as fp:
    dicParameters = json.load(fp)
    
# get inputs from Json file or from keyboard
print ""
print ""
sJsonFilename = getInputValue("Filename", "Name of PJSON parameters file to use", False, ".json")
if sJsonFilename != "":
    dicInputValues = loadJsonInputData(sJsonFilename)
else:
    dicInputValues = readInputsFromKeyboard() 

# Compute output file name
sOutputFileName = dicInputValues["Subject_Type"] + " - " + dicInputValues["TimeLoc_Date"].replace("-","") + dicInputValues["TimeLoc_Time"].replace(":","")
sOutputFileName = sOutputFileName + " - ["
sOutputFileNameTechDetails = ""
if dicInputValues["Hardware_Optic"] != "": 
    if dicInputValues["Hardware_Optic"] in dicParameters["DetailedInfo"]:
        sOutputFileNameTechDetails = sOutputFileNameTechDetails + dicParameters["DetailedInfo"][dicInputValues["Hardware_Optic"]]["ShortName"]
if dicInputValues["Hardware_Camera"] != "": 
    if dicInputValues["Hardware_Camera"] in dicParameters["DetailedInfo"]:
        if sOutputFileNameTechDetails != "": sOutputFileNameTechDetails = sOutputFileNameTechDetails + "-"
        sOutputFileNameTechDetails = sOutputFileNameTechDetails + dicParameters["DetailedInfo"][dicInputValues["Hardware_Camera"]]["ShortName"]
if dicInputValues["Hardware_Barlow"] != "": 
    if ("Barlow " + dicInputValues["Hardware_Barlow"]) in dicParameters["DetailedInfo"]:
        if sOutputFileNameTechDetails != "": sOutputFileNameTechDetails = sOutputFileNameTechDetails + "-"
        sOutputFileNameTechDetails = sOutputFileNameTechDetails + dicParameters["DetailedInfo"][("Barlow " + dicInputValues["Hardware_Barlow"])]["ShortName"]
if dicInputValues["Hardware_ADC"] != "": 
    if ("ADC " + dicInputValues["Hardware_ADC"]) in dicParameters["DetailedInfo"]:
        if sOutputFileNameTechDetails != "": sOutputFileNameTechDetails = sOutputFileNameTechDetails + "-"
        sOutputFileNameTechDetails = sOutputFileNameTechDetails + dicParameters["DetailedInfo"][("ADC " + dicInputValues["Hardware_ADC"])]["ShortName"]
if dicInputValues["Hardware_Reducer"] != "": 
    if dicInputValues["Hardware_Reducer"] in dicParameters["DetailedInfo"]:
        if sOutputFileNameTechDetails != "": sOutputFileNameTechDetails = sOutputFileNameTechDetails + "-"
        sOutputFileNameTechDetails = sOutputFileNameTechDetails + dicParameters["DetailedInfo"][dicInputValues["Hardware_Reducer"]]["ShortName"]
sOutputFileNameTechDetails = sOutputFileNameTechDetails + "]"
sOutputFileName = sOutputFileName + sOutputFileNameTechDetails
sOutputFileName = sOutputFileName + " - " + dicInputValues["Subject_MainTitle"]
if dicInputValues["Subject_Subtitle1"] != "": sOutputFileName = sOutputFileName + " - " + dicInputValues["Subject_Subtitle1"]
if dicInputValues["Subject_Subtitle2"] != "": sOutputFileName = sOutputFileName + " - " + dicInputValues["Subject_Subtitle2"]
if dicInputValues["Subject_Subtitle3"] != "": sOutputFileName = sOutputFileName + " - " + dicInputValues["Subject_Subtitle3"]
print "Output file name computed: " + sOutputFileName
print ""


# Save parameters in JSON file if not a json file in input
if sJsonFilename == "":
    with open(sOutputFileName + '.json', 'w') as fp:
        try:
            json.dump(dicInputValues, fp)
        except:
            pass
            print ""
        print " --> created json file: " + sOutputFileName + ".json"


# init boolean for diffenrent cases        
bIsMoonPicture = (dicInputValues["Subject_Type"] == "Moon")
bIsPlanetPicture = (dicInputValues["Subject_Type"] == "Planet")
bIsDeepSkyPicture = (dicInputValues["Subject_Type"] == "Deep Sky")


# build text to be displayed
sField_Signature = "PhilippeLarosa"
    
sField_Title     = dicInputValues["Subject_MainTitle"]
sField_Subtitle1 = dicInputValues["Subject_Subtitle1"]
sField_Subtitle2 = dicInputValues["Subject_Subtitle2"]
sField_Subtitle3 = dicInputValues["Subject_Subtitle3"]
if bIsMoonPicture:
    sField_Title_Additional_Info = dicInputValues["Info_Additional"]
elif bIsPlanetPicture:
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_Planet_Distance"],  u"Distance ",  u"",    u"", u"")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_Planet_Diameter"],  u"Diamètre ",  u'"',   sField_Title_Additional_Info, u"   -   ")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_Planet_Magnitude"], u"Magnitude ", u"",    sField_Title_Additional_Info, u"   -   ")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_Planet_Altitude"],  u"Altitude ",  u"deg", sField_Title_Additional_Info, u"   -   ")    
elif bIsDeepSkyPicture:
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_DeepSky_Type"],  u"",  u"",    u"", u"")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_DeepSky_Distance"],    u"Distance ",  u"",    sField_Title_Additional_Info, u"   -   ")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_DeepSky_Diameter"],    u"Diamètre ",  u"",    sField_Title_Additional_Info, u"   -   ")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_DeepSky_Magnitude"],   u"Magnitude ", u"",    sField_Title_Additional_Info, u"   -   ")
    sField_Title_Additional_Info = addInfoToString(dicInputValues["Info_DeepSky_Altitude"],    u"Altitude ",  u"deg", sField_Title_Additional_Info, u"   -   ")

sField_MoonEphem_Title = DATA_TITLE_EPHEMERIDE
sField_Data_Ephemeride_TimeLocation = str(dicInputValues["TimeLoc_Date"][8:]) + " "
sField_Data_Ephemeride_TimeLocation = sField_Data_Ephemeride_TimeLocation + arrMonths[int(dicInputValues["TimeLoc_Date"][5:7]) - 1] + " "
sField_Data_Ephemeride_TimeLocation = sField_Data_Ephemeride_TimeLocation + str(dicInputValues["TimeLoc_Date"][0:4]) + "  "
sField_Data_Ephemeride_TimeLocation = sField_Data_Ephemeride_TimeLocation + str(dicInputValues["TimeLoc_Time"][0:2]) + ":" + str(dicInputValues["TimeLoc_Time"][3:])
sField_Data_Ephemeride_TimeLocation = sField_Data_Ephemeride_TimeLocation + " GMT"
sField_Data_Ephemeride_TimeLocation = sField_Data_Ephemeride_TimeLocation + " - " 
sField_Data_Ephemeride_TimeLocation = sField_Data_Ephemeride_TimeLocation + dicInputValues["TimeLoc_Location"]
sField_Data_Ephemeride_Moon = addInfoToString(dicInputValues["Info_MoonAge"],           u"Lune: âge ",   u"",  u"", u"")
sField_Data_Ephemeride_Moon = addInfoToString(dicInputValues["Info_MoonIllumination"],  u"Illum. ",      u"%", sField_Data_Ephemeride_Moon, u" - ")
sField_Data_Ephemeride_Moon = addInfoToString(dicInputValues["Info_MoonColongitude"],   u"Colong. ",     u"",  sField_Data_Ephemeride_Moon, u" - ")
sField_Data_Ephemeride_Moon = addInfoToString(dicInputValues["Info_MoonPositionAngle"], u"Pos. angle. ", u"",  sField_Data_Ephemeride_Moon, u" - ")

sField_Hardware_Title = DATA_TITLE_TELESCOPE
sField_Data_Hardware_Optic_Mount       = addInfoToString(dicInputValues["Hardware_Optic"],           "",          "", "", "")
sField_Data_Hardware_Optic_Mount       = addInfoToString(dicInputValues["Hardware_Mount"],           "",          "", sField_Data_Hardware_Optic_Mount, " - ")
sField_Data_Hardware_Optic_Accessories = addInfoToString(dicInputValues["Hardware_ADC"],             "ADC: ",     "", "", "")
sField_Data_Hardware_Optic_Accessories = addInfoToString(dicInputValues["Hardware_Reducer"],         "",          "", sField_Data_Hardware_Optic_Accessories, " - ")
sField_Data_Hardware_Optic_Accessories = addInfoToString(dicInputValues["Hardware_Barlow"],          "Barlow ",   "", sField_Data_Hardware_Optic_Accessories, " - ")
sField_Data_Hardware_Optic_Accessories = addInfoToString(dicInputValues["Hardware_Filter"],          "Filtre ",   "", sField_Data_Hardware_Optic_Accessories, " - ")
sField_Data_Hardware_Camera            = addInfoToString(dicInputValues["Hardware_Camera"],          "Capteur: ", "", "", "")
sField_Hardware_AdditionalInfo         = addInfoToString(dicInputValues["Hardware_Additional_Info"], "",          "", "", "")

sField_Data_Capture_Title = DATA_TITLE_CAPTURE
sField_Data_Capture = addInfoToString(dicInputValues["Capture_Software"],      "", "",   "", "")
sField_Data_Capture = addInfoToString(dicInputValues["Capture_Bin"],           "bin ",   "",      sField_Data_Capture, " - ")
sField_Data_Capture = addInfoToString(dicInputValues["Capture_Bits"],          "",       " bits", sField_Data_Capture, " / ")
sField_Data_Capture = addInfoToString(dicInputValues["Capture_Gain"],          "Gain ",  "",      sField_Data_Capture, " / ")
sField_Data_Capture = addInfoToString(dicInputValues["Capture_Exposition"],    "Exp. ",  "",      sField_Data_Capture, " / ")
sField_Data_Capture = addInfoToString(dicInputValues["Capture_Rate"],          "",       " fps",  sField_Data_Capture, " / ")
sField_Data_Capture = addInfoToString(dicInputValues["Capture_TotalExposure"], "Total ", "",      sField_Data_Capture, " - ")

sField_Data_Processing_Title = DATA_TITLE_PROCESSING
sField_Data_Process_Preprocessing  = addInfoToString(dicInputValues["Processing_Pre-processingSoftware"], "", "", "", "")
sField_Data_Process_Stacking       = addInfoToString(dicInputValues["Processing_StackingSoftware"],       "", "", "", "")
sField_Data_Process_Stacking       = addInfoToString(dicInputValues["Processing_ImagesProcessed"],        "", "", sField_Data_Process_Stacking, " - ")
sField_Data_Process_Processing     = addInfoToString(dicInputValues["Processing_ProcessingSoftware"],     "", "", "", "")
sField_Data_Process_Rendering      = addInfoToString(dicInputValues["Processing_RenderingSoftware"],      "", "", "", "")
sField_Data_Process_AdditionalInfo = addInfoToString(dicInputValues["Processing_AdditionalInfo"],         "", "", "", "")

sField_Data_MoonFeature_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_1, "   ")
sField_Data_MoonFeature_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Width"],    "Larg. ", "",   sField_Data_MoonFeature_1, "   ")
sField_Data_MoonFeature_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Length"],   "Long. ", "",   sField_Data_MoonFeature_1, "   ")
sField_Data_MoonFeature_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_1, "   ")
sField_Data_MoonFeature_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Height"],   "Haut. ", "",   sField_Data_MoonFeature_1, "   ")
sField_Data_MoonFeature_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_2, "   ")
sField_Data_MoonFeature_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Width"],    "Larg. ", "",   sField_Data_MoonFeature_2, "   ")
sField_Data_MoonFeature_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Length"],   "Long. ", "",   sField_Data_MoonFeature_2, "   ")
sField_Data_MoonFeature_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_2, "   ")
sField_Data_MoonFeature_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Height"],   "Haut. ", "",   sField_Data_MoonFeature_2, "   ")
sField_Data_MoonFeature_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_3, "   ")
sField_Data_MoonFeature_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Width"],    "Larg. ", "",   sField_Data_MoonFeature_3, "   ")
sField_Data_MoonFeature_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Length"],   "Long. ", "",   sField_Data_MoonFeature_3, "   ")
sField_Data_MoonFeature_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_3, "   ")
sField_Data_MoonFeature_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Height"],   "Haut. ", "",   sField_Data_MoonFeature_3, "   ")
sField_Data_MoonFeature_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_4, "   ")
sField_Data_MoonFeature_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Width"],    "Larg. ", "",   sField_Data_MoonFeature_4, "   ")
sField_Data_MoonFeature_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Length"],   "Long. ", "",   sField_Data_MoonFeature_4, "   ")
sField_Data_MoonFeature_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_4, "   ")
sField_Data_MoonFeature_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Height"],   "Haut. ", "",   sField_Data_MoonFeature_4, "   ")
sField_Data_MoonFeature_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_5, "   ")
sField_Data_MoonFeature_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Width"],    "Larg. ", "",   sField_Data_MoonFeature_5, "   ")
sField_Data_MoonFeature_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Length"],   "Long. ", "",   sField_Data_MoonFeature_5, "   ")
sField_Data_MoonFeature_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_5, "   ")
sField_Data_MoonFeature_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Height"],   "Haut. ", "",   sField_Data_MoonFeature_5, "   ")
sField_Data_MoonFeature_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_6, "   ")
sField_Data_MoonFeature_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Width"],    "Larg. ", "",   sField_Data_MoonFeature_6, "   ")
sField_Data_MoonFeature_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Length"],   "Long. ", "",   sField_Data_MoonFeature_6, "   ")
sField_Data_MoonFeature_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_6, "   ")
sField_Data_MoonFeature_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Height"],   "Haut. ", "",   sField_Data_MoonFeature_6, "   ")
sField_Data_MoonFeature_7 = addInfoToString(dicInputValues["Info_MoonFeature6_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_7 = addInfoToString(dicInputValues["Info_MoonFeature6_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_7, "   ")
sField_Data_MoonFeature_7 = addInfoToString(dicInputValues["Info_MoonFeature6_Width"],    "Larg. ", "",   sField_Data_MoonFeature_7, "   ")
sField_Data_MoonFeature_7 = addInfoToString(dicInputValues["Info_MoonFeature6_Length"],   "Long. ", "",   sField_Data_MoonFeature_7, "   ")
sField_Data_MoonFeature_7 = addInfoToString(dicInputValues["Info_MoonFeature6_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_7, "   ")
sField_Data_MoonFeature_7 = addInfoToString(dicInputValues["Info_MoonFeature6_Height"],   "Haut. ", "",   sField_Data_MoonFeature_7, "   ")
sField_Data_MoonFeature_8 = addInfoToString(dicInputValues["Info_MoonFeature7_Name"],      "",      "  ", "", "")
sField_Data_MoonFeature_8 = addInfoToString(dicInputValues["Info_MoonFeature7_Diameter"], "Diam. ", "",   sField_Data_MoonFeature_8, "   ")
sField_Data_MoonFeature_8 = addInfoToString(dicInputValues["Info_MoonFeature7_Width"],    "Larg. ", "",   sField_Data_MoonFeature_8, "   ")
sField_Data_MoonFeature_8 = addInfoToString(dicInputValues["Info_MoonFeature7_Length"],   "Long. ", "",   sField_Data_MoonFeature_8, "   ")
sField_Data_MoonFeature_8 = addInfoToString(dicInputValues["Info_MoonFeature7_Depth"],    "Prof. ", "",   sField_Data_MoonFeature_8, "   ")
sField_Data_MoonFeature_8 = addInfoToString(dicInputValues["Info_MoonFeature7_Height"],   "Haut. ", "",   sField_Data_MoonFeature_8, "   ")

# Compute Rows Content
sRow_Header_Main_1 = sField_Title
sRow_Header_Subtitle_1 = sField_Subtitle1
sRow_Header_Subtitle_2 = sField_Subtitle2
sRow_Header_Subtitle_3 = sField_Subtitle3
sRow_Header_Additional = sField_Title_Additional_Info

sRow_Data_Ephem_1 = sField_Data_Ephemeride_TimeLocation
sRow_Data_Ephem_2 = sField_Data_Ephemeride_Moon

sRow_Data_Hardware_1 = sField_Data_Hardware_Optic_Mount
sRow_Data_Hardware_2 = sField_Data_Hardware_Optic_Accessories
sRow_Data_Hardware_3 = sField_Data_Hardware_Camera
sRow_Data_Hardware_4 = sField_Hardware_AdditionalInfo
if sRow_Data_Hardware_3 == "":
    sRow_Data_Hardware_3 = sRow_Data_Hardware_4
    sRow_Data_Hardware_4 = ""
if sRow_Data_Hardware_2 == "":
    sRow_Data_Hardware_2 = sRow_Data_Hardware_3
    sRow_Data_Hardware_3 = sRow_Data_Hardware_4
    sRow_Data_Hardware_4 = ""
if sRow_Data_Hardware_1 == "":
    sRow_Data_Hardware_1 = sRow_Data_Hardware_2
    sRow_Data_Hardware_2 = sRow_Data_Hardware_3
    sRow_Data_Hardware_3 = sRow_Data_Hardware_4
    sRow_Data_Hardware_4 = ""

sRow_Data_Capture = sField_Data_Capture

sRow_data_Process_1 = sField_Data_Process_Preprocessing
sRow_data_Process_2 = sField_Data_Process_Stacking
sRow_data_Process_3 = sField_Data_Process_Processing
sRow_data_Process_4 = sField_Data_Process_Rendering
sRow_data_Process_5 = sField_Data_Process_AdditionalInfo
if sRow_data_Process_4 == "":
    sRow_data_Process_4 = sRow_data_Process_5
    sRow_data_Process_5 = ""
if sRow_data_Process_3 == "":
    sRow_data_Process_3 = sRow_data_Process_4
    sRow_data_Process_4 = sRow_data_Process_5
    sRow_data_Process_5 = ""
if sRow_data_Process_2 == "":
    sRow_data_Process_2 = sRow_data_Process_3
    sRow_data_Process_3 = sRow_data_Process_4
    sRow_data_Process_4 = sRow_data_Process_5
    sRow_data_Process_5 = ""
if sRow_data_Process_1 == "":
    sRow_data_Process_1 = sRow_data_Process_2
    sRow_data_Process_2 = sRow_data_Process_3
    sRow_data_Process_3 = sRow_data_Process_4
    sRow_data_Process_4 = sRow_data_Process_5
    sRow_data_Process_5 = ""


# Display Rows
print ""
print ""
print "   ROWS"
print "   ------"
print ""
print "     Header Row 1:          " + sRow_Header_Main_1
print "     Header Row 2:          " + sRow_Header_Subtitle_1
print "     Header Row 3:          " + sRow_Header_Subtitle_2
print "     Header Row 4:          " + sRow_Header_Subtitle_3
print "     Header Row 5:          " + sRow_Header_Additional
print ""
print "     Data Row 1:            " + (sField_MoonEphem_Title + "              ")[0:15] + sRow_Data_Ephem_1
print "     Data Row 2:            " + "               " + sRow_Data_Ephem_2
print "     Data Row 3:            " + (sField_Hardware_Title + "              ")[0:15] + sRow_Data_Hardware_1
print "     Data Row 4:            " + "               " + sRow_Data_Hardware_2
print "     Data Row 5:            " + "               " + sRow_Data_Hardware_3
print "     Data Row 6:            " + "               " + sRow_Data_Hardware_4
print "     Data Row 7:            " + (sField_Data_Capture_Title + "              ")[0:15] + sRow_Data_Capture
print "     Data Row 8:            " + (sField_Data_Processing_Title + "              ")[0:15] + sRow_data_Process_1
print "     Data Row 9:            " + "               " + sRow_data_Process_2
print "     Data Row 10:           " + "               " + sRow_data_Process_3
print "     Data Row 11:           " + "               " + sRow_data_Process_4
print "     Data Row 12:           " + "               " + sRow_data_Process_5
print ""
print "     Moon Feature Row 1:    " + sField_Data_MoonFeature_1
print "     Moon Feature Row 2:    " + sField_Data_MoonFeature_2
print "     Moon Feature Row 3:    " + sField_Data_MoonFeature_3
print "     Moon Feature Row 4:    " + sField_Data_MoonFeature_4
print "     Moon Feature Row 5:    " + sField_Data_MoonFeature_5
print "     Moon Feature Row 6:    " + sField_Data_MoonFeature_6
print "     Moon Feature Row 7:    " + sField_Data_MoonFeature_7
print "     Moon Feature Row 8:    " + sField_Data_MoonFeature_8
print ""
print ""

    
    
#Ready to process
print ""
sOk = getInputValue("Parameter", "Ok to proceed ? ", "CommonValues/YesNo", None)
if sOk == "No":
    print ""
    print "Aborted."
    print ""
else:
    print ""
    print "Processing..."
    print ""
    
    # Set colors
    theColorTitle           = (255,255,255)
    theColorSubTitle        = (180,180,180)
    theColorHeaderAddinfo   = (127,127,127)
    theColorDataText        = (96,96,96)
    theColorDataTitle       = (176,176,176)
    if bIsMoonPicture:
        theColorSignature   = (228,228,228,255) # if moon. border and signature more bright
    else:
        theColorSignature   = (128,128,128,255)
    theColorSignatureShadow = (32,32,32)
    
    # Set fonts
    theGeoDataFont                 = ImageFont.truetype("PCNavita-Regular.ttf", 14)
    theInfoDataFont                = ImageFont.truetype("PCNavita-Regular.ttf", 12)
    theTitleFont                   = ImageFont.truetype("georgia.ttf",         36)
    theSubTitleFont                = ImageFont.truetype("georgiai.ttf",         20)
    theSubHeaderAdditionalInfoFont = ImageFont.truetype("georgiai.ttf",         16)
    theSignatureFont               = ImageFont.truetype("Sugar Candy.ttf",      18)
        
    # get Winjupos size
    print ""
    if dicInputValues["Bitmap_WinjuposFileName"] != "":
        imgWinjupos = Image.open(dicInputValues["Bitmap_WinjuposFileName"])
        iWinjuposWidth, iWinjuposHeight = imgWinjupos.size
        print "   --> Winjupos size: " + str(iWinjuposWidth) + " x " + str(iWinjuposHeight)
        if iWinjuposHeight != 128:
            # Resize to 128 pixel height maxi
            fCoeff =  128.0 / float(iWinjuposHeight)
            iWinjuposWidth = int(float(iWinjuposWidth) * fCoeff)
            iWinjuposHeight = int(float(iWinjuposHeight) * fCoeff)
            imgWinjupos.thumbnail((iWinjuposWidth, iWinjuposHeight), Image.ANTIALIAS)
            print "   --> Winjupos resized to: " + str(iWinjuposWidth) + " x " + str(iWinjuposHeight)

    # get picture size
    imgPicture = Image.open(dicInputValues["Bitmap_PictureFileName"])
    iPictureWidth, iPictureHeight = imgPicture.size
    iPictureWidthAdjustBorder = 0
    print "   --> Picture size: " + str(iPictureWidth) + " x " + str(iPictureHeight)
    print ""

    if bIsMoonPicture:
        if dicInputValues["Info_MoonFeature0_Name"] != "":
            imgMiniature = Image.open(dicInputValues["Bitmap_PictureFileName"])
            iMiniatureWidth, iMiniatureHeight = imgMiniature.size
            fCoeff = fMiniatureHeight / float(iMiniatureHeight)
            iMiniatureWidth = int(float(iMiniatureWidth) * fCoeff)
            iMiniatureHeight = int(float(iMiniatureHeight) * fCoeff)
            imgMiniature.thumbnail((iMiniatureWidth, iMiniatureHeight), Image.ANTIALIAS)
    
    # create temporary bitmap (for computing text size)
    theTempImg = Image.new( 'RGBA', (1920, 100), (0, 0, 0, 255))
    theTempDraw = ImageDraw.Draw(theTempImg)
    
    
    
    
    #=========================================================================================
    #
    # compute main sections size and position
    #
    #    Header
    #    Picture with Frame and Signature
    #    Footer
    #=========================================================================================
    iHeaderHeight = theTempDraw.textsize(sRow_Header_Main_1, font=theTitleFont)[1]
    if sRow_Header_Subtitle_1 != "": iHeaderHeight = iHeaderHeight + iMainTitleTextInterligne + theTempDraw.textsize(sRow_Header_Subtitle_1, font=theSubTitleFont)[1]
    if sRow_Header_Subtitle_2 != "": iHeaderHeight = iHeaderHeight + iTitleTextInterligne + theTempDraw.textsize(sRow_Header_Subtitle_2, font=theSubTitleFont)[1]
    if sRow_Header_Subtitle_3 != "": iHeaderHeight = iHeaderHeight + iTitleTextInterligne + theTempDraw.textsize(sRow_Header_Subtitle_3, font=theSubTitleFont)[1]
    if sRow_Header_Additional != "": iHeaderHeight = iHeaderHeight + iMarginBottomSubtitle + theTempDraw.textsize(sRow_Header_Additional, font=theSubHeaderAdditionalInfoFont)[1]
    if bIsMoonPicture and dicInputValues["Bitmap_WinjuposFileName"] != "" and iHeaderHeight < iWinjuposHeight: iHeaderHeight = iWinjuposHeight

    iDataFooterLeftHeight = 0
    if sRow_Data_Ephem_1    != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_Data_Ephem_2    != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_Data_Hardware_1 != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataSectionInterligne + iDataTextRowHeight
    if sRow_Data_Hardware_2 != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_Data_Hardware_3 != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_Data_Hardware_4 != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_Data_Capture    != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataSectionInterligne + iDataTextRowHeight
    if sRow_data_Process_1  != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataSectionInterligne + iDataTextRowHeight
    if sRow_data_Process_2  != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_data_Process_3  != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_data_Process_4  != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight
    if sRow_data_Process_5  != "": iDataFooterLeftHeight = iDataFooterLeftHeight + iDataTextRowHeight

    if sField_Data_MoonFeature_1 != "": 
        iDataFooterRightHeight = theTempDraw.textsize(sField_Data_MoonFeature_1, font=theInfoDataFont)[1]
        iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_1, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_2 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_2, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_2, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_3 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_3, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_3, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_4 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_4, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_4, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_5 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_5, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_5, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_6 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_6, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_6, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_7 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_7, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_7, font=theInfoDataFont)[0]
        if sField_Data_MoonFeature_8 != "":
            iDataFooterRightHeight = iDataFooterRightHeight + iDataTextRowHeight
            if iDataFooterRightWidth < theTempDraw.textsize(sField_Data_MoonFeature_8, font=theInfoDataFont)[0]: iDataFooterRightWidth = theTempDraw.textsize(sField_Data_MoonFeature_8, font=theInfoDataFont)[0]
        if iDataFooterRightHeight < int(fMiniatureHeight): iDataFooterRightHeight = int(fMiniatureHeight)
    else:
        iDataFooterRightHeight = 0
    
    if iDataFooterLeftHeight > iDataFooterRightHeight:
        iFooterHeight = iDataFooterLeftHeight
    else:
        iFooterHeight = iDataFooterRightHeight
   
    iPictureWithFrameAndSignatureHeight = iBorderSize + iMarginPicture + iPictureHeight + iMarginPicture + iBorderSize + theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] - iMarginSignature
    iPositionTopFooter = iFinalPictureMarginWidth + iHeaderHeight + iMarginTopPicture + iPictureWithFrameAndSignatureHeight + iMarginBottomPicture
    
    
    
    
    #=========================================================================================
    #
    # Compute Objects position and size
    #
    #=========================================================================================
    # Final image
    iFinalImageWidth = iFinalPictureMarginWidth + iBorderSize + iMarginPicture + iPictureWidth + iMarginPicture + iBorderSize + iFinalPictureMarginWidth
    iFinalImageHeight = iFinalPictureMarginWidth + iHeaderHeight + iMarginTopPicture + iPictureWithFrameAndSignatureHeight + iMarginBottomPicture + iFooterHeight + iFinalPictureMarginWidth
    
    # Winjupos miniature
    if dicInputValues["Bitmap_WinjuposFileName"] != "":
        if bIsMoonPicture:
            iWinjupos_X = iFinalImageWidth - iFinalPictureMarginWidth - iWinjuposWidth
            iWinjupos_Y = iFinalPictureMarginWidth
        if bIsPlanetPicture:
            iWinjupos_X = iFinalImageWidth - iFinalPictureMarginWidth - iWinjuposWidth
            iWinjupos_Y = iPositionTopFooter
    else:
        iWinjuposHeight = 0

    # Image miniature if moon features displayed    
    if bIsMoonPicture and sField_Data_MoonFeature_1 != "":
        iMiniature_X = iFinalImageWidth - iFinalPictureMarginWidth - iDataFooterRightWidth - iFinalPictureMarginWidth - iMiniatureWidth
        iMiniature_Y = iPositionTopFooter

    # Picture and Frame
    iPicture_X = iFinalPictureMarginWidth + iBorderSize + iMarginPicture
    iPicture_Y = iFinalPictureMarginWidth + iHeaderHeight + iMarginTopPicture + iBorderSize + iMarginPicture
    
    iPictureFrame_X = iFinalPictureMarginWidth
    iPictureFrame_Y = iFinalPictureMarginWidth + iHeaderHeight + iMarginTopPicture
    iPictureFrame_Width = iBorderSize + iMarginPicture + iPictureWidth + iMarginPicture + iBorderSize 
    iPictureFrame_Height = iBorderSize + iMarginPicture + iPictureHeight + iMarginPicture + iBorderSize 
    
    # Signature
    iField_Signature_X = iPicture_X + iPictureWidth - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[0] - iMarginSignature
    iField_Signature_Y = iPicture_Y + iPictureHeight + iMarginPicture - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] / 3
    
    # Header
    iTitleMain_X = iFinalPictureMarginWidth
    iTitleMain_Y = iFinalPictureMarginWidth
    if sRow_Header_Subtitle_1 != "":
        iSubtitle_1_X = iFinalPictureMarginWidth
        iSubtitle_1_Y = iTitleMain_Y + theTempDraw.textsize(sRow_Header_Main_1, font=theTitleFont)[1] + iMainTitleTextInterligne
    if sRow_Header_Subtitle_2 != "":
        iSubtitle_2_X = iFinalPictureMarginWidth
        iSubtitle_2_Y = iSubtitle_1_Y + theTempDraw.textsize(sRow_Header_Subtitle_1, font=theSubTitleFont)[1] + iTitleTextInterligne
    if sRow_Header_Subtitle_3 != "":
        iSubtitle_3_X = iFinalPictureMarginWidth
        iSubtitle_3_Y = iSubtitle_2_Y + theTempDraw.textsize(sRow_Header_Subtitle_2, font=theSubTitleFont)[1] + iTitleTextInterligne
    if sRow_Header_Additional != "":
        iHeader_Additional_X = iFinalPictureMarginWidth
        iHeader_Additional_Y = iPictureFrame_Y - iMarginBottomSubtitle - theTempDraw.textsize(sRow_Header_Additional, font=theSubHeaderAdditionalInfoFont)[1]
    
    # Footer Left
    iDataTitle_Width = theTempDraw.textsize(sField_MoonEphem_Title, font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Hardware_Title,        font=theInfoDataFont)[0] > iDataTitle_Width: iDataTitle_Width = theTempDraw.textsize(sField_Hardware_Title,        font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Data_Capture_Title,    font=theInfoDataFont)[0] > iDataTitle_Width: iDataTitle_Width = theTempDraw.textsize(sField_Data_Capture_Title,    font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Data_Processing_Title, font=theInfoDataFont)[0] > iDataTitle_Width: iDataTitle_Width = theTempDraw.textsize(sField_Data_Processing_Title, font=theInfoDataFont)[0]
    iDataTitle_Width = iDataTitle_Width + 5

    
    iPosY_NextRow = iPositionTopFooter
    if sRow_Data_Ephem_1 != "":
        sRow_Data_Ephem_Title_X = iFinalPictureMarginWidth
        sRow_Data_Ephem_1_X = sRow_Data_Ephem_Title_X + iDataTitle_Width
        sRow_Data_Ephem_1_Y = iPosY_NextRow
        iPosY_NextRow = sRow_Data_Ephem_1_Y + iDataTextRowHeight
    if sRow_Data_Ephem_2 != "":
        sRow_Data_Ephem_2_X = iFinalPictureMarginWidth + iDataTitle_Width
        sRow_Data_Ephem_2_Y = iPosY_NextRow
        iPosY_NextRow = sRow_Data_Ephem_2_Y + iDataTextRowHeight
    if sRow_Data_Hardware_1 != "":
        sRow_Data_Hardware_Title_X = iFinalPictureMarginWidth
        sRow_Data_Hardware_1_X = sRow_Data_Hardware_Title_X + iDataTitle_Width
        sRow_Data_Hardware_1_Y = iPosY_NextRow + iDataSectionInterligne
        iPosY_NextRow = sRow_Data_Hardware_1_Y + iDataTextRowHeight
    if sRow_Data_Hardware_2 != "":
        sRow_Data_Hardware_2_X = sRow_Data_Hardware_Title_X + iDataTitle_Width
        sRow_Data_Hardware_2_Y = iPosY_NextRow
        iPosY_NextRow = sRow_Data_Hardware_2_Y + iDataTextRowHeight
    if sRow_Data_Hardware_3 != "":
        sRow_Data_Hardware_3_X = sRow_Data_Hardware_Title_X + iDataTitle_Width
        sRow_Data_Hardware_3_Y = iPosY_NextRow
        iPosY_NextRow = sRow_Data_Hardware_3_Y + iDataTextRowHeight
    if sRow_Data_Hardware_4 != "":
        sRow_Data_Hardware_4_X = sRow_Data_Hardware_Title_X + iDataTitle_Width
        sRow_Data_Hardware_4_Y = iPosY_NextRow
        iPosY_NextRow = sRow_Data_Hardware_4_Y + iDataTextRowHeight
    if sRow_Data_Capture != "":
        sRow_Data_Capture_Title_X = iFinalPictureMarginWidth
        sRow_Data_Capture_X = sRow_Data_Capture_Title_X + iDataTitle_Width
        sRow_Data_Capture_Y = iPosY_NextRow + iDataSectionInterligne
        iPosY_NextRow = sRow_Data_Capture_Y + iDataTextRowHeight
    if sRow_data_Process_1 != "":
        sRow_data_Process_Title_X = iFinalPictureMarginWidth
        sRow_data_Process_1_X = sRow_data_Process_Title_X + iDataTitle_Width
        sRow_data_Process_1_Y = iPosY_NextRow + iDataSectionInterligne
        iPosY_NextRow = sRow_data_Process_1_Y + iDataTextRowHeight
    if sRow_data_Process_2 != "":
        sRow_data_Process_2_X = sRow_data_Process_Title_X + iDataTitle_Width
        sRow_data_Process_2_Y = iPosY_NextRow
        iPosY_NextRow = sRow_data_Process_2_Y + iDataTextRowHeight
    if sRow_data_Process_3 != "":
        sRow_data_Process_3_X = sRow_data_Process_Title_X + iDataTitle_Width
        sRow_data_Process_3_Y = iPosY_NextRow
        iPosY_NextRow = sRow_data_Process_3_Y + iDataTextRowHeight
    if sRow_data_Process_4 != "":
        sRow_data_Process_4_X = sRow_data_Process_Title_X + iDataTitle_Width
        sRow_data_Process_4_Y = iPosY_NextRow
        iPosY_NextRow = sRow_data_Process_4_Y + iDataTextRowHeight
    if sRow_data_Process_5 != "":
        sRow_data_Process_5_X = sRow_data_Process_Title_X + iDataTitle_Width
        sRow_data_Process_5_Y = iPosY_NextRow
        iPosY_NextRow = sRow_data_Process_5_Y + iDataTextRowHeight
    
    # Footer Right
    if bIsMoonPicture and sField_Data_MoonFeature_1 != "":
        iPosY_NextRow = iPositionTopFooter
        sField_Data_MoonFeature_1_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
        sField_Data_MoonFeature_1_Y = iPosY_NextRow
        iPosY_NextRow = sField_Data_MoonFeature_1_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_2 != "":
            sField_Data_MoonFeature_2_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_2_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_2_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_3 != "":
            sField_Data_MoonFeature_3_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_3_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_3_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_4 != "":
            sField_Data_MoonFeature_4_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_4_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_4_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_5 != "":
            sField_Data_MoonFeature_5_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_5_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_5_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_6 != "":
            sField_Data_MoonFeature_6_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_6_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_6_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_7 != "":
            sField_Data_MoonFeature_7_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_7_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_7_Y + iDataTextRowHeight
        if sField_Data_MoonFeature_8 != "":
            sField_Data_MoonFeature_8_X = iMiniature_X + iMiniatureWidth + iFinalPictureMarginWidth
            sField_Data_MoonFeature_8_Y = iPosY_NextRow
            iPosY_NextRow = sField_Data_MoonFeature_8_Y + iDataTextRowHeight
    
    
    #=========================================================================================
    #
    # Draw Objects
    #
    #=========================================================================================
    # create new bitmap
    theFinalImg = Image.new( 'RGBA', (iFinalImageWidth, iFinalImageHeight), (0, 0, 0, 255))
    theFinalDraw = ImageDraw.Draw(theFinalImg)
    
    # paste Winjupos             
    if dicInputValues["Bitmap_WinjuposFileName"] != "":
        # # if moon picture, add marker on winjupos image for features location
        if bIsMoonPicture:
            if dicInputValues["Info_MoonFeature0_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature0_Longitude"], dicInputValues["Info_MoonFeature0_Latitude"], eval(dicParameters["CommonValues"]["Feature0_Color"]))
            if dicInputValues["Info_MoonFeature1_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature1_Longitude"], dicInputValues["Info_MoonFeature1_Latitude"], eval(dicParameters["CommonValues"]["Feature1_Color"]))
            if dicInputValues["Info_MoonFeature2_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature2_Longitude"], dicInputValues["Info_MoonFeature2_Latitude"], eval(dicParameters["CommonValues"]["Feature2_Color"]))
            if dicInputValues["Info_MoonFeature3_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature3_Longitude"], dicInputValues["Info_MoonFeature3_Latitude"], eval(dicParameters["CommonValues"]["Feature3_Color"]))
            if dicInputValues["Info_MoonFeature4_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature4_Longitude"], dicInputValues["Info_MoonFeature4_Latitude"], eval(dicParameters["CommonValues"]["Feature4_Color"]))
            if dicInputValues["Info_MoonFeature5_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature5_Longitude"], dicInputValues["Info_MoonFeature5_Latitude"], eval(dicParameters["CommonValues"]["Feature5_Color"]))
            if dicInputValues["Info_MoonFeature6_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature6_Longitude"], dicInputValues["Info_MoonFeature6_Latitude"], eval(dicParameters["CommonValues"]["Feature6_Color"]))
            if dicInputValues["Info_MoonFeature7_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature7_Longitude"], dicInputValues["Info_MoonFeature7_Latitude"], eval(dicParameters["CommonValues"]["Feature7_Color"]))
        theFinalImg.paste(imgWinjupos, (iWinjupos_X, iWinjupos_Y))

    # Paste Picture
    #    Draw border around the picture
    theFinalDraw.rectangle((iPictureFrame_X, iPictureFrame_Y, iPictureFrame_X + iPictureFrame_Width , iPictureFrame_Y + iPictureFrame_Height), outline=theColorSignature, fill=(0, 0, 0, 255))
    theFinalDraw.rectangle((iField_Signature_X - 10, iField_Signature_Y - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] , iField_Signature_X + theTempDraw.textsize(sField_Signature, font=theSignatureFont)[0], iField_Signature_Y + theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] ), outline=(0, 0, 0, 255), fill=(0, 0, 0, 255))
    #   paste picture
    theFinalImg.paste(imgPicture, (iPicture_X, iPicture_Y ))
    #   Signature
    theFinalDraw.text((iField_Signature_X,     iField_Signature_Y),     sField_Signature, theColorSignatureShadow, font=theSignatureFont)
    theFinalDraw.text((iField_Signature_X - 1, iField_Signature_Y - 1), sField_Signature, theColorSignatureShadow, font=theSignatureFont)
    theFinalDraw.text((iField_Signature_X - 2, iField_Signature_Y - 2), sField_Signature, theColorSignature,       font=theSignatureFont)

    # Paste Image miniature if moon features displayed
    if bIsMoonPicture and sField_Data_MoonFeature_1 != "":
        theFinalImg.paste(imgMiniature, (iMiniature_X , iMiniature_Y  ))
        theFinalDraw.rectangle((iMiniature_X - 1, iMiniature_Y - 1, iMiniature_X + iMiniatureWidth, iMiniature_Y + iMiniatureHeight - 1), outline=theColorDataTitle)
    
    # Draw line after main title
    iY = iTitleMain_Y + theTempDraw.textsize(sRow_Header_Main_1, font=theTitleFont)[1] + 8
    iXMin = iTitleMain_X #+ 3 + theTempDraw.textsize(sRow_Header_Main_1, font=theTitleFont)[0]
    if bIsMoonPicture:
        iXMax = iFinalImageWidth - iFinalPictureMarginWidth - 3 - iWinjuposWidth
    else:
        iXMax = iFinalImageWidth - iFinalPictureMarginWidth
    iColorMax = 36
    for iY in range(iTitleMain_Y + 3, iTitleMain_Y + theTempDraw.textsize(sRow_Header_Main_1, font=theTitleFont)[1] + 9):
        if iColorMax == 36:
            iColorMax = 48
        else:
            iColorMax = 36
        for iX in range (iXMin,  iXMax):
            if (iXMax - iX) > iColorMax:
                iColor = iColorMax
            else:
                iColor = (iXMax - iX)
            theFinalDraw.ellipse( (iX, iY, iX, iY), fill=(iColor, iColor, iColor), outline=(iColor, iColor, iColor) )
    # Header
    for j in range(1, 5):
        theFinalDraw.text((iTitleMain_X + 3 + j, iTitleMain_Y + j), sRow_Header_Main_1, (0, 0, 0),     font=theTitleFont)
    theFinalDraw.text((iTitleMain_X + 3,     iTitleMain_Y),     sRow_Header_Main_1, theColorTitle, font=theTitleFont)
    # Draw subtitles
    if sRow_Header_Subtitle_1 != "": theFinalDraw.text((iSubtitle_1_X, iSubtitle_1_Y), sRow_Header_Subtitle_1, theColorSubTitle, font=theSubTitleFont)
    if sRow_Header_Subtitle_2 != "": theFinalDraw.text((iSubtitle_2_X, iSubtitle_2_Y), sRow_Header_Subtitle_2, theColorSubTitle, font=theSubTitleFont)
    if sRow_Header_Subtitle_3 != "": theFinalDraw.text((iSubtitle_3_X, iSubtitle_3_Y), sRow_Header_Subtitle_3, theColorSubTitle, font=theSubTitleFont)
    if sRow_Header_Additional != "": theFinalDraw.text((iHeader_Additional_X, iHeader_Additional_Y), sRow_Header_Additional, theColorHeaderAddinfo, font=theSubHeaderAdditionalInfoFont)
        
    # Footer Left
    if sRow_Data_Ephem_1 != "": 
        theFinalDraw.text((sRow_Data_Ephem_Title_X, sRow_Data_Ephem_1_Y), sField_MoonEphem_Title, theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.text((sRow_Data_Ephem_1_X, sRow_Data_Ephem_1_Y), sRow_Data_Ephem_1, theColorDataText,  font=theInfoDataFont)
    if sRow_Data_Ephem_2 != "": 
        theFinalDraw.text((sRow_Data_Ephem_2_X, sRow_Data_Ephem_2_Y), sRow_Data_Ephem_2, theColorDataText,  font=theInfoDataFont)
        
    if sRow_Data_Hardware_1 != "": 
        theFinalDraw.text((sRow_Data_Hardware_Title_X, sRow_Data_Hardware_1_Y), sField_Hardware_Title, theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.text((sRow_Data_Hardware_1_X, sRow_Data_Hardware_1_Y), sRow_Data_Hardware_1, theColorDataText,  font=theInfoDataFont)
    if sRow_Data_Hardware_2 != "": 
        theFinalDraw.text((sRow_Data_Hardware_2_X, sRow_Data_Hardware_2_Y), sRow_Data_Hardware_2, theColorDataText,  font=theInfoDataFont)
    if sRow_Data_Hardware_3 != "": 
        theFinalDraw.text((sRow_Data_Hardware_3_X, sRow_Data_Hardware_3_Y), sRow_Data_Hardware_3, theColorDataText,  font=theInfoDataFont)
    if sRow_Data_Hardware_4 != "": 
        theFinalDraw.text((sRow_Data_Hardware_4_X, sRow_Data_Hardware_4_Y), sRow_Data_Hardware_4, theColorDataText,  font=theInfoDataFont)
        
    if sRow_Data_Capture != "": 
        theFinalDraw.text((sRow_Data_Capture_Title_X, sRow_Data_Capture_Y), sField_Data_Capture_Title, theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.text((sRow_Data_Capture_X, sRow_Data_Capture_Y), sRow_Data_Capture, theColorDataText,  font=theInfoDataFont)
         
    if sRow_data_Process_1 != "": 
        theFinalDraw.text((sRow_data_Process_Title_X, sRow_data_Process_1_Y), sField_Data_Processing_Title, theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.text((sRow_data_Process_1_X, sRow_data_Process_1_Y), sRow_data_Process_1, theColorDataText,  font=theInfoDataFont)
    if sRow_data_Process_2 != "": 
        theFinalDraw.text((sRow_data_Process_2_X, sRow_data_Process_2_Y), sRow_data_Process_2, theColorDataText,  font=theInfoDataFont)
    if sRow_data_Process_3 != "": 
        theFinalDraw.text((sRow_data_Process_3_X, sRow_data_Process_3_Y), sRow_data_Process_3, theColorDataText,  font=theInfoDataFont)
    if sRow_data_Process_4 != "": 
        theFinalDraw.text((sRow_data_Process_4_X, sRow_data_Process_4_Y), sRow_data_Process_4, theColorDataText,  font=theInfoDataFont)
    if sRow_data_Process_5 != "": 
        theFinalDraw.text((sRow_data_Process_5_X, sRow_data_Process_5_Y), sRow_data_Process_5, theColorDataText,  font=theInfoDataFont)
   
    if bIsMoonPicture and sField_Data_MoonFeature_1 != "":
        if sField_Data_MoonFeature_1 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_1_X, sField_Data_MoonFeature_1_Y), sField_Data_MoonFeature_1, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_1_X, sField_Data_MoonFeature_1_Y), dicInputValues["Info_MoonFeature0_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_1_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_1_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_1_X - iMarginPicture, sField_Data_MoonFeature_1_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature0_Color"]), fill=eval(dicParameters["CommonValues"]["Feature0_Color"]))
        if sField_Data_MoonFeature_2 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_2_X, sField_Data_MoonFeature_2_Y), sField_Data_MoonFeature_2, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_2_X, sField_Data_MoonFeature_2_Y), dicInputValues["Info_MoonFeature1_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_2_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_2_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_2_X - iMarginPicture, sField_Data_MoonFeature_2_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature1_Color"]), fill=eval(dicParameters["CommonValues"]["Feature1_Color"]))
        if sField_Data_MoonFeature_3 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_3_X, sField_Data_MoonFeature_3_Y), sField_Data_MoonFeature_3, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_3_X, sField_Data_MoonFeature_3_Y), dicInputValues["Info_MoonFeature2_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_3_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_3_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_3_X - iMarginPicture, sField_Data_MoonFeature_3_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature2_Color"]), fill=eval(dicParameters["CommonValues"]["Feature2_Color"]))
        if sField_Data_MoonFeature_4 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_4_X, sField_Data_MoonFeature_4_Y), sField_Data_MoonFeature_4, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_4_X, sField_Data_MoonFeature_4_Y), dicInputValues["Info_MoonFeature3_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_4_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_4_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_4_X - iMarginPicture, sField_Data_MoonFeature_4_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature3_Color"]), fill=eval(dicParameters["CommonValues"]["Feature3_Color"]))
        if sField_Data_MoonFeature_5 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_5_X, sField_Data_MoonFeature_5_Y), sField_Data_MoonFeature_5, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_5_X, sField_Data_MoonFeature_5_Y), dicInputValues["Info_MoonFeature4_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_5_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_5_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_5_X - iMarginPicture, sField_Data_MoonFeature_5_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature4_Color"]), fill=eval(dicParameters["CommonValues"]["Feature4_Color"]))
        if sField_Data_MoonFeature_6 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_6_X, sField_Data_MoonFeature_6_Y), sField_Data_MoonFeature_6, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_6_X, sField_Data_MoonFeature_6_Y), dicInputValues["Info_MoonFeature5_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_6_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_6_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_6_X - iMarginPicture, sField_Data_MoonFeature_6_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature5_Color"]), fill=eval(dicParameters["CommonValues"]["Feature5_Color"]))
        if sField_Data_MoonFeature_7 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_7_X, sField_Data_MoonFeature_7_Y), sField_Data_MoonFeature_7, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_7_X, sField_Data_MoonFeature_7_Y), dicInputValues["Info_MoonFeature6_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_7_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_7_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_7_X - iMarginPicture, sField_Data_MoonFeature_7_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature6_Color"]), fill=eval(dicParameters["CommonValues"]["Feature6_Color"]))
        if sField_Data_MoonFeature_8 != "": 
            theFinalDraw.text((sField_Data_MoonFeature_8_X, sField_Data_MoonFeature_8_Y), sField_Data_MoonFeature_8, theColorDataText,  font=theInfoDataFont)
            theFinalDraw.text((sField_Data_MoonFeature_8_X, sField_Data_MoonFeature_8_Y), dicInputValues["Info_MoonFeature7_Name"], theColorDataTitle,  font=theInfoDataFont)
            theFinalDraw.rectangle((sField_Data_MoonFeature_8_X - iDataTextDotSize - iMarginPicture, sField_Data_MoonFeature_8_Y - iDataTextDotSize/2 + iDataTextRowHeight / 2, sField_Data_MoonFeature_8_X - iMarginPicture, sField_Data_MoonFeature_8_Y + iDataTextRowHeight / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature7_Color"]), fill=eval(dicParameters["CommonValues"]["Feature7_Color"]))
  
    
    # Save image
    theFinalImg.save(sOutputFileName + ".png", "PNG")
    print ""
    print " --> created picture: " + sOutputFileName + ".png"
    print ""
    print ""

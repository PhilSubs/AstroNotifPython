#!/usr/bin/python2.7
# -*-coding:Latin-1 -*


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
    for sKey, aValue in sorted(dicJsonValues.iteritems()): 
        # Loop for each occurence
        for j in range(0, dicJsonValues[sKey]["OccurrenceMax"]):
            # Loop through section's fields
            for i in range(0, len(dicJsonValues[sKey]["Fields"])):
                sSubID = dicJsonValues[sKey]["Fields"][i]["ID"].replace("<OccID>", str(j))
                sSubID = sSubID[sSubID.find("-")+1:]
                dicInput[sSubID] = ""
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
    bIsMandatory = False
    theInputValue = None
    theDefaultValue = None
    
    sPromptDisplayed = (sPrompt + "...................................................................")[:60]
    if sType == "Parameter":
        # read parameters
        with open("FormatAstroImages_Settings.json", 'r') as fp:
            dicParameters = json.load(fp)
        # Compute prompt
        sKey = aParam1
        theListItem = eval('dicParameters["' + sKey.replace("/", '"]["') + '"]')
        bIsMandatory = (theListItem["values"][0] != "")
        theDefaultValue = theListItem["default"]
        if not aParam2 is None: theDefaultValue = aParam2
        if bIsMandatory:
            sPromptDisplayed = sPromptDisplayed + ("  [" + " / ".join(theListItem["values"]) + "]")
        else:
            if theDefaultValue != "":
                sPromptDisplayed = sPromptDisplayed + ("  [" + " / ".join(theListItem["values"]) + "]").replace("[ / ", "[ - / ")
            else:
                sPromptDisplayed = sPromptDisplayed + ("  [" + " / ".join(theListItem["values"]) + "]").replace("[ / ", "[")
        if theDefaultValue != "": sPromptDisplayed = sPromptDisplayed + "  --> " + theDefaultValue
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
        sPromptDisplayed = sPromptDisplayed + "[" + aParam2 + "]"
        bIsMandatory = False
    else:
        bIsMandatory = aParam1


    bAnswerIsValid = False
    while not bAnswerIsValid:
        theInputValue = raw_input(sPromptDisplayed + "  ")

        # Handle default value and - value
        if sType == "Parameter":
            if theDefaultValue != "":
                if theInputValue == "": theInputValue = theDefaultValue
                if not bIsMandatory and theInputValue == "-": theInputValue = ""
        elif sType == "String":
            if not aParam2 is None:
                if theInputValue == "": theInputValue = aParam2
                if theInputValue == "-": theInputValue = ""
        
        # check validity
        if not bIsMandatory and theInputValue == "":
             bAnswerIsValid = True
        elif sType == "Parameter":
            sPossibleValuesList = "|".join(theListItem["values"])
            if sPossibleValuesList[0:1] == "|": sPossibleValuesList = sPossibleValuesList[1:]
            iNbOcc, sValueSelected = getOccurrencesInStringList(sPossibleValuesList, theInputValue)
            if iNbOcc == 1:
                theInputValue = sValueSelected
                bAnswerIsValid = True
            else:
                bAnswerIsValid = False
                print "  ERREUR: la valeur doit etre dans la liste:  " + " / ".join(theListItem["values"]) + " !"
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
        elif sType == "StringFromList":
            iNbOcc, sValueSelected = getOccurrencesInStringList(aParam2, theInputValue)
            if iNbOcc == 1:
                theInputValue = sValueSelected
                bAnswerIsValid = True
            else:
                bAnswerIsValid = False
                print "  ERREUR: la valeur doit etre dans la liste:  " + aParam2.replace("|", " / ") + " !"

    if theInputValue != "": print "   --> " + theInputValue
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
        # check if dependency
        bDependencyVerified = True
        if dicJsonValues[sKey]["Dependency"]["Field"] != "":
            bCondition = eval('dicInputValues["' + dicJsonValues[sKey]["Dependency"]["Field"] + '"] ' + dicJsonValues[sKey]["Dependency"]["Operator"] + " " + '"' + dicJsonValues[sKey]["Dependency"]["Value"] + '"')
            if not bCondition: bDependencyVerified = False

        if bDependencyVerified:
            print ""
            print ""
            print sKey
            print ("-"*100)[0:len(sKey)]
            # Loop for each occurence
            bAllOccurenceCompleted = False
            bIsMultipleOccurrence = (dicJsonValues[sKey]["OccurrenceMax"] > 1)
            for j in range(0, dicJsonValues[sKey]["OccurrenceMax"]):
                sDefaultDiameter = ""
                sDefaultHeight = ""
                sDefaultDepth = ""
                sDefaultWidth = ""
                sDefaultLength = ""
                # Loop through section's fields
                if bAllOccurenceCompleted ==  False:
                    for i in range(0, len(dicJsonValues[sKey]["Fields"])):
                        if bAllOccurenceCompleted ==  False:
                            sSubID = dicJsonValues[sKey]["Fields"][i]["ID"].replace("<OccID>", str(j))
                            sSubID = sSubID[sSubID.find("-")+1:]
                            aParam1 = None
                            if dicJsonValues[sKey]["Fields"][i]["Param1"] != "": aParam1 = dicJsonValues[sKey]["Fields"][i]["Param1"]
                            aParam2 = None
                            if dicJsonValues[sKey]["Fields"][i]["Param2"] != "": aParam2 = dicJsonValues[sKey]["Fields"][i]["Param2"]
                            if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Diameter" and sDefaultDiameter != "": aParam2 = sDefaultDiameter
                            if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Depth" and sDefaultDepth != "": aParam2 = sDefaultDepth
                            if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Height" and sDefaultHeight != "": aParam2 = sDefaultHeight
                            if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Length" and sDefaultLength != "": aParam2 = sDefaultLength
                            if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Width" and sDefaultWidth != "": aParam2 = sDefaultWidth
                            sType = dicJsonValues[sKey]["Fields"][i]["Type"]
                            sPrompt = "     "
                            if bIsMultipleOccurrence: sPrompt = sPrompt + "     "
                            sPrompt = sPrompt + dicJsonValues[sKey]["Fields"][i]["Prompt"].replace("<OccID>", str(j))
                            if dicInputValues[sSubID] == "": 
                                if j > 0 and i == 0 and bIsMultipleOccurrence: print "          --------------------------------------------------------------------------------------"
                                dicInputValues[sSubID] = getInputValue(sType, sPrompt, aParam1, aParam2)
                            # if moon feature name, then we take values from the json Lunar Features file if exist
                            if sSubID[0:16] == "Info_MoonFeature" and sSubID[17:] == "_Name":
                                if dicInputValues[sSubID].upper() in dicLunarFeatures:
                                    sLongitude = "-"
                                    sLatitude = "-"
                                    sLength = "-"
                                    sWidth = "-"
                                    sHeight = "-"
                                    if not dicLunarFeatures[dicInputValues[sSubID].upper()]["LongitudeInDeg"] is None: sLongitude = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["LongitudeInDeg"])
                                    if not dicLunarFeatures[dicInputValues[sSubID].upper()]["LatitudeInDeg"] is None: sLatitude = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["LatitudeInDeg"])
                                    if not dicLunarFeatures[dicInputValues[sSubID].upper()]["LengthInKm"] is None: sLength = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["LengthInKm"])
                                    if not dicLunarFeatures[dicInputValues[sSubID].upper()]["WidthInKm"] is None: sWidth = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["WidthInKm"])
                                    if not dicLunarFeatures[dicInputValues[sSubID].upper()]["HeightInM"] is None: sHeight = str(dicLunarFeatures[dicInputValues[sSubID].upper()]["HeightInM"])
                                    print "          Lunar Feature Info ...  Long: " + sLongitude + "km   Lat " + sLatitude + "km   Width: " + sWidth + "km   Length: " + sLength + "km   Height: " + sHeight + "m"
                                    sDefaultDiameter = ""
                                    if sWidth != "-": sDefaultWidth = sWidth + " km"
                                    if sLength != "-": sDefaultLength = sLength + " km"
                                    if sHeight != "-": sDefaultHeight = sHeight + " m"
                                    sDefaultDepth = ""
                                    if sWidth != "-" and sLength != "-":
                                        if float(sWidth) / float(sLength) > 0.9:
                                            sDefaultDiameter = sWidth + " km"
                                            sDefaultWidth = ""
                                            sDefaultLength = ""
                                            sDefaultHeight = ""
                                            if sHeight != "-": sDefaultDepth = sHeight + " m"
                                    if sLongitude != "-": dicInputValues["Info_MoonFeature" + str(j) +  "_Longitude"] = float(sLongitude)
                                    if sLatitude != "-": dicInputValues["Info_MoonFeature" + str(j) +  "_Latitude"] = float(sLatitude)
                            if i==0 and bIsMultipleOccurrence and dicInputValues[sSubID] == "":
                                bAllOccurenceCompleted = True
                            
                        i = i + 1
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
iMarginTopPicture = 20        # Margin above the picture, below the title/subtitle 
iMarginBottomPicture = 20     # Margin below the picture, above the logo and data 
iBorderSize = 1               # Border around the picture
iPositionWinjuposX = 200      # position of the Winjupos, from the right edge (+margin)    
iPositionWinjuposY = 100      # position of the Winjupos, from  the border around the picture (+ margin)   
iDataTextInterligne = 3       # interline in pixel between data text lines
iDataTextInterligneEphem = 12 # interline in pixel between data info text and data info ephemerides
iMarginSignature = 5          # Margin for signature related to inside border of picture
fMiniatureHeight = 96.0       # Height of miniature image for Moon
iDataTextDotSize = 3          # Size of the dot on each data text line for Lunar features

DATA_TITLE_EPHEMERIDE = "EPHEMERIDE  "
DATA_TITLE_TELESCOPE  = "MATERIEL  "
DATA_TITLE_CAPTURE    = "CAPTURE  "
DATA_TITLE_PROCESSING = "TRAITEMENT  "

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

    bIsMoonPicture = (dicInputValues["Subject_Type"] == "Moon")
    bIsPlanetPicture = (dicInputValues["Subject_Type"] == "Planet")
    bIsDeepSkyPicture = (dicInputValues["Subject_Type"] == "Deep Sky")
    
    # Set colors
    theColorTitle           = (255,255,255)
    theColorSubTitle        = (164,164,164)
    theColorDataText        = (96,96,96)
    theColorDataTitle       = (176,176,176)
    if bIsMoonPicture:
        theColorSignature   = (228,228,228,255) # if moon. border and signature more bright
    else:
        theColorSignature   = (128,128,128,255)
    theColorSignatureShadow = (32,32,32)
    
    # Set fonts
#    theGeoDataFont   = ImageFont.truetype("PathwayGothicOne-Regular.ttf",    16)
    theGeoDataFont   = ImageFont.truetype("PCNavita-Regular.ttf", 14)
#    theInfoDataFont  = ImageFont.truetype("PathwayGothicOne-Regular.ttf",    16)
    theInfoDataFont  = ImageFont.truetype("PCNavita-Regular.ttf", 12)
    theTitleFont     = ImageFont.truetype("georgia.ttf",          30)
    theSubTitleFont  = ImageFont.truetype("georgia.ttf",          16)
    theSignatureFont = ImageFont.truetype("Sugar Candy.ttf",      18)
    
    # Compute output file name
    sOutputFileName = dicInputValues["Subject_Type"] + " - " + dicInputValues["TimeLoc_Date"].replace("-","") + dicInputValues["TimeLoc_Time"].replace(":","") + " - " + dicInputValues["Subject_Title"]

    # Save parameters in JSON file if not a json file in input
    if sJsonFilename == "":
        with open(sOutputFileName + '.json', 'w') as fp:
            try:
                json.dump(dicInputValues, fp)
            except:
                pass
                print ""
            print " --> created json file: " + sOutputFileName + ".json"
    
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
#    if iPictureWidth < 1000 and bIsDeepSkyPicture: 
#        iPictureWidthAdjustBorder = (1000 - iPictureWidth) / 2
#        print ">>> Adjusted image width to 1000 instead of " + str(iPictureWidth) + " (border: " + str(iPictureWidthAdjustBorder) + ")"
#        iPictureWidth = 1000
    print "   --> Picture size: " + str(iPictureWidth) + " x " + str(iPictureHeight)
    print ""

    # create temporary bitmap (for computing text size)
    theTempImg = Image.new( 'RGBA', (1920, 100), (0, 0, 0, 255))
    theTempDraw = ImageDraw.Draw(theTempImg)

    # Compute fields to be displayed
    sField_Signature = "PhilippeLarosa"

    arrMonths = [ "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juiller", "Août", "Septembre", "Octobre", "Movembre", "Décembre"]
    sField_Date = str(dicInputValues["TimeLoc_Date"][8:]) + " "
    sField_Date = sField_Date + arrMonths[int(dicInputValues["TimeLoc_Date"][5:7]) - 1] + " "
    sField_Date = sField_Date + str(dicInputValues["TimeLoc_Date"][0:4]) + "  "
    sField_Date = sField_Date + str(dicInputValues["TimeLoc_Time"][0:2]) + ":" + str(dicInputValues["TimeLoc_Time"][3:])
    sField_Date = sField_Date + " GMT"
    
    sField_Location  = dicInputValues["TimeLoc_Location"]
    
    sField_Title     = dicInputValues["Subject_Title"]
    if bIsMoonPicture:
        sField_SubTitle1 = dicInputValues["Info_Additional"]
        sField_SubTitle2 = ""
        sField_SubTitle3 = ""
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Name"], "", "  ", "", "")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Diameter"], "Diam. ", "", sField_Object_Data_1, "   ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Width"], "Larg. ", "", sField_Object_Data_1, "   ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Length"], "Long. ", "", sField_Object_Data_1, "   ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Depth"], "Prof. ", "", sField_Object_Data_1, "   ")
        sField_Object_Data_1 = addInfoToString(dicInputValues["Info_MoonFeature0_Height"], "Haut. ", "", sField_Object_Data_1, "   ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Name"], "", "  ", "", "")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Diameter"], "Diam. ", "", sField_Object_Data_2, "   ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Width"], "Larg. ", "", sField_Object_Data_2, "   ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Length"], "Long. ", "", sField_Object_Data_2, "   ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Depth"], "Prof. ", "", sField_Object_Data_2, "   ")
        sField_Object_Data_2 = addInfoToString(dicInputValues["Info_MoonFeature1_Height"], "Haut. ", "", sField_Object_Data_2, "   ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Name"], "", "  ", "", "")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Diameter"], "Diam. ", "", sField_Object_Data_3, "   ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Width"], "Larg. ", "", sField_Object_Data_3, "   ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Length"], "Long. ", "", sField_Object_Data_3, "   ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Depth"], "Prof. ", "", sField_Object_Data_3, "   ")
        sField_Object_Data_3 = addInfoToString(dicInputValues["Info_MoonFeature2_Height"], "Haut. ", "", sField_Object_Data_3, "   ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Name"], "", "  ", "", "")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Diameter"], "Diam. ", "", sField_Object_Data_4, "   ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Width"], "Larg. ", "", sField_Object_Data_4, "   ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Length"], "Long. ", "", sField_Object_Data_4, "   ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Depth"], "Prof. ", "", sField_Object_Data_4, "   ")
        sField_Object_Data_4 = addInfoToString(dicInputValues["Info_MoonFeature3_Height"], "Haut. ", "", sField_Object_Data_4, "   ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Name"], "", "  ", "", "")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Diameter"], "Diam. ", "", sField_Object_Data_5, "   ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Width"], "Larg. ", "", sField_Object_Data_5, "   ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Length"], "Long. ", "", sField_Object_Data_5, "   ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Depth"], "Prof. ", "", sField_Object_Data_5, "   ")
        sField_Object_Data_5 = addInfoToString(dicInputValues["Info_MoonFeature4_Height"], "Haut. ", "", sField_Object_Data_5, "   ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Name"], "", "  ", "", "")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Diameter"], "Diam. ", "", sField_Object_Data_6, "   ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Width"], "Larg. ", "", sField_Object_Data_6, "   ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Length"], "Long. ", "", sField_Object_Data_6, "   ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Depth"], "Prof. ", "", sField_Object_Data_6, "   ")
        sField_Object_Data_6 = addInfoToString(dicInputValues["Info_MoonFeature5_Height"], "Haut. ", "", sField_Object_Data_6, "   ")

    elif bIsPlanetPicture:
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Distance"], "Distance ", "", "", "")
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Diameter"], "Diameter ", '"', sField_SubTitle1, " - ")
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Magnitude"], "Magnitude ", "", sField_SubTitle1, " - ")
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_Planet_Altitude"], "Altitude ", "deg", sField_SubTitle1, " - ")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_Planet_CMI"], "CMI ", "deg", "", "")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_Planet_CMII"], "CMII ", "deg", sField_SubTitle2, " - ")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_Planet_CMIII"], "CMIII ", "deg", sField_SubTitle2, " - ")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_Planet_FocalLength"], "Focal ", "mm", "", "")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_Planet_FocalRatio"], "F/", "", sField_SubTitle3, " - ")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_Planet_Resolution"], "Resolution  ", '"', sField_SubTitle3, " - ")
        sField_Object_Data_1 = ""
        sField_Object_Data_2 = ""
        sField_Object_Data_3 = ""
        sField_Object_Data_4 = ""
        sField_Object_Data_5 = ""
        sField_Object_Data_6 = ""
    elif bIsDeepSkyPicture:
        sField_SubTitle1 = addInfoToString(dicInputValues["Info_DeepSky_Distance"], "Distance ", "", "", "")
        sField_SubTitle2 = addInfoToString(dicInputValues["Info_DeepSky_Diameter"], "Diametre ", "", "", "")
        sField_SubTitle3 = addInfoToString(dicInputValues["Info_DeepSky_Magnitude"], "Magnitude ", "", "", "")
        sField_Object_Data_1 = ""
        sField_Object_Data_2 = ""
        sField_Object_Data_3 = ""
        sField_Object_Data_4 = ""
        sField_Object_Data_5 = ""
        sField_Object_Data_6 = ""
        
    sField_MoonEphem_Title = DATA_TITLE_EPHEMERIDE
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonAge"], "Lune: age ", "", "", "")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonIllumination"], "illum. ", "%", sField_MoonEphem, " - ")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonColongitude"], "colong. ", "", sField_MoonEphem, " - ")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonPositionAngle"], "pos. angle. ", "", sField_MoonEphem, " - ")
    sField_Hardware_Title = DATA_TITLE_TELESCOPE
    sField_Hardware_1 = addInfoToString(dicInputValues["Hardware_Optic"], "", "", "", "")
    sField_Hardware_1 = addInfoToString(dicInputValues["Hardware_Mount"], "", "", sField_Hardware_1, " - ")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_ADC"], "ADC ", "", "", "")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_Reducer"], "", "", sField_Hardware_2, " - ")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_Barlow"], "Barlow ", "", sField_Hardware_2, " - ")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_Filter"], "Filtre ", "", sField_Hardware_2, " - ")
    sField_Hardware_3 = addInfoToString(dicInputValues["Hardware_Camera"], "Camera ", "", "", "")
    sField_Hardware_4 = addInfoToString(dicInputValues["Hardware_Additional_Info"], "", "", "", "")
    sField_Data_Capture_Title = DATA_TITLE_CAPTURE
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Software"], "", "", "", "")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Bin"], "bin ", "", sField_Data_Capture, " - ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Bits"], "", " bits", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Gain"], "Gain ", "", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Exposition"], "Exp. ", "", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_Rate"], "", " fps", sField_Data_Capture, " / ")
    sField_Data_Capture = addInfoToString(dicInputValues["Capture_TotalExposure"], "Total ", "", sField_Data_Capture, " - ")
    sField_Data_Processing_Title = DATA_TITLE_PROCESSING
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_ImagesProcessed"], "", "", "", "")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_Pre-processingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_StackingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_ProcessingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_RenderingSoftware"], "", "", sField_Data_Processing, " - ")
    sField_Data_Processing = addInfoToString(dicInputValues["Processing_AdditionalInfo"], "", "", sField_Data_Processing, " - ")
    
    # Display fields
    print ""
    print ""
    print "   FIELDS"
    print "   ------"
    print ""
    print "     Field_Date:              " + sField_Date
    print "     Field_Location:          " + sField_Location
    print ""
    print "     Field_Title:             " + sField_Title
    print "     Field_SubTitle1:         " + sField_SubTitle1
    print "     Field_SubTitle2:         " + sField_SubTitle2
    print "     Field_SubTitle3:         " + sField_SubTitle3
    print ""
    print "     Field_MoonEphem:         " + sField_MoonEphem
    print ""
    print "     Field_Hardware 1:        " + (DATA_TITLE_TELESCOPE + "              ")[0:15] + sField_Hardware_1
    print "     Field_Hardware 2:        " + "               " + sField_Hardware_2
    print "     Field_Hardware 3:        " + "               " + sField_Hardware_3
    print "     Field_Hardware 4:        " + "               " + sField_Hardware_4
    print "     Field_Data_Capture:      " + (DATA_TITLE_CAPTURE + "              ")[0:15] + sField_Data_Capture
    print "     Field_Data_Processing:   " + (DATA_TITLE_PROCESSING + "              ")[0:15] + sField_Data_Processing
    print ""
    print "     Field_Object_Data_1:     " + sField_Object_Data_1
    print "     Field_Object_Data_2:     " + sField_Object_Data_2
    print "     Field_Object_Data_3:     " + sField_Object_Data_3
    print "     Field_Object_Data_4:     " + sField_Object_Data_4
    print "     Field_Object_Data_5:     " + sField_Object_Data_5
    print "     Field_Object_Data_6:     " + sField_Object_Data_6
    print ""
    print ""
       
    
    # compute objects size and position
    iTitleAndSubtitleHeight = theTempDraw.textsize(sField_Title, font=theTitleFont)[1] + iDataTextInterligne * 5  
    iTitleAndSubtitleHeight = iTitleAndSubtitleHeight + theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[1] + iDataTextInterligne
    iTitleAndSubtitleHeight = iTitleAndSubtitleHeight + theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[1] + iDataTextInterligne
    iTitleAndSubtitleHeight = iTitleAndSubtitleHeight + theTempDraw.textsize(sField_SubTitle3, font=theSubTitleFont)[1]
    if not imgWinjupos is None:                      
        iMoonWinjuposHeight = iWinjuposHeight
    else:
        iMoonWinjuposHeight = 0
    iDateLocationMoonEphemHeight = theTempDraw.textsize(sField_Date, font=theGeoDataFont)[1] + iDataTextInterligne
    iDateLocationMoonEphemHeight = theTempDraw.textsize(sField_Location, font=theGeoDataFont)[1] + iDataTextInterligne
    iDateLocationMoonEphemHeight = theTempDraw.textsize(sField_MoonEphem, font=theGeoDataFont)[1]
    
    iTopInfoHeight = iDateLocationMoonEphemHeight
    if iTitleAndSubtitleHeight > iTopInfoHeight: iTopInfoHeight = iTitleAndSubtitleHeight
    if iMoonWinjuposHeight > iTopInfoHeight: iTopInfoHeight = iMoonWinjuposHeight
    
    iObjectDataInfoHeight = theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[1] + iDataTextInterligne
    iObjectDataInfoHeight = iObjectDataInfoHeight + theTempDraw.textsize(sField_Object_Data_6, font=theInfoDataFont)[1]
    if sField_MoonEphem != "":
        iTechnicalDataInfoHeight = theTempDraw.textsize(sField_MoonEphem, font=theInfoDataFont)[1] + iDataTextInterligneEphem
        iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligne
    else:
        iTechnicalDataInfoHeight = theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Hardware_2, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Hardware_4, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Data_Capture, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Data_Processing, font=theInfoDataFont)[1]
    if iObjectDataInfoHeight > iTechnicalDataInfoHeight:
        iDataInfoHeight = iObjectDataInfoHeight
    else:
        iDataInfoHeight = iTechnicalDataInfoHeight
    if bIsMoonPicture and iDataInfoHeight < int(fMiniatureHeight): iDataInfoHeight = int(fMiniatureHeight)
    iPictureWithBorderWidth  = iBorderSize + iMarginPicture + iPictureWidth  + iMarginPicture + iBorderSize
    iPictureWithBorderHeight = iBorderSize + iMarginPicture + iPictureHeight + iMarginPicture + iBorderSize
    iFinalImageWidth  = iFinalPictureMarginWidth + iPictureWithBorderWidth + iFinalPictureMarginWidth
    iFinalImageHeight = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture + iDataInfoHeight + iFinalPictureMarginWidth
    
    if not imgWinjupos is None:
        iWinjuposPositionX = iFinalImageWidth - iWinjuposWidth - iFinalPictureMarginWidth
        iWinjuposPositionY = iFinalPictureMarginWidth
    iPictureFramePositionX = iFinalPictureMarginWidth
    iPictureFramePositionY = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture
    iPicturePositionX = iPictureFramePositionX + iMarginPicture 
    iPicturePositionY = iPictureFramePositionY + iMarginPicture

    # Compute fields' position
    iField_Signature_X = iPicturePositionX + iPictureWidth - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[0] - iMarginSignature
    iField_Signature_Y = iPicturePositionY + iPictureHeight - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] - iMarginSignature
    iField_Signature_Y = iPicturePositionY + iPictureHeight + iMarginPicture - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] / 3

    iField_Date_X      = iFinalPictureMarginWidth
    iField_Date_Y      = iFinalPictureMarginWidth
    iField_Location_X  = iFinalPictureMarginWidth
    iField_Location_Y  = iField_Date_Y + theTempDraw.textsize(sField_Date, font=theGeoDataFont)[1] + iDataTextInterligne

    iField_Title_X     = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_Title, font=theTitleFont)[0]) / 2
    iField_Title_Y     = iFinalPictureMarginWidth + (iTopInfoHeight - iTitleAndSubtitleHeight) / 2
    iField_SubTitle1_X = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[0]) / 2
    iField_SubTitle1_Y = iField_Title_Y + theTempDraw.textsize(sField_Title, font=theTitleFont)[1] + iDataTextInterligne * 5
    iField_SubTitle2_X = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[0]) / 2
    iField_SubTitle2_Y = iField_SubTitle1_Y + theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[1] + iDataTextInterligne
    iField_SubTitle3_X = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle3, font=theSubTitleFont)[0]) / 2
    iField_SubTitle3_Y = iField_SubTitle2_Y + theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[1] + iDataTextInterligne

    iField_Object_Data_min_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[0]
    if iField_Object_Data_min_X > (iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[0]): iField_Object_Data_min_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[0]
    if iField_Object_Data_min_X > (iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[0]): iField_Object_Data_min_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[0]
    if iField_Object_Data_min_X > (iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[0]): iField_Object_Data_min_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[0]
    if iField_Object_Data_min_X > (iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[0]): iField_Object_Data_min_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[0]
    if iField_Object_Data_min_X > (iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_6, font=theInfoDataFont)[0]): iField_Object_Data_min_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_6, font=theInfoDataFont)[0]

    iObject_Data_Row_Height = theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[1] + iDataTextInterligne
    if (theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[1] + iDataTextInterligne) > iObject_Data_Row_Height: iObject_Data_Row_Height = theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[1] + iDataTextInterligne
    if (theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[1] + iDataTextInterligne) > iObject_Data_Row_Height: iObject_Data_Row_Height = theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[1] + iDataTextInterligne
    if (theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[1] + iDataTextInterligne) > iObject_Data_Row_Height: iObject_Data_Row_Height = theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[1] + iDataTextInterligne
    if (theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[1] + iDataTextInterligne) > iObject_Data_Row_Height: iObject_Data_Row_Height = theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[1] + iDataTextInterligne

    iField_Object_Data_1_X = iField_Object_Data_min_X
    iField_Object_Data_1_Y = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Object_Data_2_X = iField_Object_Data_min_X
    iField_Object_Data_2_Y = iField_Object_Data_1_Y + iObject_Data_Row_Height
    iField_Object_Data_3_X = iField_Object_Data_min_X
    iField_Object_Data_3_Y = iField_Object_Data_2_Y + iObject_Data_Row_Height
    iField_Object_Data_4_X = iField_Object_Data_min_X
    iField_Object_Data_4_Y = iField_Object_Data_3_Y + iObject_Data_Row_Height
    iField_Object_Data_5_X = iField_Object_Data_min_X
    iField_Object_Data_5_Y = iField_Object_Data_4_Y + iObject_Data_Row_Height
    iField_Object_Data_6_X = iField_Object_Data_min_X
    iField_Object_Data_6_Y = iField_Object_Data_5_Y + iObject_Data_Row_Height

    iSizeMax_Title_Data = theTempDraw.textsize(sField_Hardware_Title, font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Data_Capture_Title, font=theInfoDataFont)[0] > iSizeMax_Title_Data: iSizeMax_Title_Data = theTempDraw.textsize(sField_Data_Capture_Title, font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Data_Processing_Title, font=theInfoDataFont)[0] > iSizeMax_Title_Data: iSizeMax_Title_Data = theTempDraw.textsize(sField_Data_Processing_Title, font=theInfoDataFont)[0]
    
    iField_MoonEphem_Title_X       = iFinalPictureMarginWidth
    iField_MoonEphem_Title_Y       = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_MoonEphem_X             = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_MoonEphem_Y             = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Hardware_Title_X        = iFinalPictureMarginWidth
    iField_Hardware_1_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    if sField_MoonEphem != "": 
        iField_Hardware_Title_Y        = iField_MoonEphem_Y + theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligneEphem
        iField_Hardware_1_Y            = iField_MoonEphem_Y + theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligneEphem
    else:
        iField_Hardware_Title_Y        = iField_MoonEphem_Title_Y
        iField_Hardware_1_Y            = iField_MoonEphem_Title_Y
    iField_Hardware_2_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Hardware_2_Y            = iField_Hardware_1_Y + theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Hardware_3_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Hardware_3_Y            = iField_Hardware_2_Y + theTempDraw.textsize(sField_Hardware_2, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Hardware_4_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Hardware_4_Y            = iField_Hardware_3_Y + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Capture_Title_X    = iFinalPictureMarginWidth
    if sField_Hardware_4 != "": 
        iField_Data_Capture_Title_Y    = iField_Hardware_4_Y + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
    else:
        iField_Data_Capture_Title_Y    = iField_Hardware_3_Y + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Capture_X          = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Data_Capture_Y          = iField_Data_Capture_Title_Y
    iField_Data_Processing_Title_X = iFinalPictureMarginWidth
    iField_Data_Processing_Title_Y = iField_Data_Capture_Y + theTempDraw.textsize(sField_Data_Capture, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Processing_X       = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Data_Processing_Y       = iField_Data_Capture_Y + theTempDraw.textsize(sField_Data_Capture, font=theInfoDataFont)[1] + iDataTextInterligne

    # create new bitmap
    theFinalImg = Image.new( 'RGBA', (iFinalImageWidth, iFinalImageHeight), (0, 0, 0, 255))
    theFinalDraw = ImageDraw.Draw(theFinalImg)
    
    # paste Winjupos             
    if dicInputValues["Bitmap_WinjuposFileName"] != "":
        # if moon picture, add marker on winjupos image for features location
        if bIsMoonPicture:
            if dicInputValues["Info_MoonFeature0_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature0_Longitude"], dicInputValues["Info_MoonFeature0_Latitude"], eval(dicParameters["CommonValues"]["Feature0_Color"]))
            if dicInputValues["Info_MoonFeature1_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature1_Longitude"], dicInputValues["Info_MoonFeature1_Latitude"], eval(dicParameters["CommonValues"]["Feature1_Color"]))
            if dicInputValues["Info_MoonFeature2_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature2_Longitude"], dicInputValues["Info_MoonFeature2_Latitude"], eval(dicParameters["CommonValues"]["Feature2_Color"]))
            if dicInputValues["Info_MoonFeature3_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature3_Longitude"], dicInputValues["Info_MoonFeature3_Latitude"], eval(dicParameters["CommonValues"]["Feature3_Color"]))
            if dicInputValues["Info_MoonFeature4_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature4_Longitude"], dicInputValues["Info_MoonFeature4_Latitude"], eval(dicParameters["CommonValues"]["Feature4_Color"]))
            if dicInputValues["Info_MoonFeature5_Name"] != "":  imgWinjupos = addLocationMarkerOnWinjuposImage(imgWinjupos, dicInputValues["Info_MoonPositionAngle"], dicInputValues["Info_MoonFeature5_Longitude"], dicInputValues["Info_MoonFeature5_Latitude"], eval(dicParameters["CommonValues"]["Feature5_Color"]))
        theFinalImg.paste(imgWinjupos, (iWinjuposPositionX, iWinjuposPositionY))

        
    # Display fields
    theFinalDraw.text((iField_Date_X,      iField_Date_Y),      sField_Date,      theColorDataText, font=theGeoDataFont)
    theFinalDraw.text((iField_Location_X,  iField_Location_Y),  sField_Location,  theColorDataText, font=theGeoDataFont)
    
    theFinalDraw.text((iField_Title_X,     iField_Title_Y),     sField_Title,     theColorTitle,    font=theTitleFont)
    theFinalDraw.text((iField_SubTitle1_X, iField_SubTitle1_Y), sField_SubTitle1, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_SubTitle2_X, iField_SubTitle2_Y), sField_SubTitle2, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_SubTitle3_X, iField_SubTitle3_Y), sField_SubTitle3, theColorSubTitle, font=theSubTitleFont)
    
    theFinalDraw.text((iField_Object_Data_1_X, iField_Object_Data_1_Y), sField_Object_Data_1, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_1 != "" and bIsMoonPicture: 
        theFinalDraw.text((iField_Object_Data_1_X, iField_Object_Data_1_Y), dicInputValues["Info_MoonFeature0_Name"], theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.rectangle((iField_Object_Data_1_X - iDataTextDotSize - iMarginPicture, iField_Object_Data_1_Y - iDataTextDotSize/2 + theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[1] / 2, iField_Object_Data_1_X - iMarginPicture, iField_Object_Data_1_Y + theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[1] / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature0_Color"]), fill=eval(dicParameters["CommonValues"]["Feature0_Color"]))
    theFinalDraw.text((iField_Object_Data_2_X, iField_Object_Data_2_Y), sField_Object_Data_2, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_2 != "" and bIsMoonPicture: 
        theFinalDraw.text((iField_Object_Data_2_X, iField_Object_Data_2_Y), dicInputValues["Info_MoonFeature1_Name"], theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.rectangle((iField_Object_Data_2_X - iDataTextDotSize - iMarginPicture, iField_Object_Data_2_Y - iDataTextDotSize/2 + theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[1] / 2, iField_Object_Data_2_X - iMarginPicture, iField_Object_Data_2_Y + theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[1] / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature1_Color"]), fill=eval(dicParameters["CommonValues"]["Feature1_Color"]))
    theFinalDraw.text((iField_Object_Data_3_X, iField_Object_Data_3_Y), sField_Object_Data_3, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_3 != "" and bIsMoonPicture: 
        theFinalDraw.text((iField_Object_Data_3_X, iField_Object_Data_3_Y), dicInputValues["Info_MoonFeature2_Name"], theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.rectangle((iField_Object_Data_3_X - iDataTextDotSize - iMarginPicture, iField_Object_Data_3_Y - iDataTextDotSize/2 + theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[1] / 2, iField_Object_Data_3_X - iMarginPicture, iField_Object_Data_3_Y + theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[1] / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature2_Color"]), fill=eval(dicParameters["CommonValues"]["Feature2_Color"]))
    theFinalDraw.text((iField_Object_Data_4_X, iField_Object_Data_4_Y), sField_Object_Data_4, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_4 != "" and bIsMoonPicture: 
        theFinalDraw.text((iField_Object_Data_4_X, iField_Object_Data_4_Y), dicInputValues["Info_MoonFeature3_Name"], theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.rectangle((iField_Object_Data_4_X - iDataTextDotSize - iMarginPicture, iField_Object_Data_4_Y - iDataTextDotSize/2 + theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[1] / 2, iField_Object_Data_4_X + - iMarginPicture, iField_Object_Data_4_Y + theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[1] / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature3_Color"]), fill=eval(dicParameters["CommonValues"]["Feature3_Color"]))
    theFinalDraw.text((iField_Object_Data_5_X, iField_Object_Data_5_Y), sField_Object_Data_5, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_5 != "" and bIsMoonPicture: 
        theFinalDraw.text((iField_Object_Data_5_X, iField_Object_Data_5_Y), dicInputValues["Info_MoonFeature4_Name"], theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.rectangle((iField_Object_Data_5_X - iDataTextDotSize - iMarginPicture, iField_Object_Data_5_Y - iDataTextDotSize/2 + theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[1] / 2, iField_Object_Data_5_X + - iMarginPicture, iField_Object_Data_5_Y + theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[1] / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature4_Color"]), fill=eval(dicParameters["CommonValues"]["Feature4_Color"]))
    theFinalDraw.text((iField_Object_Data_6_X, iField_Object_Data_6_Y), sField_Object_Data_6, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_6 != "" and bIsMoonPicture: 
        theFinalDraw.text((iField_Object_Data_6_X, iField_Object_Data_6_Y), dicInputValues["Info_MoonFeature5_Name"], theColorDataTitle, font=theInfoDataFont)
        theFinalDraw.rectangle((iField_Object_Data_6_X - iDataTextDotSize - iMarginPicture, iField_Object_Data_6_Y - iDataTextDotSize/2 + theTempDraw.textsize(sField_Object_Data_6, font=theInfoDataFont)[1] / 2, iField_Object_Data_6_X + - iMarginPicture, iField_Object_Data_6_Y + theTempDraw.textsize(sField_Object_Data_6, font=theInfoDataFont)[1] / 2 + iDataTextDotSize/2 ), outline=eval(dicParameters["CommonValues"]["Feature5_Color"]), fill=eval(dicParameters["CommonValues"]["Feature5_Color"]))

    if sField_MoonEphem != "": theFinalDraw.text((iField_MoonEphem_X, iField_MoonEphem_Y), sField_MoonEphem, theColorDataText,  font=theInfoDataFont)
    if sField_MoonEphem != "": theFinalDraw.text((iField_MoonEphem_Title_X, iField_MoonEphem_Title_Y), sField_MoonEphem_Title, theColorDataTitle, font=theInfoDataFont)
    
    theFinalDraw.text((iField_Hardware_1_X, iField_Hardware_1_Y), sField_Hardware_1, theColorDataText,  font=theInfoDataFont)
    theFinalDraw.text((iField_Hardware_Title_X, iField_Hardware_Title_Y), sField_Hardware_Title, theColorDataTitle, font=theInfoDataFont)
    if sField_Hardware_2 != "": theFinalDraw.text((iField_Hardware_2_X, iField_Hardware_2_Y), sField_Hardware_2, theColorDataText,  font=theInfoDataFont)
    if sField_Hardware_3 != "": theFinalDraw.text((iField_Hardware_3_X, iField_Hardware_3_Y), sField_Hardware_3, theColorDataText,  font=theInfoDataFont)
    if sField_Hardware_4 != "": theFinalDraw.text((iField_Hardware_4_X, iField_Hardware_4_Y), sField_Hardware_4, theColorDataText,  font=theInfoDataFont)
    theFinalDraw.text((iField_Data_Capture_X, iField_Data_Capture_Y), sField_Data_Capture, theColorDataText,  font=theInfoDataFont)
    theFinalDraw.text((iField_Data_Capture_Title_X, iField_Data_Capture_Title_Y), sField_Data_Capture_Title, theColorDataTitle, font=theInfoDataFont)
    theFinalDraw.text((iField_Data_Processing_X, iField_Data_Processing_Y), sField_Data_Processing, theColorDataText,  font=theInfoDataFont)
    theFinalDraw.text((iField_Data_Processing_Title_X, iField_Data_Processing_Title_Y), sField_Data_Processing_Title, theColorDataTitle, font=theInfoDataFont)
    
    # Draw border around the picture
    theFinalDraw.rectangle((iPictureFramePositionX, iPictureFramePositionY, iPictureFramePositionX + iMarginPicture * 2 + iBorderSize + iPictureWidth , iPictureFramePositionY + iMarginPicture * 2 + iBorderSize + iPictureHeight ), outline=theColorSignature, fill=(0, 0, 0, 255))
    theFinalDraw.rectangle((iField_Signature_X - 10, iField_Signature_Y - theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] , iField_Signature_X + theTempDraw.textsize(sField_Signature, font=theSignatureFont)[0], iField_Signature_Y + theTempDraw.textsize(sField_Signature, font=theSignatureFont)[1] ), outline=(0, 0, 0, 255), fill=(0, 0, 0, 255))
    
    # paste picture
    theFinalImg.paste(imgPicture, (iPicturePositionX + iPictureWidthAdjustBorder, iPicturePositionY ))
        
    # Signature
    theFinalDraw.text((iField_Signature_X,     iField_Signature_Y),     sField_Signature, theColorSignatureShadow, font=theSignatureFont)
    theFinalDraw.text((iField_Signature_X - 1, iField_Signature_Y - 1), sField_Signature, theColorSignatureShadow, font=theSignatureFont)
    theFinalDraw.text((iField_Signature_X - 2, iField_Signature_Y - 2), sField_Signature, theColorSignature, font=theSignatureFont)

    # Add miniature for Moon, if at least one feature is mentioned
    if bIsMoonPicture:
        if dicInputValues["Info_MoonFeature0_Name"] != "":
            imgMiniature = Image.open(dicInputValues["Bitmap_PictureFileName"])
            iMiniatureWidth, iMiniatureHeight = imgMiniature.size
            fCoeff = fMiniatureHeight / float(iMiniatureHeight)
            iMiniatureWidth = int(float(iMiniatureWidth) * fCoeff)
            iMiniatureHeight = int(float(iMiniatureHeight) * fCoeff)
            imgMiniature.thumbnail((iMiniatureWidth, iMiniatureHeight), Image.ANTIALIAS)
            iMiniature_X = iField_Object_Data_1_X
            if iField_Object_Data_2_X < iMiniature_X: iMiniature_X = iField_Object_Data_2_X
            if iField_Object_Data_3_X < iMiniature_X: iMiniature_X = iField_Object_Data_3_X
            if iField_Object_Data_4_X < iMiniature_X: iMiniature_X = iField_Object_Data_4_X
            if iField_Object_Data_5_X < iMiniature_X: iMiniature_X = iField_Object_Data_5_X
            if iField_Object_Data_6_X < iMiniature_X: iMiniature_X = iField_Object_Data_6_X
            iMiniature_X = iMiniature_X - iMarginBottomPicture - iDataTextDotSize - iMarginPicture - iMiniatureWidth
            iMiniature_Y = iField_Object_Data_1_Y
            theFinalDraw.rectangle((iMiniature_X, iMiniature_Y, iMiniature_X + iMiniatureWidth + 1, iMiniature_Y + iMiniatureHeight), outline=theColorDataTitle, fill=(255, 0, 0, 255))
            theFinalImg.paste(imgMiniature, (iMiniature_X + 1 , iMiniature_Y + 1 ))
    
    # Save image
    theFinalImg.save(sOutputFileName + ".png", "PNG")
    print ""
    print " --> created picture: " + sOutputFileName + ".png"
    print ""
    print ""

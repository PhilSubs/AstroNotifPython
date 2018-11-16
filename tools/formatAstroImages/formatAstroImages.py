#!/usr/bin/python2.7
# -*-coding:Latin-1 -*


# Minimap.png ... correspond to the Winjupos bitmap  128x128 pixels
    
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
        print "Planet Distance................ " + dicInputValues["Info_Planet_Distance"]
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
    print "Winjupos file name.............. " + dicInputValues["Bitmap_WinjuposFileName"]   
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
    dicInput["Bitmap_WinjuposFileName"] = ""
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
    dicInput["Info_Planet_Distance"] = ""
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
    #        String            aParam1: is mandatory (bool)       aParam2:  
    #        StringFromList    aParam1: is mandatory (bool)       aParam2: possible value list (| delim)
    bIsMandatory = False
    theInputValue = None
    theDefaultValue = None
    
    sPromptDisplayed = (sPrompt + "...................................................................")[:60]
    if sType == "Parameter":
        # read parameters
        with open("parameters.json", 'r') as fp:
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
                aDate = datetime.datetime(int(theInputValue[0:4]), int(theInputValue[5:7]), int(theInputValue[8:]), 0, 0, 0)
                if theInputValue[4:5] != "-" or theInputValue[7:8] != "-":
                    bAnswerIsValid = False
                else:
                    bAnswerIsValid = True
            except:
                bAnswerIsValid = False
        elif sType == "TimeHH:MM":
            try:
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
                print "  ERREUR: la valeur doit Ãªtre dans la liste:  " + aParam2.replace("|", " / ") + " !"

    if theInputValue != "": print "   --> " + theInputValue
    return theInputValue

def readInputsFromKeyboard():
    dicInputValues = getEmptyDicInput() 
    print ""
    print ""
    print "Pictures"
    print "--------"
    dicInputValues["Bitmap_WinjuposFileName"] = getInputValue("Filename", "Name of PNG file from Winjupos (256x256) ", False, ".png")
    dicInputValues["Bitmap_PictureFileName"] = getInputValue("Filename", "Name of PNG file for picture ", True, ".png")

    print ""
    print "Subject"
    print "-------"
    dicInputValues["Subject_Type"]  = (getInputValue("StringFromList", "Object type: Moon, Planet, Deep Sky ", True, "M|P|DS")).upper()
    dicInputValues["Subject_Title"] = getInputValue("String", "Title ", True, None)
    if dicInputValues["Subject_Type"] == "M":  dicInputValues["Subject_Type"] = "Moon"
    if dicInputValues["Subject_Type"] == "P":  dicInputValues["Subject_Type"] = "Planet"
    if dicInputValues["Subject_Type"] == "DS": dicInputValues["Subject_Type"] = "Deep Sky"
    if dicInputValues["Subject_Type"] == "Moon":
        dicInputValues["Info_MoonAge"]          = getInputValue("String", "Moon Age ", False, None) 
        dicInputValues["Info_MoonIllumination"] = getInputValue("String", "Moon Illumination (%) ", False, None) 
        dicInputValues["Info_MoonColongitude"]  = getInputValue("String", "Moon Colongitude (deg) ", False, None) 
        bAllFeaturesFilled = False
        for i in range(0,6):
            sFeatureID = str(i).strip()
            dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] = ""
            if not bAllFeaturesFilled:
                dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] = getInputValue("String", "    Feature " + sFeatureID + " Name ", False, None)
                if dicInputValues["Info_MoonFeature" + sFeatureID + "_Name"] != "":
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Diameter"] = getInputValue("String", "        Diameter (+ unit) ", False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Height"]   = getInputValue("String", "        Height (+ unit) ", False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Length"]   = getInputValue("String", "        Length  (+ unit)", False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Width"]    = getInputValue("String", "        Width (+ unit) ", False, None)
                    dicInputValues["Info_MoonFeature" + sFeatureID + "_Depth"]    = getInputValue("String", "        Depth (+ unit) ", False, None)
                else:
                    bAllFeaturesFilled = True
        dicInputValues["Info_Additional"] = getInputValue("String", "Additional comment ", False, None)
    elif dicInputValues["Subject_Type"] == "Planet":
        dicInputValues["Info_Planet_Distance"]    = getInputValue("String", "Planet Distance (+ unit) ", False, None) 
        dicInputValues["Info_Planet_Diameter"]    = getInputValue("String", "Planet Diameter (sec) ", False, None) 
        dicInputValues["Info_Planet_Altitude"]    = getInputValue("String", "Planet Altitude (deg) ", False, None) 
        dicInputValues["Info_Planet_Magnitude"]   = getInputValue("String", "Planet Magnitude ", False, None) 
        dicInputValues["Info_Planet_CMI"]         = getInputValue("String", "Planet CMI (deg) ", False, None) 
        dicInputValues["Info_Planet_CMII"]        = getInputValue("String", "Planet CMII (deg) ", False, None) 
        dicInputValues["Info_Planet_CMIII"]       = getInputValue("String", "Planet CMIII (deg) ", False, None) 
        dicInputValues["Info_Planet_FocalLength"] = getInputValue("String", "Planet Focal Length (mm) ", False, None) 
        dicInputValues["Info_Planet_FocalRatio"]  = getInputValue("String", "Planet Focal Ratio (F/..) ", False, None) 
        dicInputValues["Info_Planet_Resolution"]  = getInputValue("String", "Planet Resolution (sec) ", False, None) 
    elif dicInputValues["Subject_Type"] == "Deep Sky":
        dicInputValues["Info_DeepSky_Type"]      = getInputValue("String", "Object Type ", False, None) 
        dicInputValues["Info_DeepSky_Distance"]  = getInputValue("String", "Object Distance (+ unit) ", False, None) 
        dicInputValues["Info_DeepSky_Diameter"]  = getInputValue("String", "Object Diameter (+ unit) ", False, None) 
        dicInputValues["Info_DeepSky_Magnitude"] = getInputValue("String", "Object Magnitude ", False, None) 
    print ""
    print "Time & Location"
    print "---------------"
    dicInputValues["TimeLoc_Date"]     = getInputValue("DateAAAA-MM-JJ", "Date       [AAAA-MM-JJ] ", True, None)
    dicInputValues["TimeLoc_Time"]     = getInputValue("TimeHH:MM", "Time GMT   [HH:MM] ", True, None)
    dicInputValues["TimeLoc_Location"] = getInputValue("Parameter", "Location ", "Other/Location", None)
    print ""
    print "Hardware"
    print "--------"
    dicInputValues["Hardware_Optic"]   = getInputValue("Parameter", "Optical instrument ", "Hardware/Instrument/Scope", None)
    dicInputValues["Hardware_Mount"]   = getInputValue("Parameter", "Mount ", "Hardware/Instrument/Mount", None)
    dicInputValues["Hardware_ADC"]     = getInputValue("Parameter", "Accessory: ADC ?", "Hardware/Accessories/ADC", None)
    dicInputValues["Hardware_Reducer"] = getInputValue("Parameter", "Accessory: Reducer ?", "Hardware/Accessories/Reducer", None)
    dicInputValues["Hardware_Barlow"]  = getInputValue("Parameter", "Accessory: Barlow ?", "Hardware/Accessories/Barlow", None)
    dicInputValues["Hardware_Camera"]  = getInputValue("Parameter", "Camera ", "Hardware/Camera", None)
    if dicInputValues["Hardware_Camera"] == "ASI 224MC":
        dicInputValues["Hardware_Filter"]   = getInputValue("Parameter", "Filter ", "Hardware/Accessories/Filters", "IR/UV Cut")
    else:
        dicInputValues["Hardware_Filter"]   = getInputValue("Parameter", "Filter ", "Hardware/Accessories/Filters", None)
    print ""
    print "Capture"
    print "-------"
    dicInputValues["Capture_Software"]      = getInputValue("Parameter", "Capture software ", "Software/Capture", None)
    dicInputValues["Capture_Bin"]           = getInputValue("Parameter", "Bin setting ", "CameraSettings/Bin", None)
    dicInputValues["Capture_Gain"]          = getInputValue("String", "Gain setting ", True, None)
    dicInputValues["Capture_Bits"]          = getInputValue("Parameter", "Bits setting ", "CameraSettings/Bits", None)
    dicInputValues["Capture_Exposition"]    = getInputValue("String", "Exposition (+ unit) ", True, None)
    dicInputValues["Capture_Rate"]          = getInputValue("String", "Frame rate (fps) ", False, None)
    dicInputValues["Capture_TotalExposure"] = getInputValue("String", "Total Exposure (+ unit) ", True, None)
    print ""
    print "Processing"
    print "----------"
    dicInputValues["Processing_Pre-processingSoftware"] = getInputValue("Parameter", "Pre-processing software ", "Software/Pre-processing", None)
    dicInputValues["Processing_StackingSoftware"]       = getInputValue("Parameter", "Stacking software ", "Software/Stacking", None)
    dicInputValues["Processing_ImagesProcessed"]        = getInputValue("String", "# images processed (detailed captured, stacked, darks,...) ", True, None)
    dicInputValues["Processing_ProcessingSoftware"]     = getInputValue("Parameter", "Processing software ", "Software/Processing", None)
    dicInputValues["Processing_RenderingSoftware"]      = getInputValue("Parameter", "Final rendering software ", "Software/Rendering", None)
    dicInputValues["Processing_AdditionalInfo"]         = getInputValue("String", "Additional info (resize,...) ", False, None)

    return dicInputValues

# Constants
iFinalPictureMarginWidth = 20 # Margin for the final picture         
iMarginPicture = 5            # Margin around the picture, inside the border   
iMarginTopPicture = 20        # Margin above the picture, below the title/subtitle 
iMarginBottomPicture = 20     # Margin below the picture, above the logo and data 
iBorderSize = 1               # Border around the picture
iDataInfoHeight = 300         # height of data info display at the bottom    
iPositionWinjuposX = 200      # position of the Winjupos, from the right edge (+margin)    
iPositionWinjuposY = 100      # position of the Winjupos, from  the border around the picture (+ margin)   
iDataTextInterligne = 3       # interline in pixel between data text lines
iMarginSignature = 5          # Margin for signature related to inside border of picture
fMiniatureHeight = 96.0       # Height of miniature image for Moon

DATA_TITLE_TELESCOPE = "MATERIEL  "
DATA_TITLE_CAPTURE = "CAPTURE  "
DATA_TITLE_PROCESSING = "TRAITEMENT  "

imgWinjupos = None
imgPicture = None

# get inputs from Json file or from keyboard
print ""
print ""
sJsonFilename = getInputValue("Filename", "Name of PJSON parameters file to use", False, ".json")
if sJsonFilename != "":
    with open(sJsonFilename, 'r') as fp:
        dicInputValues = json.load(fp)
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
        theColorSignature       = (228,228,228,255) # if moon. border and signature moe bright
    else:
        theColorSignature       = (128,128,128,255)
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
    sField_Date      = "Février"
    sField_Date      = str(dicInputValues["TimeLoc_Date"][8:]) + " "  + sField_Date + " " 
    sField_Date      = sField_Date + str(dicInputValues["TimeLoc_Date"][0:4]) + "  "
    sField_Date      = sField_Date + str(dicInputValues["TimeLoc_Time"][0:2]) + ":" + str(dicInputValues["TimeLoc_Time"][3:])
    sField_Date      = sField_Date + " GMT"
    sField_Location  = dicInputValues["TimeLoc_Location"]
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonAge"], "Lune: age ", "", "", "")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonIllumination"], "illum. ", "%", sField_MoonEphem, " - ")
    sField_MoonEphem = addInfoToString(dicInputValues["Info_MoonColongitude"], "colong. ", "", sField_MoonEphem, " - ")
    
    sField_Title     = dicInputValues["Subject_Title"]
    if bIsMoonPicture:
        sField_SubTitle1 = ""
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
        
    sField_Hardware_Title = DATA_TITLE_TELESCOPE
    sField_Hardware_1 = addInfoToString(dicInputValues["Hardware_Optic"], "", "", "", "")
    sField_Hardware_1 = addInfoToString(dicInputValues["Hardware_Mount"], "", "", sField_Hardware_1, " - ")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_ADC"], "ADC ", "", "", "")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_Reducer"], "", "", sField_Hardware_2, " - ")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_Barlow"], "Barlow ", "", sField_Hardware_2, " - ")
    sField_Hardware_2 = addInfoToString(dicInputValues["Hardware_Filter"], "Filtre ", "", sField_Hardware_2, " - ")
    sField_Hardware_3 = addInfoToString(dicInputValues["Hardware_Camera"], "Camera ", "", "", "")
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
    print "     Field_MoonEphem:         " + sField_MoonEphem
    print ""
    print "     Field_Title:             " + sField_Title
    print "     Field_SubTitle1:         " + sField_SubTitle1
    print "     Field_SubTitle2:         " + sField_SubTitle2
    print "     Field_SubTitle3:         " + sField_SubTitle3
    print ""
    print "     Field_Hardware 1:        " + (DATA_TITLE_TELESCOPE + "              ")[0:15] + sField_Hardware_1
    print "     Field_Hardware 2:        " + "               " + sField_Hardware_2
    print "     Field_Hardware 3:        " + "               " + sField_Hardware_3
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
    iTechnicalDataInfoHeight = theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Hardware_2, font=theInfoDataFont)[1] + iDataTextInterligne
    iTechnicalDataInfoHeight = iTechnicalDataInfoHeight + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
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
    iField_MoonEphem_X  = iFinalPictureMarginWidth
    iField_MoonEphem_Y  = iField_Location_Y + theTempDraw.textsize(sField_Location, font=theGeoDataFont)[1] + iDataTextInterligne

    iField_Title_X     = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_Title, font=theTitleFont)[0]) / 2
    iField_Title_Y     = iFinalPictureMarginWidth + (iTopInfoHeight - iTitleAndSubtitleHeight) / 2
    iField_SubTitle1_X = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[0]) / 2
    iField_SubTitle1_Y = iField_Title_Y + theTempDraw.textsize(sField_Title, font=theTitleFont)[1] + iDataTextInterligne * 5
    iField_SubTitle2_X = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[0]) / 2
    iField_SubTitle2_Y = iField_SubTitle1_Y + theTempDraw.textsize(sField_SubTitle1, font=theSubTitleFont)[1] + iDataTextInterligne
    iField_SubTitle3_X = iFinalPictureMarginWidth + (iPictureWithBorderWidth - theTempDraw.textsize(sField_SubTitle3, font=theSubTitleFont)[0]) / 2
    iField_SubTitle3_Y = iField_SubTitle2_Y + theTempDraw.textsize(sField_SubTitle2, font=theSubTitleFont)[1] + iDataTextInterligne

    iField_Object_Data_1_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[0]
    iField_Object_Data_1_Y = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Object_Data_2_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[0]
    iField_Object_Data_2_Y = iField_Object_Data_1_Y + theTempDraw.textsize(sField_Object_Data_1, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Object_Data_3_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[0]
    iField_Object_Data_3_Y = iField_Object_Data_2_Y + theTempDraw.textsize(sField_Object_Data_2, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Object_Data_4_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[0]
    iField_Object_Data_4_Y = iField_Object_Data_3_Y + theTempDraw.textsize(sField_Object_Data_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Object_Data_5_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[0]
    iField_Object_Data_5_Y = iField_Object_Data_4_Y + theTempDraw.textsize(sField_Object_Data_4, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Object_Data_6_X = iFinalImageWidth - iFinalPictureMarginWidth - theTempDraw.textsize(sField_Object_Data_6, font=theInfoDataFont)[0]
    iField_Object_Data_6_Y = iField_Object_Data_5_Y + theTempDraw.textsize(sField_Object_Data_5, font=theInfoDataFont)[1] + iDataTextInterligne

    iSizeMax_Title_Data = theTempDraw.textsize(sField_Hardware_Title, font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Data_Capture_Title, font=theInfoDataFont)[0] > iSizeMax_Title_Data: iSizeMax_Title_Data = theTempDraw.textsize(sField_Data_Capture_Title, font=theInfoDataFont)[0]
    if theTempDraw.textsize(sField_Data_Processing_Title, font=theInfoDataFont)[0] > iSizeMax_Title_Data: iSizeMax_Title_Data = theTempDraw.textsize(sField_Data_Processing_Title, font=theInfoDataFont)[0]
    
    iField_Hardware_Title_X        = iFinalPictureMarginWidth
    iField_Hardware_Title_Y        = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Hardware_1_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Hardware_1_Y            = iFinalPictureMarginWidth + iTopInfoHeight + iMarginTopPicture + iPictureWithBorderHeight + iMarginBottomPicture
    iField_Hardware_2_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Hardware_2_Y            = iField_Hardware_1_Y + theTempDraw.textsize(sField_Hardware_1, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Hardware_3_X            = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Hardware_3_Y            = iField_Hardware_2_Y + theTempDraw.textsize(sField_Hardware_2, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Capture_Title_X    = iFinalPictureMarginWidth
    iField_Data_Capture_Title_Y    = iField_Hardware_3_Y + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Capture_X          = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Data_Capture_Y          = iField_Hardware_3_Y + theTempDraw.textsize(sField_Hardware_3, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Processing_Title_X = iFinalPictureMarginWidth
    iField_Data_Processing_Title_Y = iField_Data_Capture_Y + theTempDraw.textsize(sField_Data_Capture, font=theInfoDataFont)[1] + iDataTextInterligne
    iField_Data_Processing_X       = iSizeMax_Title_Data + iFinalPictureMarginWidth
    iField_Data_Processing_Y       = iField_Data_Capture_Y + theTempDraw.textsize(sField_Data_Capture, font=theInfoDataFont)[1] + iDataTextInterligne

    # create new bitmap
    theFinalImg = Image.new( 'RGBA', (iFinalImageWidth, iFinalImageHeight), (0, 0, 0, 255))
    theFinalDraw = ImageDraw.Draw(theFinalImg)
    
    # paste Winjupos             
    if dicInputValues["Bitmap_WinjuposFileName"] != "":
        theFinalImg.paste(imgWinjupos, (iWinjuposPositionX, iWinjuposPositionY))
    
    # Display fields
    theFinalDraw.text((iField_Date_X,      iField_Date_Y),      sField_Date,      theColorDataText, font=theGeoDataFont)
    theFinalDraw.text((iField_Location_X,  iField_Location_Y),  sField_Location,  theColorDataText, font=theGeoDataFont)
    theFinalDraw.text((iField_MoonEphem_X, iField_MoonEphem_Y), sField_MoonEphem, theColorDataText, font=theGeoDataFont)
    
    theFinalDraw.text((iField_Title_X,     iField_Title_Y),     sField_Title,     theColorTitle,    font=theTitleFont)
    theFinalDraw.text((iField_SubTitle1_X, iField_SubTitle1_Y), sField_SubTitle1, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_SubTitle2_X, iField_SubTitle2_Y), sField_SubTitle2, theColorSubTitle, font=theSubTitleFont)
    theFinalDraw.text((iField_SubTitle3_X, iField_SubTitle3_Y), sField_SubTitle3, theColorSubTitle, font=theSubTitleFont)
    
    theFinalDraw.text((iField_Object_Data_1_X, iField_Object_Data_1_Y), sField_Object_Data_1, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_1 != "" and bIsMoonPicture: theFinalDraw.text((iField_Object_Data_1_X, iField_Object_Data_1_Y), dicInputValues["Info_MoonFeature0_Name"], theColorDataTitle, font=theInfoDataFont)
    theFinalDraw.text((iField_Object_Data_2_X, iField_Object_Data_2_Y), sField_Object_Data_2, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_2 != "" and bIsMoonPicture: theFinalDraw.text((iField_Object_Data_2_X, iField_Object_Data_2_Y), dicInputValues["Info_MoonFeature1_Name"], theColorDataTitle, font=theInfoDataFont)
    theFinalDraw.text((iField_Object_Data_3_X, iField_Object_Data_3_Y), sField_Object_Data_3, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_3 != "" and bIsMoonPicture: theFinalDraw.text((iField_Object_Data_3_X, iField_Object_Data_3_Y), dicInputValues["Info_MoonFeature2_Name"], theColorDataTitle, font=theInfoDataFont)
    theFinalDraw.text((iField_Object_Data_4_X, iField_Object_Data_4_Y), sField_Object_Data_4, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_4 != "" and bIsMoonPicture: theFinalDraw.text((iField_Object_Data_4_X, iField_Object_Data_4_Y), dicInputValues["Info_MoonFeature3_Name"], theColorDataTitle, font=theInfoDataFont)
    theFinalDraw.text((iField_Object_Data_5_X, iField_Object_Data_5_Y), sField_Object_Data_5, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_5 != "" and bIsMoonPicture: theFinalDraw.text((iField_Object_Data_5_X, iField_Object_Data_5_Y), dicInputValues["Info_MoonFeature4_Name"], theColorDataTitle, font=theInfoDataFont)
    theFinalDraw.text((iField_Object_Data_6_X, iField_Object_Data_6_Y), sField_Object_Data_6, theColorDataText, font=theInfoDataFont)
    if sField_Object_Data_6 != "" and bIsMoonPicture: theFinalDraw.text((iField_Object_Data_6_X, iField_Object_Data_6_Y), dicInputValues["Info_MoonFeature5_Name"], theColorDataTitle, font=theInfoDataFont)
    
    theFinalDraw.text((iField_Hardware_1_X, iField_Hardware_1_Y), sField_Hardware_1, theColorDataText,  font=theInfoDataFont)
    theFinalDraw.text((iField_Hardware_Title_X, iField_Hardware_Title_Y), sField_Hardware_Title, theColorDataTitle, font=theInfoDataFont)
    if sField_Hardware_2 != "": theFinalDraw.text((iField_Hardware_2_X, iField_Hardware_2_Y), sField_Hardware_2, theColorDataText,  font=theInfoDataFont)
    if sField_Hardware_3 != "": theFinalDraw.text((iField_Hardware_3_X, iField_Hardware_3_Y), sField_Hardware_3, theColorDataText,  font=theInfoDataFont)
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

    # Add miniature for Moon
    if bIsMoonPicture:
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
        iMiniature_X = iMiniature_X - iMarginBottomPicture - iMiniatureWidth
        iMiniature_Y = iField_Object_Data_1_Y
        theFinalDraw.rectangle((iMiniature_X, iMiniature_Y, iMiniature_X + iMiniatureWidth + 1, iMiniature_Y + iMiniatureHeight), outline=theColorDataTitle, fill=(255, 0, 0, 255))
        theFinalImg.paste(imgMiniature, (iMiniature_X + 1 , iMiniature_Y + 1 ))
        
    
    # Save image
    theFinalImg.save(sOutputFileName + ".png", "PNG")
    print ""
    print " --> created picture: " + sOutputFileName + ".png"
    print ""
    print ""

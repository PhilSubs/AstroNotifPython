#!/usr/bin/python2.7
# coding: utf8 

from __future__ import unicode_literals

import json
import os.path
import datetime
import sys
try:
    import piexif
    bEXIFOptionEnabled = True
except ImportError:
    bEXIFOptionEnabled = False
from PIL import Image, ImageDraw, ImageFont

def _getInput(sLabel, sDefaultValue = ""):
    if len(sDefaultValue) != 0:
        sLabelDisplayed = sLabel + " [" + sDefaultValue + "]"
    else:
        sLabelDisplayed = sLabel
    sLabelDisplayed = sLabelDisplayed + "   "
    sValue = raw_input(sLabelDisplayed)
    if len(sDefaultValue) != 0 and len(sValue) == 0:
        sValue = sDefaultValue
    return sValue.lower()

def _getRescaledSize(iPictureSizeX, iPictureSizeY, idealPictureSizeX, idealPictureSizeY):
    iNewSizeX = iPictureSizeX
    iNewSizeY = iPictureSizeY
    if iNewSizeX >= iNewSizeY:
        #print "_getRescaledSize  ... landscape mode..."
        # resize X first
        if iNewSizeX > idealPictureSizeX:
            iNewSizeY = int((float(idealPictureSizeX) / float(iNewSizeX)) * float(iNewSizeY))
            iNewSizeX = idealPictureSizeX
            #print "_getRescaledSize  ... resize X first... " + str(iNewSizeX) + "x" + str(iNewSizeY)
        # then resze Y if needed
        if iNewSizeY > idealPictureSizeY:
            iNewSizeX = int((float(idealPictureSizeY) / float(iNewSizeY)) * float(iNewSizeX))
            iNewSizeY = idealPictureSizeY
            #print "_getRescaledSize  ... then resze Y... " + str(iNewSizeX) + "x" + str(iNewSizeY)
    else:
        #print "_getRescaledSize  ... portrait mode..."
        # resize Y first
        if iNewSizeY > idealPictureSizeY:
            iNewSizeX = int((float(idealPictureSizeY) / float(iNewSizeY)) * float(iNewSizeX))
            iNewSizeY = idealPictureSizeY
            #print "_getRescaledSize  ... resize Y first... " + str(iNewSizeX) + "x" + str(iNewSizeY)
        # then resze X if needed
        if iNewSizeX > idealPictureSizeX:
            iNewSizeY = int((float(idealPictureSizeX) / float(iNewSizeX)) * float(iNewSizeY))
            iNewSizeX = idealPictureSizeX
            #print "_getRescaledSize  ... then resze X... " + str(iNewSizeX) + "x" + str(iNewSizeY)
    # return new sizes
    return iNewSizeX, iNewSizeY
    
def _computePictureResize(iPictureSizeX, iPictureSizeY, sResizeType):
    newPictureSizeX = iPictureSizeX
    newPictureSizeY = iPictureSizeY
    idealPictureSizeX = iPictureSizeX
    idealPictureSizeY = iPictureSizeY
    if sResizeType == "i":
        if newPictureSizeX == newPictureSizeY:
            # portrait mode size for Instagram is 1080x1080
            idealPictureSizeX = 1080
            idealPictureSizeY = 1080
        elif newPictureSizeX > newPictureSizeY:
            # paysage mode size for Instagram is 1080×566
            idealPictureSizeX = 1080
            idealPictureSizeY = 566
        else:
            # portrait mode size for Instagram is 1080×1350
            idealPictureSizeX = 1080
            idealPictureSizeY = 1350
    elif sResizeType == "f":
        if newPictureSizeX >= newPictureSizeY:
            # paysage mode size for fullHD is 1920x1080
            idealPictureSizeX = 1920
            idealPictureSizeY = 1080
        else:
            # portrait mode size for fullHD is 1080x1920
            idealPictureSizeX = 1080
            idealPictureSizeY = 1920
    elif sResizeType == "h":
        if newPictureSizeX >= newPictureSizeY:
            # paysage mode size for fullHD is 1280×720
            idealPictureSizeX = 1280
            idealPictureSizeY = 720
        else:
            # portrait mode size for fullHD is 720x1280
            idealPictureSizeX = 720
            idealPictureSizeY = 1280
            
    newPictureSizeX, newPictureSizeY = _getRescaledSize(iPictureSizeX, iPictureSizeY, idealPictureSizeX, idealPictureSizeY)
    return ((newPictureSizeX != iPictureSizeX) or (newPictureSizeY != iPictureSizeY)), newPictureSizeX, newPictureSizeY, idealPictureSizeX, idealPictureSizeY

def _computeSignatureSizePercentage(iPictureSizeX, iPictureSizeY):
    iMinSize = 100
    if iPictureSizeX > iPictureSizeY:
        iSize = int(float(iPictureSizeX) / 11.0)
        if iSize < iMinSize:
            iSize = iMinSize
        iPercent = int(float(iSize) / float(iPictureSizeX) * 100.0)
    else:
        iSize = int(float(iPictureSizeY) / 6.0)
        if iSize < iMinSize:
            iSize = iMinSize
        iPercent = int(float(iSize) / float(iPictureSizeY) * 100.0)
    return iPercent
    
bAbort = False
print sys.argv[0]

print ""

# Get signature file
sSignatureFilename = _getInput("Signature filename                                                        ", "Signature-2018G-1.png")
imgSignatureFile = Image.open(sSignatureFilename)
iSignatureSizeX, iSignatureSizeY = imgSignatureFile.size

# Get photo file
sPhotoFilename = _getInput("Photo filename                                                            ")
imgPhotoFile = Image.open(sPhotoFilename)
iPhotoOriginalSizeX, iPhotoOriginalSizeY = imgPhotoFile.size
iPhotoSizeX, iPhotoSizeY = imgPhotoFile.size

#
print ""

# get additional parameters
sResizeImageType         = _getInput("Resize image ?      [N]o  [I]nstagram  [F]ullHD_1920x1080  [H]D_1280x720  ", "N")

# Resize picture if needed
isResizeNeeded, newPictureSizeX, newPictureSizeY, idealPictureSizeX, idealPictureSizeY = _computePictureResize(iPhotoSizeX, iPhotoSizeY, sResizeImageType)
if isResizeNeeded:
    imgPhotoFile.thumbnail((newPictureSizeX, newPictureSizeY), Image.ANTIALIAS)
    iPhotoSizeX = newPictureSizeX
    iPhotoSizeY = newPictureSizeY
    sResizeInfoMessage = "resized to fit ideal size of " + str(idealPictureSizeX) + "x" + str(idealPictureSizeY)
else:
    sResizeInfoMessage = "already fits ideal size of " + str(idealPictureSizeX) + "x" + str(idealPictureSizeY)

# compute proposed values for parameters
iPercentSizeSignatureProposed = _computeSignatureSizePercentage(iPhotoSizeX, iPhotoSizeY)
iMarginProposed = int(float(iPhotoSizeX) * 0.03)

# get remaining paameters
sPositionTopBottom       = _getInput("Signature Vertical Position ?                 [T]op   [B]ottom  [C]enter  ", "B")
sPositionLeftRight       = _getInput("Signature Horizontal Position ?               [L]eft  [R]ight   [C]enter  ", "R")
sSignatureSize           = _getInput("Signature width in px or % ?                           (ex. 100px or 5%)  ", str(iPercentSizeSignatureProposed) + "%")
sSignaturePadding        = _getInput("Signature Padding in px ?                                    (ex. 100px)  ", str(iMarginProposed) + "px")
sSignatureOpacity        = _getInput("Signature Opacity in % ?                                       (ex. 70%)  ", "50%")
sJPEGQuality             = _getInput("JPEG Quality in % ?                                            (ex. 90%)  ", "90%")
if bEXIFOptionEnabled: 
    sCopyEXIFData = _getInput("Copy EXIF data from original ?                               [Y]es  [N]o  ", "Y")
else:
    print "EXIF option is DISABLED"
    sCopyEXIFData = "n"


# process parameters
iSignaturePaddingValue = int(sSignaturePadding[:len(sSignaturePadding) - 2])
iSignatureOpacityValue = int(sSignatureOpacity[:len(sSignatureOpacity) - 1])
iJPEGQualityValue = int(sJPEGQuality[:len(sJPEGQuality) - 1])
bCopyEXIFData = (sCopyEXIFData == "y")

# compute signature display size
iMinSignatureSizeX = 100
if sSignatureSize.find("%") > 0:
    iSignatureSizeValue = int(sSignatureSize[:len(sSignatureSize) - 1])
    iSignatureDisplaySizeX = int(float(iPhotoSizeX) * float(iSignatureSizeValue) / 100.0)
    fCoeff = float(iSignatureDisplaySizeX) / float(iSignatureSizeX)
    iSignatureDisplaySizeY = int(float(iSignatureSizeY) * fCoeff)
    if iSignatureDisplaySizeX < iMinSignatureSizeX:
        iSignatureDisplaySizeX = iMinSignatureSizeX
        fCoeff = float(iSignatureDisplaySizeX) / float(iSignatureSizeX)
        iSignatureDisplaySizeY = int(float(iSignatureSizeY) * fCoeff)
elif sSignatureSize.find("px") > 0:
    iSignatureSizeValue = int(sSignatureSize[:len(sSignatureSize) - 2])
    iSignatureDisplaySizeX = iSignatureSizeValue
    fCoeff = float(iSignatureDisplaySizeX) / float(iSignatureSizeX)
    iSignatureDisplaySizeY = int(iSignatureSizeY * fCoeff)
else:
    print "Error - invalid signature size (" + sSignatureSize + ":     %:" + str(sSignatureSize.find("%")) + "     px:" + str(sSignatureSize.find("px")) + ")"
    bAbort = True
    
# compute signature position
if sPositionTopBottom == "t":
    iSignaturePositionY = iSignaturePaddingValue + 1
elif sPositionTopBottom == "b":
    iSignaturePositionY = iPhotoSizeY - iSignatureDisplaySizeY - iSignaturePaddingValue - 1
elif sPositionTopBottom == "c":
    iSignaturePositionY = iSignaturePaddingValue + (iPhotoSizeY - iSignatureDisplaySizeY) / 2
else:
    print "Error - invalid signature position Top/Bottom (" + sPositionTopBottom + ")"
    bAbort = True
if sPositionLeftRight == "l":
    iSignaturePositionX = iSignaturePaddingValue + 1
elif sPositionLeftRight == "r":
    iSignaturePositionX = iPhotoSizeX - iSignatureDisplaySizeX - iSignaturePaddingValue - 1
elif sPositionLeftRight == "c":
    iSignaturePositionX = iSignaturePaddingValue + (iPhotoSizeX - iSignatureDisplaySizeX) / 2
else:
    print "Error - invalid signature position Left/Right (" + sPositionLeftRight + ")"
    bAbort = True

# Compute final image    
if not bAbort:
    print ""
    print ""
    print "Image:         original size........:  " + str(iPhotoOriginalSizeX) + "x" + str(iPhotoOriginalSizeY)
    if sResizeImageType == "i":
        print "               resize ..............:  Instagram"
    elif sResizeImageType == "F":
        print "               resize ..............:  FullHD 1920x1080"
    elif sResizeImageType == "i":
        print "               resize ..............:  HD 1280x720"
    else:
        print "               resize ..............:  None"
    print "               final size ..........:  " + str(iPhotoSizeX) + "x" + str(iPhotoSizeY) + "     (" + sResizeInfoMessage + ")"
    print "               quality..............:  " + sJPEGQuality
    if bEXIFOptionEnabled:
       if bCopyEXIFData:
          print "               exif option..........:  Yes"
       else:
          print "               exif option..........:  No"
    else:
        print "               exif option..........:  disabled"
    print ""
    print "Signature:     original size........:  " + str(iSignatureSizeX) + "x" + str(iSignatureSizeY)
    print "               displayed size.......:  " + str(iSignatureDisplaySizeX) + "x" + str(iSignatureDisplaySizeY)
    print "               displayed position...:  X:" + str(iSignaturePositionX) + "  Y:" + str(iSignaturePositionY)
    print "               opacity..............:  " + sSignatureOpacity
    
    # compute final image name
    sImageNameInfo = "IMAGE["
    sImageNameInfo = sImageNameInfo + str(iPhotoSizeX) +  "x" + str(iPhotoSizeY) + "_"
    if sResizeImageType != "n": sImageNameInfo = sImageNameInfo + "r" + sResizeImageType.upper() + "_"
    sImageNameInfo = sImageNameInfo + "q" + str(iJPEGQualityValue)
    if bCopyEXIFData: sImageNameInfo = sImageNameInfo + "_exif"
    sImageNameInfo = sImageNameInfo + "]"

    sImageNameSignInfo = "SIGN["
    sImageNameSignInfo = sImageNameSignInfo + "s"  + sSignatureSize + "_"
    sImageNameSignInfo = sImageNameSignInfo + "p"  + str(iSignaturePaddingValue) + "_"
    sImageNameSignInfo = sImageNameSignInfo + "o"  + str(iSignatureOpacityValue)
    sImageNameSignInfo = sImageNameSignInfo + "]"
    
    sFinalImageFilename = sPhotoFilename.replace(".", "___" + sImageNameInfo + "_" + sImageNameSignInfo + ".")
            
    # resize signature
    imgSignatureFile.thumbnail((iSignatureDisplaySizeX, iSignatureDisplaySizeY), Image.ANTIALIAS)
    if imgSignatureFile.mode!='RGBA':
        alpha = Image.new('L', imgSignatureFile.size, 255)
        imgSignatureFile.putalpha(alpha)

    # Add signature
    paste_mask = imgSignatureFile.split()[3].point(lambda i: i * iSignatureOpacityValue / 100.0)
    imgPhotoFile.paste(imgSignatureFile, (iSignaturePositionX,iSignaturePositionY), mask=paste_mask)

    # copy EXIF (if needed)  and save final image
    if bCopyEXIFData:
        exif_dict = piexif.load(sPhotoFilename)
        exif_bytes = piexif.dump(exif_dict)
        imgPhotoFile.save(sFinalImageFilename, format='JPEG', subsampling=0, quality=iJPEGQualityValue, exif=exif_bytes)
    else:
        imgPhotoFile.save(sFinalImageFilename, format='JPEG', subsampling=0, quality=iJPEGQualityValue)

    print ""
    print "Image created: " + sFinalImageFilename
    print ""
    
    print ""
    sClose = raw_input("Taper ENTER pour quitter")
    
    
    
    

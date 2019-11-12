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
        iSize = int(float(iPictureSizeX) / 12.0)
        if iSize < iMinSize:
            iSize = iMinSize
        iPercent = int(float(iSize) / float(iPictureSizeX) * 100.0)
    else:
        iSize = int(float(iPictureSizeY) / 7.0)
        if iSize < iMinSize:
            iSize = iMinSize
        iPercent = int(float(iSize) / float(iPictureSizeY) * 100.0)
    return iPercent

def _computeSignatureOpacity(imgPhoto, iSignaturePositionX, iSignaturePositionY, iSignatureSizeX, iSignatureSizeY):
    dAvgLuminance = 0.0
    dNbPixels = float(iSignatureSizeX * iSignatureSizeY)
    imPhoto = imgPhoto.load()
    for x in range(iSignatureSizeX):
        for y in range(iSignatureSizeY):
            tupColor = imPhoto[iSignaturePositionX + x, iSignaturePositionY + y]
            dAvgLuminance = dAvgLuminance + (((0.3 * float(tupColor[0]) + 0.6 * float(tupColor[1]) + 0.1 * float(tupColor[2])))  / dNbPixels)
    print "     Signature Zone " + str(iSignaturePositionX) + "," + str(iSignaturePositionY) + " - " + str(iSignaturePositionX + iSignatureSizeX) + "," + str(iSignaturePositionY + iSignatureSizeY) + "   Luminance: " + str(int(dAvgLuminance)) + "  (" + str(int(dAvgLuminance/2.55)) + "%)"
    iReturnValue = dAvgLuminance / 255.0 * 100.0
    if iReturnValue <= 10.0:
        iReturnValue = iReturnValue * 3.0
    elif iReturnValue < 20.0:
        iReturnValue = iReturnValue * 2.0
    elif iReturnValue < 30.0:
        iReturnValue = iReturnValue * 1.5
    elif iReturnValue < 40.0:
        iReturnValue = iReturnValue * 1.3
    elif iReturnValue < 50.0:
        iReturnValue = iReturnValue * 1.1
    else:
        iReturnValue = iReturnValue * 0.6
    iReturnValue = int(iReturnValue)
    if iReturnValue > 100: iReturnValue = 100
    if iReturnValue < 15: iReturnValue = 15
    return iReturnValue

bAbort = False
print sys.argv[0]

print ""

# Get Photo Title
sPhotoTitle = raw_input("Title             ")

# Get signature file
sSignatureFilename = _getInput("Signature filename", "Signature-2018G-1.png")
imgSignatureFile = Image.open(sSignatureFilename)
iSignatureSizeX, iSignatureSizeY = imgSignatureFile.size
print "          Size: " + str(iSignatureSizeX) + "x" + str(iSignatureSizeY)

# Get photo file
sPhotoFilename = _getInput("Photo filename")
imgPhotoFile = Image.open(sPhotoFilename)
iPhotoSizeX, iPhotoSizeY = imgPhotoFile.size
print "          Size: " + str(iPhotoSizeX) + "x" + str(iPhotoSizeY)

#
print ""

# get additional parameters
sResizeImageType         = _getInput("Resize image ?              [N]o  / [I]nstagram / [F]ullHD 1920x1080 / [H]D 1280x720", "N")

# Resize picture if needed
isResizeNeeded, newPictureSizeX, newPictureSizeY, idealPictureSizeX, idealPictureSizeY = _computePictureResize(iPhotoSizeX, iPhotoSizeY, sResizeImageType)
if isResizeNeeded:
    imgPhotoFile.thumbnail((newPictureSizeX, newPictureSizeY), Image.ANTIALIAS)
    iPhotoSizeX = newPictureSizeX
    iPhotoSizeY = newPictureSizeY
    print "     Picture will be resized to " + str(iPhotoSizeX) + "x" + str(iPhotoSizeY) + " to fit ideal size of " + str(idealPictureSizeX) + "x" + str(idealPictureSizeY)
else:
    print "     No need to resize the picture...   " + str(iPhotoSizeX) + "x" + str(iPhotoSizeY) + " already fits ideal size of " + str(idealPictureSizeX) + "x" + str(idealPictureSizeY)

# compute proposed values for parameters
iPercentSizeSignatureProposed = _computeSignatureSizePercentage(iPhotoSizeX, iPhotoSizeY)
if int(float(iPhotoSizeX) * 0.02) > int(float(iPhotoSizeY) * 0.02):
    iMarginProposed = int(float(iPhotoSizeY) * 0.02)
else:
    iMarginProposed = int(float(iPhotoSizeX) * 0.02)

# get remaining parameters
sPositionTopBottom       = _getInput("Signature Position ?        [T]op  / [B]ottom / [C]enter", "B")
sPositionLeftRight       = _getInput("Signature Position ?        [L]eft / [R]ight  / [C]enter", "R")
sSignatureSize           = _getInput("Signature width in px or % ?           (ex. 100px or 5%)", str(iPercentSizeSignatureProposed) + "%")
sSignaturePadding        = _getInput("Signature Padding in px ?                    (ex. 100px)", str(iMarginProposed) + "px")


# process parameters
iSignaturePaddingValue = int(sSignaturePadding[:len(sSignaturePadding) - 2])

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

# get Default Opacity
iDefaultOpacity = _computeSignatureOpacity(imgPhotoFile, iSignaturePositionX, iSignaturePositionY, iSignatureDisplaySizeX, iSignatureDisplaySizeY)

# get remaining parameters
sSignatureOpacity = _getInput("Signature Opacity in % ?                       (ex. 70%)", str(iDefaultOpacity) + "%")
sJPEGQuality      = _getInput("JPEG Quality in % ?                            (ex. 90%)", "90%")
if bEXIFOptionEnabled:
    sCopyEXIFData = _getInput("Copy EXIF data from original ?              [Y]es / [N]o", "Y")
else:
    sCopyEXIFData = "n"

# process parameters
iSignatureOpacityValue = int(sSignatureOpacity[:len(sSignatureOpacity) - 1])
iJPEGQuality = int(sJPEGQuality[:len(sJPEGQuality) - 1])
bCopyEXIFData = (sCopyEXIFData == "y")

# Compute final image    
if not bAbort:
    print ""
    print "Signature:"
    print "            displayed size: " + str(iSignatureDisplaySizeX) + "x" + str(iSignatureDisplaySizeY)
    print "            displayed position:   X:" + str(iSignaturePositionX) + "    Y:" + str(iSignaturePositionY)
    print "            Opacity: " + sSignatureOpacity
    
    # compute final image name
    sFinalImageFilename = sPhotoFilename.replace(".", ".")
    sFinalImageFilename = sFinalImageFilename.replace(".", "_" + str(iPhotoSizeX) +  "x" + str(iPhotoSizeY) + ".")
    if sResizeImageType != "n": sFinalImageFilename = sFinalImageFilename.replace(".", "_Resz-" + sResizeImageType + ".")
    sFinalImageFilename = sFinalImageFilename.replace(".", "_Qa" + sJPEGQuality + ".")
    sFinalImageFilename = sFinalImageFilename.replace(".", "_Op" + sSignatureOpacity + ".")
    sFinalImageFilename = sFinalImageFilename.replace(".", "_Sz" + sSignatureSize + ".")
    sFinalImageFilename = sFinalImageFilename.replace(".", "_Pd" + sSignaturePadding + ".")
    if bCopyEXIFData: sFinalImageFilename = sFinalImageFilename.replace(".", "_Exif.")
    sFinalImageFilename = sPhotoTitle + " -- " + sFinalImageFilename

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
        # Add image name in "artist" tag, just after Philippe larosa
        exif_dict['0th'][315] = exif_dict['0th'][315] + "  (".encode('utf8') + sPhotoTitle.encode('utf8') + " -- ".encode('utf8') + sFinalImageFilename.encode('utf8') + ")".encode('utf8')
        exif_bytes = piexif.dump(exif_dict)
        imgPhotoFile.save(sFinalImageFilename, format='JPEG', subsampling=0, quality=iJPEGQuality, exif=exif_bytes)
    else:
        pass
        imgPhotoFile.save(sFinalImageFilename, format='JPEG', subsampling=0, quality=iJPEGQuality)

    print ""
    print "Image created: " + sFinalImageFilename
    print ""
    
    print ""
    sClose = raw_input("Taper ENTER pour quitter")
    
    
    
    

#!/usr/bin/python2.7
# coding: utf8 
#
# Rename all ".jpg" files in current dir with name taken from "Artist" tag in EXIF
#
#

from __future__ import unicode_literals

import json
import os
import datetime
import sys

try:
    import piexif
    bEXIFOptionEnabled = True
except ImportError:
    bEXIFOptionEnabled = False
from PIL import Image, ImageDraw, ImageFont


# Loop through jpg files in current folder
sCurrentPath = os.getcwd()
for file in os.listdir(sCurrentPath):
    if file.endswith(".jpg"):
        sCurrentFileName = os.path.join(sCurrentPath, file)
        # get EXIF from file
        if not bEXIFOptionEnabled:
            print "EXIF not enabled -- Cannot rename file " + sCurrentFileName
        else:
            exif_dict = piexif.load(sCurrentFileName)
            sNewFileName = exif_dict['0th'][315]
            # Remove Name and parenthesis
            sNewFileName = sNewFileName[sNewFileName.find("("):]
            sNewFileName = sNewFileName[:len(sNewFileName) - 1]
            sNewFileName = sCurrentPath + sNewFileName.strip()
            # rename file
            try:
                os.rename(sCurrentFileName, sNewFileName)
                print "SUCCESS - File   " + sCurrentFileName + "   renamed to   " + sNewFileName
            except:
                print "ERROR   - Cannot rename file   " + sCurrentFileName + "   to   " + sNewFileName

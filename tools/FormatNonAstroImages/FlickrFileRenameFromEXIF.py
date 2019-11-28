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
        print "- File  " + sCurrentFileName
        # get EXIF from file
        if not bEXIFOptionEnabled:
            print "   EXIF not enabled -- Cannot rename file " + sCurrentFileName
        else:
            try:
                exif_dict = piexif.load(sCurrentFileName)
                sNewFileName = exif_dict['0th'][315]
            except:
                sNewFileName = ""
            if sNewFileName == "":
                print "   ERROR   - Cannot rename file   " + sCurrentFileName + "   ... can't retrieve EXIF"
            else:
                sNewFileName = exif_dict['0th'][315]
                # Remove Name and parenthesis
                sNewFileName = sNewFileName[sNewFileName.find("(")+1:]
                sNewFileName = sNewFileName[:len(sNewFileName) - 1]
                sNewFileName = os.path.join(sCurrentPath, sNewFileName.strip())
                # rename file
                try:
                    os.rename(sCurrentFileName, sNewFileName)
                    print "   SUCCESS - File   " + sCurrentFileName + " --> " + sNewFileName
                except:
                    print "   ERROR   - Cannot rename file   " + sCurrentFileName + "   to   " + sNewFileName

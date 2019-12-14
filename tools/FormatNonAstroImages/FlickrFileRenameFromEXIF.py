#!/usr/bin/python2.7
# coding: utf8 
#
# Rename all ".jpg" files in current dir with name taken from "Artist" tag in EXIF
#
#

from __future__ import unicode_literals

import json
import os
import logging

try:
    import piexif
    bEXIFOptionEnabled = True
except ImportError:
    bEXIFOptionEnabled = False

# Options
logging.basicConfig(level=logging.INFO)
logging.debug("Option EXIF {}".format(bEXIFOptionEnabled))


# Loop through jpg files in current folder
sCurrentPath = os.getcwd()
for file in os.listdir(sCurrentPath):
    if file.endswith(".jpg"):
        sCurrentFileName = os.path.join(sCurrentPath, file)
        logging.info("- File  {}".format(sCurrentFileName))
        # get EXIF from file
        if not bEXIFOptionEnabled:
            logging.info("   EXIF not enabled -- Cannot rename file {}".format(sCurrentFileName))
        else:
            try:
                exif_dict = piexif.load(sCurrentFileName)
                sNewFileName = exif_dict['0th'][315]
            except:
                sNewFileName = ""
            if sNewFileName == "":
                logging.info("   ERROR   - Cannot rename file   {}   ... can't retrieve EXIF".format(sCurrentFileName))
            else:
                sNewFileName = str(exif_dict['0th'][315])
                logging.info("Image {} contains following name: {}".format(sCurrentFileName, sNewFileName))
                # Remove Name and parenthesis
                sNewFileName = sNewFileName[sNewFileName.find("(")+1:]
                sNewFileName = sNewFileName[:len(sNewFileName) - 1]
                sNewFileName = os.path.join(sCurrentPath, sNewFileName.strip())
                # rename file
                try:
                    os.rename(sCurrentFileName, sNewFileName)
                    logging.info("   SUCCESS - File   {} --> {}".format(sCurrentFileName, sNewFileName))
                except:
                    logging.info("   ERROR   - Cannot rename file   {}   to   {}".format(sCurrentFileName, sNewFileName))

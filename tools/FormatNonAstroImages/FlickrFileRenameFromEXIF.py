#!/usr/bin/python2.7
# coding: utf8 
#
# Rename all ".jpg" files in current dir with name taken from "Artist" tag in EXIF
#
#

from __future__ import unicode_literals

import logging
import os
from PIL import Image

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
                # Prints the nicely formatted dictionary
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
                sTitle = sNewFileName[:sNewFileName.find(" --"):]
                sNewFileName = os.path.join(sCurrentPath, sNewFileName.strip())
                # Change EXIF
                im = Image.open(sCurrentFileName)
                exif_dict_for_change = piexif.load(im.info["exif"])
                # process im and exif_dict...
                exif_dict_for_change['0th'][270] = sTitle.strip()
                exif_bytes_for_change = piexif.dump(exif_dict_for_change)
                im.save(sCurrentFileName + ".new.jpg", "jpeg", exif=exif_bytes_for_change, subsampling=0, quality=100)
                # rename file
                try:
                    os.rename(sCurrentFileName, sNewFileName)
                    logging.info("   SUCCESS - File   {} --> {}".format(sCurrentFileName, sNewFileName))
                except:
                    logging.info("   ERROR   - Cannot rename file   {}   to   {}".format(sCurrentFileName, sNewFileName))

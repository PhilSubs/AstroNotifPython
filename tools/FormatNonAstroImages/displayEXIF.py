#!/usr/bin/python2.7
# coding: utf8 
#
# Rename all ".jpg" files in current dir with name taken from "Artist" tag in EXIF
#
#

from __future__ import unicode_literals

import logging
import pprint
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


# get filename
sFilename = input("file... ")
logging.info("- File  {}".format(sFilename))
# get EXIF from file
if not bEXIFOptionEnabled:
    logging.info("   EXIF not enabled -- Cannot read EXIF data in {}".format(sCurrentFileName))
else:
    try:
        exif_dict = piexif.load(sFilename)
        # Prints the nicely formatted dictionary
        pprint.pprint(exif_dict)
    except:
        logging.info("   ERROR   - Cannot load EXIF read from file   {}".format(sFilename))

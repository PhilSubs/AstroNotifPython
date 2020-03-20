#!/usr/bin/python2.7
# coding: utf8 
#
# Rename all "<chaine1>*.*" files in <dir> dir with "<chaine2>*.*"
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

# get parameters
sBackslash = "\\"
sDirectory = input("Repertoire.............. ")
sDirectory.replace(sBackslash, sBackslash+sBackslash)
sStringToSearch = input("Texte a remplacer....... ")
sStringToReplaceWith = input("Texte de remplacement... ")
sApplyRename = input("Renommer ? (O/N)........ ")

sStringToSearch = sStringToSearch.lower()
iLengthSearchString = len(sStringToSearch)

# Loop through jpg files in current folder
for file in os.listdir(sDirectory):
    sCurrentFileName = file.lower();
    sFullFileName = os.path.join(sDirectory, file)
    logging.info("... {}".format(sCurrentFileName))
    if sCurrentFileName[:iLengthSearchString] == sStringToSearch:
        sNewFileName = sStringToReplaceWith + sCurrentFileName[iLengthSearchString:]
        sFullNewFileName = os.path.join(sDirectory, sNewFileName)
        try:
            if sApplyRename == "O":
                os.rename(sFullFileName, os.path.join(sDirectory, sFullNewFileName))
                logging.info("- File  {}   ... renomme en   {}".format(sFullFileName, sFullNewFileName))
            else:
                logging.info("- File  {}   ... renomme (pas applique) en   {}".format(sFullFileName, sFullNewFileName))
        except:
            logging.info("  ERREUR: impossible de renommer {}   en   {}".format(sFullFileName, sFullNewFileName))

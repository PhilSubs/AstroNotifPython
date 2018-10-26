#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

#
# Paramètre de ligne de command
#
#    "resetTrace"
#    "logToTrace"               "Text"
#    "getTrace"                 
#    "getHTMLPageForTrace"      "HTML"  (facultatif:  remplave \n par <BR>\n
#



# Import libs
from datetime import datetime, timedelta
import ANLib
import sys

# get command line values
sAction = sys.argv[1]
sParameter1 = ""
if len(sys.argv) > 2: 
    sParameter1 = sys.argv[2]

# Read the parameters files
theParameters = ANLib.Parameters() # read parameters file parameters_run.json

# Actions
if sAction == "resetTrace":
    # Reset the logfile
    ANLib.Tools.resetTrace(theParameters.Runtime().get("Global.PathToLogFileName"))
elif sAction == "logToTrace":
    ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), sParameter1)
elif sAction == "getTrace":
    if sParameter1 == "HTML":
        print ANLib.Tools.getTrace(theParameters.Runtime().get("Global.PathToLogFileName")).replace("\n","<BR>\n")
    else:
        print ANLib.Tools.getTrace(theParameters.Runtime().get("Global.PathToLogFileName"))
elif sAction == "generateHTMLPageForTrace":
    sPageContent = "<HTML>\n"
    sPageContent += "	<HEAD>\n"
    sPageContent += '      <TITLE>AstroNotifLog</TITLE>\n'
    sPageContent += '      <BASE href="">\n'
    sPageContent += '      <LINK rel="icon" href="http://' + theParameters.Runtime().get('NightlyBatch.Domain') + '/favicon.png">\n'
    sPageContent += '      <LINK rel="stylesheet" href="http://' + theParameters.Runtime().get('NightlyBatch.Domain') + '/AstroNotif.css">\n'
    sPageContent += '      <META charset="UTF-8">\n'
    sPageContent += "	</HEAD>\n"
    sPageContent += "  <BODY>\n"

    sPageContent += ANLib.Tools.getTrace(theParameters.Runtime().get("Global.PathToLogFileName")).replace("\n","<BR>").replace("<BR>","<BR>\n") + "\n\n"

    sPageContent += "  </BODY>\n"    
    sPageContent += "</HTML>\n"
    
    ANLib.Tools.saveAsFileEncoded(theParameters.Runtime().get("Global.PathToWWWFolder") + ANLib.Tools.get_path_separator() + "nightlybatchlog.html", sPageContent)

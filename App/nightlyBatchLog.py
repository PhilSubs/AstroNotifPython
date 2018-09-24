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
sParameter1 = sys.argv[2]

# Read the parameters files
theParameters = ANLib.Parameters() # read parameters file parameters_run.json

# Actions
if sAction == "resetTrace":
    # Reset the logfile
    ANLib.Tools.resetTrace(theParameters.Runtime().getGlobal("PathToLogFileName"))
elif sAction == "logToTrace":
    ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), sParameter1)
elif sAction == "getTrace":
    if sParameter1 == "HTML":
        print ANLib.Tools.getTrace(theParameters.Runtime().getGlobal("PathToLogFileName")).replace("\n","<BR>\n")
    else:
        print ANLib.Tools.getTrace(theParameters.Runtime().getGlobal("PathToLogFileName"))
elif sAction = "generateHTMLPageForTrace":
    sPageContent = "<HTML>"
    sPageContent += "	<HEAD>"
    sPageContent += '      <TITLE>AstroNotifLog</TITLE>'
    sPageContent += '      <LINK rel="icon" href="http://' + theParameters.Runtime().getNightlyBatch('Domain') + '/favicon.png">      <base href="">'
    sPageContent += '      <LINK rel="stylesheet" href="http://' + theParameters.Runtime().getNightlyBatch('Domain') + '/AstroNotif.css">'
    sPageContent += '      <META charset="UTF-8">'
    sPageContent += "	</HEAD>"
    sPageContent += "  <BODY>"

    sPageContent += ANLib.Tools.getTrace(theParameters.Runtime().getGlobal("PathToLogFileName")).replace("\n","<BR>\n")

    sPageContent += "  </BODY>"    
    sPageContent += "</HTML>"
    
    ANLib.Tools.saveAsFileEncoded(theParameters.Runtime().getGlobal('PathToWWWFolder') + ANLib.Tools.get_path_separator() + "nightlybatchlog.html", sPageContent)

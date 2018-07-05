#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

# Import modules for CGI handling
import cgi, cgitb

# Import libs for ephemerides
from datetime import datetime, timedelta
import ANLib

# Enable user-firendly debug
#cgitb.enable()

# Init default values
sHTMLFileName = '../default.html'

# CGI output 
print "Content-Type: text/html"
print "<HTML>\n"
print "<BODY>\n"

# get URL arguments
theParameters = ANLib.Parameters()
sParamDate = (datetime.now() + timedelta(hours=theParameters.getNightlyBatchTimeDeltaInHours())).strftime("%Y%m%d")  # start date from current date at 00:00 + delta hours
sParamLongitude = ""
sParamLatitude = ""
sParamPlace = ""
arguments = cgi.FieldStorage()
for i in arguments.keys():
    print arguments[i].value
    if i == 'date' :
        sParamDate = arguments[i].value
        print "   Date........  "  + sParamDate + " <BR>\n"
    if i == 'place' :
        sParamPlace = arguments[i].value
        print "   Place.......  "  + sParamPlace + " <BR>\n"
    if i == "longitude":
        sParamLongitude = arguments[i].value
        print "   Longitude...  "  + sParamLongitude + " <BR>\n"
    if i == "latitude":
        sParamLatitude = arguments[i].value
        print "   Latitude....  "  + sParamLatitude + " <BR>\n"

# Prepare objects for computing ephemeris
print "Prepare parameters...<BR>\n"
theCalendar = ANLib.Calendar(sParamDate,"000000")  # start from current date at 00:00
if sParamPlace != "":
    theParameters.getPlace().setName(sParamPlace)
if sParamLongitude != "":
    theParameters.getPlace().setLongitude(float(sParamLongitude))
if sParamLatitude != "":
    theParameters.getPlace().setLatitude(float(sParamLatitude))
theEphemeridesData = ANLib.EphemeridesData()

# Check last generated files
theEphemeridesData.computeEphemeridesForPeriod(theParameters, theCalendar)
print "Check if last version generated has the same parameters than this run...<BR>\n"
if 'Render' == 'HTML':
    theRendererHTML = ANLib.RendererHTML('../bm/', "http://astronot.heliohost.org/bm/", True)
    bNoNeedToCompute = (ANLib.Tools.getCurrentFilesHTMLHeaderComment(sHTMLFileName) == theRendererHTML.getHTMLHeaderComment(theCalendar, theParameters))
else:
    theRendererBitmap = ANLib.RendererBitmap('../bm/', "http://astronot.heliohost.org/bm/", True)
    bNoNeedToCompute = (ANLib.Tools.getCurrentFilesHTMLHeaderComment(sHTMLFileName) == theRendererBitmap.getHTMLHeaderComment(theCalendar, theParameters))
bNoNeedToCompute = False

# Get HTML content
if bNoNeedToCompute:
    print "No need to render new HTML...<BR>\n"
else:
    print "Render HTML and bitmaps...<BR>\n"
    if 'Render' == 'HTML':
        sHTMLContent = theRendererHTML.getHTML(theCalendar, theParameters, theEphemeridesData)
    else:
        sHTMLContent, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable = theRendererBitmap.getHTML(theCalendar, theParameters, theEphemeridesData)
        sSubject = "Ephemerides du " + theCalendar.getFormattedDateForSlot(0, 0)
        if (iNbPlanetsObservable + iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0:
            sSubject = sSubject + "   ("
            if iNbPlanetsObservable > 0: 
                sSubject = sSubject + str(iNbPlanetsObservable) +  " planet"
                if iNbPlanetsObservable> 1: sSubject = sSubject + "s"
                if (iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0: sSubject = sSubject + ", "
            if iNbLunarFeaturesobservable > 0: 
                sSubject = sSubject + str(iNbLunarFeaturesobservable) +  " moon feat."
                if (iNbDeepSkyobjectsObservable) > 0: sSubject = sSubject + ", "
            if iNbDeepSkyobjectsObservable > 0: 
                sSubject = sSubject + str(iNbDeepSkyobjectsObservable) +  " deep sky object"
                if iNbDeepSkyobjectsObservable> 1: sSubject = sSubject + "s"
            sSubject = sSubject + ")"

        print sSubject

    # Save as default html file
    print "Save as default.html...<BR>\n"
    ANLib.Tools.saveAsFile(sHTMLFileName, sHTMLContent)


print "Completed\n"
print "</BODY>\n"
print "</HTML>\n"

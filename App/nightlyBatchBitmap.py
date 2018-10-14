#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

# Import libs for ephemerides
from datetime import datetime, timedelta
import ANLib
from PIL import Image

# Init default values
iNbPlanetsObservable = 0
iNbLunarFeaturesobservable = 0
iNbDeepSkyobjectsObservable = 0

# Read the parameters files
theParameters = ANLib.Parameters() # read parameters file parameters_run.json
ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), "Parameters read from json files...")

# Prepare objects for computing ephemeris
sParamDate = (datetime.now() + timedelta(hours=theParameters.Runtime().get('NightlyBatch.TimeDeltaInHours'))).strftime("%Y%m%d")  # start date from current date at 00:00 + delta hours
theCalendar = ANLib.Calendar(sParamDate,"000000", theParameters.Runtime().get("Place").get("CurrentLocalTimeDifferenceWithGMT"))
theEphemeridesData = ANLib.EphemeridesData()

# Compute ephemeris and produce new HTML
ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), "Compute ephemeris...")
theEphemeridesData.computeEphemeridesForPeriod(theParameters, theCalendar)
ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), "Generate HTML page and bitmap...")
theRendererBitmap = ANLib.RendererBitmap( theParameters, theParameters.Runtime().get('Global.PathToWWWFolder') + '/', "http://" + theParameters.Runtime().get('NightlyBatch.Domain') + "/", True)
sHTMLContent, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilenameAndPath, sBitmapFilename, bNotificationToBeSent = theRendererBitmap.getHTML(theCalendar, theEphemeridesData)

# Save as default html file
ANLib.Tools.saveAsFileEncoded(theParameters.Runtime().get('Global.PathToWWWFolder') + ANLib.Tools.get_path_separator() + theParameters.Runtime().get('NightlyBatch.HTMLFilname'), sHTMLContent)
ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), "HTML page and bitmap are generated in " + theParameters.Runtime().get('Global.PathToWWWFolder') + ANLib.Tools.get_path_separator())

# Prepare email for daily notification
if len(theParameters.Runtime().get('NightlyBatch.EmailAddress')) > 0:
    ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), "Preparing email to be sent")
    sTo = theParameters.Runtime().get('NightlyBatch.EmailAddress')
    sSubject = theParameters.Localization().getWithDefault("EphemerisFor") + " " + theCalendar.getFormattedLocalDateForSlot(0, 0) + " (" + theParameters.Runtime().get("Place").get("Name")  + ")"
    if bNotificationToBeSent: #(iNbPlanetsObservable + iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0:
        sSubject = sSubject + ": "
        if iNbPlanetsObservable > 0: 
            sSubject = sSubject + theParameters.Localization().getWithDefault("ThePlanets") + " [" + str(iNbPlanetsObservable) + "]"
            if (iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0: sSubject = sSubject + ",  "
        if iNbLunarFeaturesobservable > 0: 
            sSubject = sSubject + theParameters.Localization().getWithDefault("LunarFeatures") + " [" + str(iNbLunarFeaturesobservable) + "]"
            if (iNbDeepSkyobjectsObservable) > 0: sSubject = sSubject + ",  "
        if iNbDeepSkyobjectsObservable > 0: 
            sSubject = sSubject + theParameters.Localization().getWithDefault("TheDeepSkyObjects") + " [" + str(iNbDeepSkyobjectsObservable) + "]"

    # Send email
    sHTMLContent = '<HTML><BODY><A href="http://' + theParameters.Runtime().get('NightlyBatch.Domain') + '/">Lieu: ' + theParameters.Runtime().get("Place").get("Name")  + '</A></BODY></HTML>'
    sLogEmailSending = ANLib.Tools.sendEmailHTML(theParameters.Runtime().get('NightlyBatch.EmailFromAddress'), sTo, sSubject, sHTMLContent, sBitmapFilenameAndPath, sBitmapFilename, theParameters.Runtime().get('NightlyBatch.EmailSMTPServer'), theParameters.Runtime().get('NightlyBatch.EmailSMTPUser'), theParameters.Runtime().get('NightlyBatch.EmailSMTPPassword') )
    ANLib.Tools.logToTrace(theParameters.Runtime().get("Global.PathToLogFileName"), sLogEmailSending)

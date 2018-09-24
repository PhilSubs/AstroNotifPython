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
ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), "Parametres initialises")

# Prepare objects for computing ephemeris
sParamDate = (datetime.now() + timedelta(hours=theParameters.Runtime().getNightlyBatch('TimeDeltaInHours'))).strftime("%Y%m%d")  # start date from current date at 00:00 + delta hours
theCalendar = ANLib.Calendar(sParamDate,"000000", theParameters.Runtime().getPlace().getCurrentLocalTimeDifferenceWithGMT())
theEphemeridesData = ANLib.EphemeridesData()

# Compute ephemeris and produce new HTML
ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), "Calcul des ephemerides")
theEphemeridesData.computeEphemeridesForPeriod(theParameters, theCalendar)
ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), "Generation de la page HTML et du bitmap")
theRendererBitmap = ANLib.RendererBitmap( theParameters, theParameters.Runtime().getGlobal('PathToWWWFolder') + '/', "http://" + theParameters.Runtime().getNightlyBatch('Domain') + "/", True)
sHTMLContent, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilename, bNotificationToBeSent = theRendererBitmap.getHTML(theCalendar, theEphemeridesData)

# Save as default html file
ANLib.Tools.saveAsFileEncoded(theParameters.Runtime().getGlobal('PathToWWWFolder') + ANLib.Tools.get_path_separator() + theParameters.Runtime().getNightlyBatch('HTMLFilname'), sHTMLContent)
ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), "La page HTML et le bitmap sont generes dans " + theParameters.Runtime().getGlobal('PathToWWWFolder') + ANLib.Tools.get_path_separator())

# Prepare email for daily notification
if len(theParameters.Runtime().getNightlyBatch('EmailAddress')) > 0:
    ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), "Preparation a l'envoi du mail")
    sTo = theParameters.Runtime().getNightlyBatch('EmailAddress')
    sSubject = theParameters.Localization().getLabel("EphemerisFor") + " " + theCalendar.getFormattedLocalDateForSlot(0, 0) + " (" + theParameters.Runtime().getPlace().getName()  + ")"
    if bNotificationToBeSent: #(iNbPlanetsObservable + iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0:
        sSubject = sSubject + ": "
        if iNbPlanetsObservable > 0: 
            sSubject = sSubject + theParameters.Localization().getLabel("ThePlanets") + " [" + str(iNbPlanetsObservable) + "]"
            if (iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0: sSubject = sSubject + ",  "
        if iNbLunarFeaturesobservable > 0: 
            sSubject = sSubject + theParameters.Localization().getLabel("LunarFeatures") + " [" + str(iNbLunarFeaturesobservable) + "]"
            if (iNbDeepSkyobjectsObservable) > 0: sSubject = sSubject + ",  "
        if iNbDeepSkyobjectsObservable > 0: 
            sSubject = sSubject + theParameters.Localization().getLabel("TheDeepSkyObjects") + " [" + str(iNbDeepSkyobjectsObservable) + "]"

    # Send email
    ANLib.Tools.logToTrace(theParameters.Runtime().getGlobal("PathToLogFileName"), "Envoi du mail")
    sHTMLContent = '<HTML><BODY><A href="http://' + theParameters.Runtime().getNightlyBatch('Domain') + '/">Lieu: ' + theParameters.Runtime().getPlace().getName()  + '</A></BODY></HTML>'
    ANLib.Tools.sendEmailHTML(theParameters.Runtime().getNightlyBatch('EmailFromAddress'), sTo, sSubject, sHTMLContent, sBitmapFilename, theParameters.Runtime().getNightlyBatch('EmailSMTPServer'), theParameters.Runtime().getNightlyBatch('EmailSMTPUser'), theParameters.Runtime().getNightlyBatch('EmailSMTPPassword') )

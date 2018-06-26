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

# Prepare objects for computing ephemeris
theParameters = ANLib.Parameters() # read parameters file parameters_run.json
sParamDate = (datetime.now() + timedelta(hours=theParameters.getNightlyBatchTimeDeltaInHours())).strftime("%Y%m%d")  # start date from current date at 00:00 + delta hours
theCalendar = ANLib.Calendar(sParamDate,"000000")
theEphemeridesData = ANLib.EphemeridesData()

# Compute ephemeris and produce new HTML
theEphemeridesData.computeEphemeridesForPeriod(theParameters, theCalendar)
if 'Render' == 'HTML':
    theRendererHTML = ANLib.RendererHTML('../bm/', "http://" + theParameters.getNightlyBatchDomain() + "/bm/", True)
    sHTMLContent = theRendererHTML.getHTML(theCalendar, theParameters, theEphemeridesData)
else:
    theRendererBitmap = ANLib.RendererBitmap('../bm/', "http://" + theParameters.getNightlyBatchDomain() + "/bm/", True)
    sHTMLContent, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable = theRendererBitmap.getHTML(theCalendar, theParameters, theEphemeridesData)

# Save as default html file
ANLib.Tools.saveAsFile(theParameters.getNightlyBatchHTMLFilname(), sHTMLContent)

# Prepare email for daily notification
if len(theParameters.getNightlyBatchEmailAddress()) > 0:
    sTo = theParameters.getNightlyBatchEmailAddress()
    sSubject = "Ephemerides " + theCalendar.getFormattedDateForSlot(0, 0)
    if (iNbPlanetsObservable + iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0:
        sSubject = sSubject + ": "
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

    # Send email
    ANLib.Tools.sendEmailHTML(theParameters.getNightlyBatchEmailFromAdress(), sTo, sSubject, sHTMLContent, theParameters.getNightlyBatchEmailSMTPServer() )

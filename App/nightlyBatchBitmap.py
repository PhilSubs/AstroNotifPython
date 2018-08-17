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
print "Lecture des parametres du fichier parameters_run.json<br>"
theParameters = ANLib.Parameters() # read parameters file parameters_run.json
sParamDate = (datetime.now() + timedelta(hours=theParameters.Runtime().getNightlyBatchTimeDeltaInHours())).strftime("%Y%m%d")  # start date from current date at 00:00 + delta hours
theCalendar = ANLib.Calendar(sParamDate,"000000")
theEphemeridesData = ANLib.EphemeridesData()

# Compute ephemeris and produce new HTML
print "Calcul des ephemerides<br>"
theEphemeridesData.computeEphemeridesForPeriod(theParameters, theCalendar)
print "Generation de la page HTML et du bitmap<br>"
theRendererBitmap = ANLib.RendererBitmap( theParameters, theParameters.Runtime().getGlobalPathToWWWFolder() + '/', "http://" + theParameters.Runtime().getNightlyBatchDomain() + "/", True)
sHTMLContent, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilename = theRendererBitmap.getHTML(theCalendar, theEphemeridesData)

# Save as default html file
ANLib.Tools.saveAsFileEncoded(theParameters.Runtime().getGlobalPathToWWWFolder() + ANLib.Tools.get_path_separator() + theParameters.Runtime().getNightlyBatchHTMLFilname(), sHTMLContent)
print "La page HTML et le bitmap sont generes dans " + theParameters.Runtime().getGlobalPathToWWWFolder() + ANLib.Tools.get_path_separator() + '<br>'

# Prepare email for daily notification
if len(theParameters.Runtime().getNightlyBatchEmailAddress()) > 0:
    print "Preparation a l'envoi du mail<br>"
    sTo = theParameters.Runtime().getNightlyBatchEmailAddress()
    sSubject = theParameters.Localization().getLabel("EphemerisFor") + " " + theCalendar.getFormattedDateForSlot(0, 0) + " (" + theParameters.Runtime().getPlace().getName()  + ")"
    if (iNbPlanetsObservable + iNbLunarFeaturesobservable + iNbDeepSkyobjectsObservable) > 0:
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
    print "Envoi du mail<br>"
    sHTMLContent = '<HTML><BODY><A href="http://' + theParameters.Runtime().getNightlyBatchDomain() + '/">Lieu: ' + theParameters.Runtime().getPlace().getName()  + '</A></BODY></HTML>'
    ANLib.Tools.sendEmailHTML(theParameters.Runtime().getNightlyBatchEmailFromAddress(), sTo, sSubject, sHTMLContent, sBitmapFilename, theParameters.Runtime().getNightlyBatchEmailSMTPServer(), theParameters.Runtime().getNightlyBatchEmailSMTPUser(), theParameters.Runtime().getNightlyBatchEmailSMTPPassword() )

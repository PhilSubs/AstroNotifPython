#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class EphemeridesData
# 
from toolObjectSerializable import toolObjectSerializable
from EphemeridesDataObject import EphemeridesDataObject
from EphemeridesMoon import EphemeridesMoon
from EphemeridesMoonMeeus import EphemeridesMoonMeeus
from EphemeridesSun import EphemeridesSun
from EphemeridesPlanet import EphemeridesPlanet
from Calendar import Calendar
from Parameters import Parameters
from CommonAstroFormulaes import CommonAstroFormulaes

#from toolTrace import toolTrace


class EphemeridesData(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._sStartDate = ""         # YYYYMMDD
        self._sStartTime = ""         # HHMMSS
        self._iNbSlots = 0            # 
        self._observerLongitude = 0.0 #
        self._observerLatitude = 0.0  #
        self._date = {}               # date for each slot (YYYYMMDD)   (key=slotID)
        self._time = {}               # time for the beginning of the slot (HHMMSS)   (key=slotID)
        self._sunAltitude = {}        # sun's altitude for each slot   (key=slotID)
        self._sunMeanLongInDeg = {}   # sun's mean longitude for each slot   (key=slotID)
        self._objects = {}            # ephemerides for each objects (dictionary of EphemeridesDataObject, with key = ObjectID)
    
    def getObjectVisibilityStatusForSlot(self, sObjectID, iSlot, oParameters):
        # Return object visibility status depending on object altitude and Azimut, Place, and Sun Altitude
        #     - Below : object is below horizon
        #     - VeryLow: object is visible but very low   (<15)
        #     - Low: object is visible but low  (<35)
        #     - Difficult: object is visible but sun makes it difficult to see
        #     - Impossible:  object is visible but sun makes it impossible to see
        #     - Hidden: object is visible but hidden by something
        #     - Good: object is visible in good conditions
        fDisplayMaxAltitudeForObjectVeryLow = oParameters.Rendering().getDisplay('MaxAltitudeForObjectVeryLow')
        fDisplayMaxAltitudeForObjectLow = oParameters.Rendering().getDisplay('MaxAltitudeForObjectLow')
        fDisplayMaxSunAltitudeForObservableDeepSky = oParameters.Rendering().getDisplay('MaxSunAltitudeForObservableDeepSky')
        fDisplayMaxSunAltitudeForObservableBrightObjects = oParameters.Rendering().getDisplay('MaxSunAltitudeForObservableBrightObjects')
        fDisplayMaxSunAltitudeForDifficultBrightObjects = oParameters.Rendering().getDisplay('MaxSunAltitudeForDifficultBrightObjects')
        fDisplayMaxSunAltitudeFoImpossibleBrightObjects = oParameters.Rendering().getDisplay('MaxSunAltitudeFoImpossibleBrightObjects')
        fDisplayMaxSunAltitudeForObservableMediumObjects = oParameters.Rendering().getDisplay('MaxSunAltitudeForObservableMediumObjects')
        fDisplayMaxSunAltitudeForDifficultMediumObjects = oParameters.Rendering().getDisplay('MaxSunAltitudeForDifficultMediumObjects')

        fObjectAltitude = self._objects[sObjectID].getAltitudeForSlot(iSlot)
        fObjectAZimut = self._objects[sObjectID].getAzimutForSlot(iSlot)
        fSunAltitude = self._sunAltitude[str(iSlot)]
        sObjectCategory = oParameters.SkyObjects().getSkyObjectByID(sObjectID).getCategory()
        
        sStatus = "Unknown"
        
        # Below horizon and hidden
        if fObjectAltitude < 0.0:
            sStatus = "Below"
        elif oParameters.Runtime().getPlace().getObstructedSkyAreas().getVisibilityStatus(fObjectAZimut, fObjectAltitude) == "0":
            sStatus = "Hidden"
        # Deepsky
        elif sObjectCategory == "DeepSky":
            if fSunAltitude <= fDisplayMaxSunAltitudeForObservableDeepSky:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                   sStatus = "VeryLow"
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    sStatus = "Low"
                else:
                    sStatus = "Good"
            else:
                sStatus = "Impossible"           
        # Bright Planet and Moon
        elif sObjectID == "Moon" or sObjectID == "Venus" or sObjectID == "Jupiter":
            if fSunAltitude < fDisplayMaxSunAltitudeForObservableBrightObjects:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    sStatus = "VeryLow"
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    sStatus = "Low"
                else:
                    sStatus = "Good"
            elif fSunAltitude < fDisplayMaxSunAltitudeForDifficultBrightObjects:
                sStatus = "Difficult" 
            elif fSunAltitude < fDisplayMaxSunAltitudeFoImpossibleBrightObjects:
                if sObjectID == "Moon":
                    sStatus = "Difficult" 
                else:
                    sStatus = "Impossible" 
            else:
                sStatus = "Impossible"
        # Medium objects
        else:
            if fSunAltitude < fDisplayMaxSunAltitudeForObservableMediumObjects:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    sStatus = "VeryLow"
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    sStatus = "Low"
                else:
                    sStatus = "Good"
            elif fSunAltitude < fDisplayMaxSunAltitudeForDifficultMediumObjects:
                sStatus = "Difficult" 
            else:
                sStatus = "Impossible"
            
        return sStatus
    
    
    def getSunAltitudeForSlot(self, iSlot): return self._sunAltitude[str(iSlot)]
    def getSunMeanLongInDegForSlot(self, iSlot): return self._sunMeanLongInDeg[str(iSlot)] % 360.0
    def getEphemerideDataObject(self, sObjectID): return self._objects[sObjectID]
    
    def computeEphemeridesForPeriod(self, oParameters, oCalendar):
        # init display parameters
        self._sStartDate = oCalendar.getLocalStartDate()
        self._sStartTime = oCalendar.getLocalStartTime()
        self._iNbSlotsMoon = oParameters.Rendering().getDisplay('NumberOfSlotsForMoon')
        self._iNbSlots = self._iNbSlotsMoon
        self._iNbSlotsPlanets = oParameters.Rendering().getDisplay('NumberOfSlotsForPlanets')
        if self._iNbSlotsPlanets> self._iNbSlots: self._iNbSlots = self._iNbSlotsPlanets
        self._iNbSlotsDeepSky = oParameters.Rendering().getDisplay('NumberOfSlotsForDeepSky')
        if self._iNbSlotsDeepSky> self._iNbSlots: self._iNbSlots = self._iNbSlotsDeepSky
        self._observerLongitude = oParameters.Runtime().getPlace().getLongitude()
        self._observerLatitude = oParameters.Runtime().getPlace().getLatitude()
        # init objects list
        self._objects['Moon'] = EphemeridesDataObject("Moon", "Moon", "Moon", "Moon", "")
        self._objects['Mercury'] = EphemeridesDataObject("Mercury", "Planet", "Planetary", "Mercury", "")
        self._objects['Venus'] = EphemeridesDataObject("Venus", "Planet", "Planetary", "Venus", "")
        self._objects['Mars'] = EphemeridesDataObject("Mars", "Planet", "Planetary", "Mars", "")
        self._objects['Jupiter'] = EphemeridesDataObject("Jupiter", "Planet", "Planetary", "Jupiter", "")
        self._objects['Saturn'] = EphemeridesDataObject("Saturn", "Planet", "Planetary", "Saturn", "")
        self._objects['Uranus'] = EphemeridesDataObject("Uranus", "Planet", "Planetary", "Uranus", "")
        self._objects['Neptune'] = EphemeridesDataObject("Neptune", "Planet", "Planetary", "Neptune", "")
        for iIndex in range(0, oParameters.SkyObjects().getCount()):
            if oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getCategory() != "Planetary" and oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getCategory() != "Moon":
                self._objects[oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getID()] = EphemeridesDataObject(oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getID(), oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getType(), oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getCategory(), oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getName(), oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getPictureName())
        # Compute data for each slots
        theSun = EphemeridesSun()
        theMoon = EphemeridesMoonMeeus() #EphemeridesMoon()
        thePlanetMercury = EphemeridesPlanet("Mercury")
        thePlanetVenus = EphemeridesPlanet("Venus")
        thePlanetMars = EphemeridesPlanet("Mars")
        thePlanetJupiter = EphemeridesPlanet("Jupiter")
        thePlanetSaturn = EphemeridesPlanet("Saturn")
        thePlanetUranus = EphemeridesPlanet("Uranus")
        thePlanetNeptune = EphemeridesPlanet("Neptune")
        for iSlot in range (0, self._iNbSlots):
            fDateValue = oCalendar.getGMTDateValueForTimeSlot(iSlot, oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
            #
            theSun.computeEphemerides(fDateValue)
            fLocalSideralTime = CommonAstroFormulaes.getSideralTimeForTime(oCalendar.getGMTTimeForSlot(iSlot,oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')), theSun.getTrueAnoInDeg(), theSun.getArgPerihelInDeg(), oParameters.Runtime().getPlace().getLongitude())
            self._sunAltitude[str(iSlot)] = CommonAstroFormulaes.getAltitudeFromEquatCoord(theSun.getRAInDeg(), theSun.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
            self._sunMeanLongInDeg[str(iSlot)] = theSun.getMeanLongInDeg()
            #
            if iSlot <= self._iNbSlotsMoon:
                theMoon.computeEphemerides(oCalendar.getGMTDateForSlot(iSlot,oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')), oCalendar.getGMTTimeForSlot(iSlot,oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')), theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg())
                #fMoonAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(theMoon.getRightAscension(), theMoon.getDeclination(), self._observerLatitude, fLocalSideralTime)
                #fMoonAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(theMoon.getRightAscension(), theMoon.getDeclination(), self._observerLatitude, fLocalSideralTime)
                fMoonAltitude = theMoon.getElevation(self._observerLongitude, self._observerLatitude)
                fMoonAzimut = theMoon.getAzimut(self._observerLongitude, self._observerLatitude)
                self._objects['Moon'].setDataForSlot(iSlot, fMoonAzimut, fMoonAltitude, theMoon.getRightAscension(), theMoon.getDeclination(), theMoon.getDistInKM(), 0.0, theMoon.getMoonSelenographicColongitude(), theMoon.getMoonSelenographicLongitude(), theMoon.getMoonSelenographicLatitude(), theMoon.getPhase(), theMoon.getIllumination())
            #
            if iSlot <= self._iNbSlotsPlanets:
                thePlanetMercury.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), 0.0, 0.0)
                fMercuryAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetMercury.getRAInDeg(), thePlanetMercury.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fMercuryAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetMercury.getRAInDeg(), thePlanetMercury.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Mercury'].setDataForSlot(iSlot, fMercuryAzimut, fMercuryAltitude, thePlanetMercury.getRAInDeg(), thePlanetMercury.getDecInDeg(), thePlanetMercury.getSunDistInUA(), thePlanetMercury.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
                #
                thePlanetVenus.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), 0.0, 0.0)
                fVenusAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetVenus.getRAInDeg(), thePlanetVenus.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fVenusAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetVenus.getRAInDeg(), thePlanetVenus.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Venus'].setDataForSlot(iSlot, fVenusAzimut, fVenusAltitude,thePlanetVenus.getRAInDeg(), thePlanetVenus.getDecInDeg(),  thePlanetVenus.getSunDistInUA(), thePlanetVenus.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
                #
                thePlanetMars.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), 0.0, 0.0)
                fMarsAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetMars.getRAInDeg(), thePlanetMars.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fMarsAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetMars.getRAInDeg(), thePlanetMars.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Mars'].setDataForSlot(iSlot, fMarsAzimut, fMarsAltitude, thePlanetMars.getRAInDeg(), thePlanetMars.getDecInDeg(), thePlanetMars.getSunDistInUA(), thePlanetMars.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
                #
                thePlanetJupiter.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), 0.0, thePlanetSaturn.getMeanAnoInDeg(fDateValue))
                fJupiterAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetJupiter.getRAInDeg(), thePlanetJupiter.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fJupiterAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetJupiter.getRAInDeg(), thePlanetJupiter.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Jupiter'].setDataForSlot(iSlot, fJupiterAzimut, fJupiterAltitude, thePlanetJupiter.getRAInDeg(), thePlanetJupiter.getDecInDeg(), thePlanetJupiter.getSunDistInUA(), thePlanetJupiter.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
                #
                thePlanetSaturn.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), thePlanetJupiter.getMeanAnoInDeg(fDateValue), 0.0)
                fSaturnAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetSaturn.getRAInDeg(), thePlanetSaturn.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fSaturnAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetSaturn.getRAInDeg(), thePlanetSaturn.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Saturn'].setDataForSlot(iSlot, fSaturnAzimut, fSaturnAltitude, thePlanetSaturn.getRAInDeg(), thePlanetSaturn.getDecInDeg(), thePlanetSaturn.getSunDistInUA(), thePlanetSaturn.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
                #
                thePlanetUranus.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), thePlanetJupiter.getMeanAnoInDeg(fDateValue), thePlanetSaturn.getMeanAnoInDeg(fDateValue))
                fUranusAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetUranus.getRAInDeg(), thePlanetUranus.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fUranusAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetUranus.getRAInDeg(), thePlanetUranus.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Uranus'].setDataForSlot(iSlot, fUranusAzimut, fUranusAltitude, thePlanetUranus.getRAInDeg(), thePlanetUranus.getDecInDeg(), thePlanetUranus.getSunDistInUA(), thePlanetUranus.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
                #
                thePlanetNeptune.computeEphemerides(fDateValue, theSun.getMeanAnoInDeg(), theSun.getArgPerihelInDeg(), theSun.getSunDistInUA(), 0.0, 0.0)
                fNeptuneAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(thePlanetNeptune.getRAInDeg(), thePlanetNeptune.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                fNeptuneAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(thePlanetNeptune.getRAInDeg(), thePlanetNeptune.getDecInDeg(), self._observerLatitude, fLocalSideralTime)
                self._objects['Neptune'].setDataForSlot(iSlot, fNeptuneAzimut, fNeptuneAltitude, thePlanetNeptune.getRAInDeg(), thePlanetNeptune.getDecInDeg(), thePlanetNeptune.getSunDistInUA(), thePlanetNeptune.getMeanLongInDeg(), 0.0, 0.0, 0.0, 0.0, 0.0)
            #
            if iSlot <= self._iNbSlotsDeepSky:
                for iIndex in range(0, oParameters.SkyObjects().getCount()):
                    if not(oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getCategory() == "Planetary") and not(oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getCategory() == "Moon"):
                        fAzimut = CommonAstroFormulaes.getAzimutFromEquatCoord(oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getRA(), oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getDec(), self._observerLatitude, fLocalSideralTime)
                        fAltitude = CommonAstroFormulaes.getAltitudeFromEquatCoord(oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getRA(), oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getDec(), self._observerLatitude, fLocalSideralTime)
                        self._objects[oParameters.SkyObjects().getSkyObjectByIndex(iIndex).getID()].setDataForSlot(iSlot, fAzimut, fAltitude, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                    
        
    
        
        

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Parameters
# 
import json
from toolObjectSerializable import toolObjectSerializable
from Places import Places
from SkyObjects import SkyObjects
from LunarFeatures import LunarFeatures

#from toolTrace import toolTrace


class Parameters(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._sGlobalCurrentVersion = ""
        self._sNightlyBatchDomain = ""
        self._sNightlyBatchEmailAddress = ""
        self._sNightlyEmailSMTPServer = ""
        self._sNightlyEmailFromAdress = ""
        self._sNightlyBatchHTMLFilname = ""
        self._fObservationMinAltitudeInDeg = 0.0
        self._sObservationStartTimeAsHHMM = ""
        self._iObservationMaxDurationInHours = 0
        self._bObservationAlways = True
        self._bObservationForceDisplayPlanetMoon = False
        self._fObservationMaximumLunarFeatureSunAltitude = 90.0
        self._bObservationShowWhenTerminatorIsOnLunarFeature = False
        self._fObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg = 0.0
        self._sObservationPlaceName = ""
        self._bDisplayVisibilityTableAsBitmap = True
        self._iDisplayNumberOfSlotsForMoon = 0
        self._iDisplayNumberOfSlotsForMoonFeatures = 0
        self._iDisplayNumberOfSlotsForPlanets = 0
        self._iDisplayNumberOfSlotsForDeepSky = 0
        self._iDisplayNumberOfMinutesPerSlot = 0
        self._iDisplayDaySlotForDataInfo = 0
        self._fDisplayMaxObjectAltitudeForLow = 0.0
        self._fDisplayMaxObjectAltitudeForVeryLow = 0.0
        self._fDisplayMaxSunAltitudeForObservableDeepSky = 0.0
        self._fDisplayMaxSunAltitudeForObservableBrightObjects = 0.0
        self._fDisplayMaxSunAltitudeForDifficultBrightObjects = 0.0
        self._fDisplayMaxSunAltitudeFoImpossibleBrightObjects = 0.0
        self._fDisplayMaxSunAltitudeForObservableMediumObjects = 0.0
        self._fDisplayMaxSunAltitudeForDifficultMediumObjects = 0.0
        self._Place = None
        self._SkyObjects = {}
        self._LunarFeatures = {}
        self.__loadFromFile()
    def getGlobalCurrentVersion(self): return self._sGlobalCurrentVersion
    def getNightlyBatchTimeDeltaInHours(self): return self._iNightlyBatchTimeDeltaInHours
    def getNightlyBatchEmailAddress(self): return self._sNightlyBatchEmailAddress
    def getNightlyBatchEmailSMTPServer(self): return self._sNightlyBatchEmailSMTPServer
    def getNightlyBatchEmailFromAdress(self): return self._sNightlyBatchEmailFromAdress
    def getNightlyBatchDomain(self): return self._sNightlyBatchDomain
    def getNightlyBatchHTMLFilname(self): return self._sNightlyBatchHTMLFilname
    def getObservationStartTimeAsHHMM(self): return self._sObservationStartTimeAsHHMM
    def getObservationMaxDurationInHours(self): return self._iObservationMaxDurationInHours
    def getObservationMinAltitudeInDeg(self): return self._fObservationMinAltitudeInDeg
    def getObservationAlways(self): return self._bObservationAlways
    def getObservationForceDisplayPlanetMoon(self): return self._bObservationForceDisplayPlanetMoon
    def getObservationMaximumLunarFeatureSunAltitude(self): return self._fObservationMaximumLunarFeatureSunAltitude
    def getObservationShowWhenTerminatorIsOnLunarFeature(self): return self._bObservationShowWhenTerminatorIsOnLunarFeature
    def getObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg(self): return self._fObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg
    def getObservationPlaceName(self): return self._sObservationPlaceName
    def getDisplayVisibilityTableAsBitmap(self): return self._bDisplayVisibilityTableAsBitmap
    def getDisplayNumberOfSlotsForMoon(self): return self._iDisplayNumberOfSlotsForMoon
    def getDisplayNumberOfSlotsForMoonFeatures(self): return self._iDisplayNumberOfSlotsForMoonFeatures
    def getDisplayNumberOfSlotsForPlanets(self): return self._iDisplayNumberOfSlotsForPlanets
    def getDisplayNumberOfSlotsForDeepSky(self): return self._iDisplayNumberOfSlotsForDeepSky
    def getDisplayNumberOfMinutesPerSlot(self): return self._iDisplayNumberOfMinutesPerSlot
    def getDisplayDaySlotForDataInfo(self): return self._iDisplayDaySlotForDataInfo
    def getDisplayMaxAltitudeForObjectLow(self): return self._fDisplayMaxAltitudeForObjectLow
    def getDisplayMaxAltitudeForObjectVeryLow(self): return self._fDisplayMaxAltitudeForObjectVeryLow
    def getDisplayMaxSunAltitudeForObservableDeepSky(self): return self._fDisplayMaxSunAltitudeForObservableDeepSky
    def getDisplayMaxSunAltitudeForObservableBrightObjects(self): return self._fDisplayMaxSunAltitudeForObservableBrightObjects
    def getDisplayMaxSunAltitudeForDifficultBrightObjects(self): return self._fDisplayMaxSunAltitudeForDifficultBrightObjects
    def getDisplayMaxSunAltitudeFoImpossibleBrightObjects(self): return self._fDisplayMaxSunAltitudeFoImpossibleBrightObjects
    def getDisplayMaxSunAltitudeForObservableMediumObjects(self): return self._fDisplayMaxSunAltitudeForObservableMediumObjects
    def getDisplayMaxSunAltitudeForDifficultMediumObjects(self): return self._fDisplayMaxSunAltitudeForDifficultMediumObjects
    def getPlace(self): return self._Place
    def getSkyObjects(self): return self._SkyObjects
    def getLunarFeatures(self): return self._LunarFeatures
    def __loadFromFile(self):
        # load parameters file
        with open('parameters_Runtime.json', 'r') as f:
             data = json.load(f)
        # init properties
        self._sGlobalCurrentVersion = data["currentVersion"]
        self._iNightlyBatchTimeDeltaInHours = data["NightlyBatchTimeDeltaInHours"]
        self._sNightlyBatchEmailAddress = data["NightlyBatchEmailAddress"]
        self._sNightlyBatchEmailSMTPServer = data["NightlyBatchEmailSMTPServer"]
        self._sNightlyBatchEmailFromAdress = data["NightlyBatchEmailFromAdress"]
        self._sNightlyBatchDomain = data["NightlyBatchDomain"]
        self._sNightlyBatchHTMLFilname = data["NightlyBatchHTMLFilname"]
        self._sObservationStartTimeAsHHMM = data["ObservationStartTimeAsHHMM"]
        self._iObservationMaxDurationInHours = data["ObservationMaxDurationInHours"]
        self._fObservationMinAltitudeInDeg = data["ObservationMinAltitudeInDeg"]
        self._bObservationAlways = ( data["ObservationAlways"] == "Yes")
        self._bObservationForceDisplayPlanetMoon = ( data["ObservationForceDisplayPlanetMoon"] == "Yes")
        self._fObservationMaximumLunarFeatureSunAltitude = data["ObservationMaximumLunarFeatureSunAltitude"]
        self._bObservationShowWhenTerminatorIsOnLunarFeature = ( data["ObservationShowWhenTerminatorIsOnLunarFeature"] == "Yes")
        self._fObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg = data["ObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg"]
        self._sObservationPlaceName = data["ObservationPlaceName"]
        self._bDisplayVisibilityTableAsBitmap = ( data["DisplayVisibilityTableAsBitmap"] == "Yes" )
        self._iDisplayNumberOfSlotsForMoon = data["DisplayNumberOfSlotsForMoon"]
        self._iDisplayNumberOfSlotsForMoonFeatures = data["DisplayNumberOfSlotsForMoonFeatures"]
        self._iDisplayNumberOfSlotsForPlanets = data["DisplayNumberOfSlotsForPlanets"]
        self._iDisplayNumberOfSlotsForDeepSky = data["DisplayNumberOfSlotsForDeepSky"]
        self._iDisplayNumberOfMinutesPerSlot = data["DisplayNumberOfMinutesPerSlot"]
        self._iDisplayDaySlotForDataInfo = data["DisplayDaySlotForDataInfo"]
        self._fDisplayMaxAltitudeForObjectLow = data["DisplayMaxAltitudeForObjectLow"]
        self._fDisplayMaxAltitudeForObjectVeryLow = data["DisplayMaxAltitudeForObjectVeryLow"]
        self._fDisplayMaxSunAltitudeForObservableDeepSky = data["DisplayMaxSunAltitudeForObservableDeepSky"]
        self._fDisplayMaxSunAltitudeForObservableBrightObjects = data["DisplayMaxSunAltitudeForObservableBrightObjects"]
        self._fDisplayMaxSunAltitudeForDifficultBrightObjects = data["DisplayMaxSunAltitudeForDifficultBrightObjects"]
        self._fDisplayMaxSunAltitudeFoImpossibleBrightObjects = data["DisplayMaxSunAltitudeFoImpossibleBrightObjects"]
        self._fDisplayMaxSunAltitudeForObservableMediumObjects = data["DisplayMaxSunAltitudeForObservableMediumObjects"]
        self._fDisplayMaxSunAltitudeForDifficultMediumObjects = data["DisplayMaxSunAltitudeForDifficultMediumObjects"]
        fDisplayMaxSunAltitudeForObservableDeepSky = -18.0
        fDisplayMaxSunAltitudeForObservableBrightObjects = -6.0
        fDisplayMaxSunAltitudeForDifficultBrightObjects = 6.0
        fDisplayMaxSunAltitudeFoImpossibleBrightObjects = 12.0
        fDisplayMaxSunAltitudeForObservableMediumObjects = -12.0
        fDisplayMaxSunAltitudeForDifficultMediumObjects = -6.0
        
        # load places and get place set in parameters
        thePlaces = Places()
        self._Place = thePlaces.getPlaceByName(self._sObservationPlaceName)

        # init sky objects
        with open('parameters_SkyObjects.json', 'r') as f:
             data = json.load(f)
        self._SkyObjects = SkyObjects(data["Objects"])
        
        # init Lunar features
        with open('parameters_LunarFeatures.json', 'r') as f:
             data = json.load(f)
        self._LunarFeatures = LunarFeatures(data["LunarFeatures"])

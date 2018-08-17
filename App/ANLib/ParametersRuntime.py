#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Parameters
# 
from toolObjectSerializable import toolObjectSerializable
from Places import Places
from SkyObjects import SkyObjects
from LunarFeatures import LunarFeatures
from toolJSON import toolJSON

#from toolTrace import toolTrace


class ParametersRuntime(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._tRuntimeParameters = {}
        self._tRenderingParameters = {}
        self._tPlacesParameters = {}
        self._tLunarFeaturesParameters = {}
        self._tSkyObjectsParameters = {}
        
        self._sGlobalCurrentVersion = ""
        self._sGlobalPathToWWWFolder = ""
        self._sGlobalPathToAPPFolder = ""
        self._sNightlyBatchDomain = ""
        self._sNightlyBatchEmailAddress = ""
        self._sNightlyEmailSMTPServer = ""
        self._sNightlyEmailSMTPUser = ""
        self._sNightlyEmailSMTPPassword = ""
        self._sNightlyEmailFromAddress = ""
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
        self._iDisplayLanguage = "EN"
        self._iDisplayBitmapType = "JPEG"
        self._iDisplayBitmapExtension = "jpg"
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
        self.__initWithData(dicJSONData)

    def getRuntimeParameter(self, sParameterCode): return self._tRuntimeParameters[sParameterCode]
    def getRenderingParameter(self, sParameterCode): return self._tRenderingParameters[sParameterCode]
    
    def getLanguage(self): return self._iDisplayLanguage
    def getGlobalCurrentVersion(self): return self._sGlobalCurrentVersion
    def getGlobalPathToWWWFolder(self): return self._sGlobalPathToWWWFolder
    def getGlobalPathToAPPFolder(self): return self._sGlobalPathToAPPFolder
    def getNightlyBatchTimeDeltaInHours(self): return self._iNightlyBatchTimeDeltaInHours
    def getNightlyBatchEmailAddress(self): return self._sNightlyBatchEmailAddress
    def getNightlyBatchEmailSMTPServer(self): return self._sNightlyBatchEmailSMTPServer
    def getNightlyBatchEmailSMTPUser(self): return self._sNightlyBatchEmailSMTPUser
    def getNightlyBatchEmailSMTPPassword(self): return self._sNightlyBatchEmailSMTPPassword
    def getNightlyBatchEmailFromAddress(self): return self._sNightlyBatchEmailFromAddress
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
    def getDisplayBitmapType(self): return self._iDisplayBitmapType
    def getDisplayBitmapExtension(self): return self._iDisplayBitmapExtension
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
    def setPlace(self, aPlace): self._Place = aPlace
    
    def __initWithData(self, dicJSONData):
        # init properties
        self._sGlobalCurrentVersion = dicJSONData["currentVersion"]
        self._sGlobalPathToWWWFolder = dicJSONData["GlobalPathToWWWFolder"]
        self._sGlobalPathToAPPFolder = dicJSONData["GlobalPathToAPPFolder"]
        self._iNightlyBatchTimeDeltaInHours = dicJSONData["NightlyBatchTimeDeltaInHours"]
        self._sNightlyBatchEmailAddress = dicJSONData["NightlyBatchEmailAddress"]
        self._sNightlyBatchEmailSMTPServer = dicJSONData["NightlyBatchEmailSMTPServer"]
        self._sNightlyBatchEmailSMTPUser = dicJSONData["NightlyBatchEmailSMTPUser"]
        self._sNightlyBatchEmailSMTPPassword = dicJSONData["NightlyBatchEmailSMTPPassword"]
        self._sNightlyBatchEmailFromAddress = dicJSONData["NightlyBatchEmailFromAddress"]
        self._sNightlyBatchDomain = dicJSONData["NightlyBatchDomain"]
        self._sNightlyBatchHTMLFilname = dicJSONData["NightlyBatchHTMLFilname"]
        self._sObservationStartTimeAsHHMM = dicJSONData["ObservationStartTimeAsHHMM"]
        self._iObservationMaxDurationInHours = dicJSONData["ObservationMaxDurationInHours"]
        self._fObservationMinAltitudeInDeg = dicJSONData["ObservationMinAltitudeInDeg"]
        self._bObservationAlways = ( dicJSONData["ObservationAlways"] == "Yes")
        self._bObservationForceDisplayPlanetMoon = ( dicJSONData["ObservationForceDisplayPlanetMoon"] == "Yes")
        self._fObservationMaximumLunarFeatureSunAltitude = dicJSONData["ObservationMaximumLunarFeatureSunAltitude"]
        self._bObservationShowWhenTerminatorIsOnLunarFeature = ( dicJSONData["ObservationShowWhenTerminatorIsOnLunarFeature"] == "Yes")
        self._fObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg = dicJSONData["ObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg"]
        self._sObservationPlaceName = dicJSONData["ObservationPlaceName"]
        self._iDisplayLanguage = dicJSONData["DisplayLanguage"]
        self._iDisplayBitmapType = dicJSONData["DisplayBitmapType"]
        self._iDisplayBitmapExtension = dicJSONData["DisplayBitmapExtension"]
        self._bDisplayVisibilityTableAsBitmap = ( dicJSONData["DisplayVisibilityTableAsBitmap"] == "Yes" )
        self._iDisplayNumberOfSlotsForMoon = dicJSONData["DisplayNumberOfSlotsForMoon"]
        self._iDisplayNumberOfSlotsForMoonFeatures = dicJSONData["DisplayNumberOfSlotsForMoonFeatures"]
        self._iDisplayNumberOfSlotsForPlanets = dicJSONData["DisplayNumberOfSlotsForPlanets"]
        self._iDisplayNumberOfSlotsForDeepSky = dicJSONData["DisplayNumberOfSlotsForDeepSky"]
        self._iDisplayNumberOfMinutesPerSlot = dicJSONData["DisplayNumberOfMinutesPerSlot"]
        self._iDisplayDaySlotForDataInfo = dicJSONData["DisplayDaySlotForDataInfo"]
        self._fDisplayMaxAltitudeForObjectLow = dicJSONData["DisplayMaxAltitudeForObjectLow"]
        self._fDisplayMaxAltitudeForObjectVeryLow = dicJSONData["DisplayMaxAltitudeForObjectVeryLow"]
        self._fDisplayMaxSunAltitudeForObservableDeepSky = dicJSONData["DisplayMaxSunAltitudeForObservableDeepSky"]
        self._fDisplayMaxSunAltitudeForObservableBrightObjects = dicJSONData["DisplayMaxSunAltitudeForObservableBrightObjects"]
        self._fDisplayMaxSunAltitudeForDifficultBrightObjects = dicJSONData["DisplayMaxSunAltitudeForDifficultBrightObjects"]
        self._fDisplayMaxSunAltitudeFoImpossibleBrightObjects = dicJSONData["DisplayMaxSunAltitudeFoImpossibleBrightObjects"]
        self._fDisplayMaxSunAltitudeForObservableMediumObjects = dicJSONData["DisplayMaxSunAltitudeForObservableMediumObjects"]
        self._fDisplayMaxSunAltitudeForDifficultMediumObjects = dicJSONData["DisplayMaxSunAltitudeForDifficultMediumObjects"]
        fDisplayMaxSunAltitudeForObservableDeepSky = -18.0
        fDisplayMaxSunAltitudeForObservableBrightObjects = -6.0
        fDisplayMaxSunAltitudeForDifficultBrightObjects = 6.0
        fDisplayMaxSunAltitudeFoImpossibleBrightObjects = 12.0
        fDisplayMaxSunAltitudeForObservableMediumObjects = -12.0
        fDisplayMaxSunAltitudeForDifficultMediumObjects = -6.0


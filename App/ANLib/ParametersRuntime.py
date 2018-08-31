#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Parameters
# 
from toolObjectSerializable import toolObjectSerializable
from toolJSON import toolJSON

#from toolTrace import toolTrace


class ParametersRuntime(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._tGlobal = None
        self._tNightlyBatch = None
        self._tObservation = None
        
        self._Place = None
        self.__initWithData(dicJSONData)

    def getRuntimeParameter(self, sParameterCode): return self._tRuntimeParameters[sParameterCode]
    def getRenderingParameter(self, sParameterCode): return self._tRenderingParameters[sParameterCode]
    
    def getGlobal(self, sCode): return self._tGlobal[sCode]
    def getNightlyBatch(self, sCode): return self._tNightlyBatch[sCode]
    def getObservation(self, sCode): return self._tObservation[sCode]
    def getPlace(self): return self._Place
    def setPlace(self, aPlace): self._Place = aPlace
    
    def __initWithData(self, dicJSONData):
        # Global parameters
        self._tGlobal = {}
        self._tGlobal['CurrentVersion'] = dicJSONData["currentVersion"]
        self._tGlobal['PathToWWWFolder'] = dicJSONData["GlobalPathToWWWFolder"]
        self._tGlobal['PathToAPPFolder'] = dicJSONData["GlobalPathToAPPFolder"]
        # Nihtly Batch parameters
        self._tNightlyBatch = {}
        self._tNightlyBatch['TimeDeltaInHours'] = dicJSONData["NightlyBatchTimeDeltaInHours"]
        self._tNightlyBatch['EmailAddress'] = dicJSONData["NightlyBatchEmailAddress"]
        self._tNightlyBatch['EmailSMTPServer'] = dicJSONData["NightlyBatchEmailSMTPServer"]
        self._tNightlyBatch['EmailSMTPUser'] = dicJSONData["NightlyBatchEmailSMTPUser"]
        self._tNightlyBatch['EmailSMTPPassword'] = dicJSONData["NightlyBatchEmailSMTPPassword"]
        self._tNightlyBatch['EmailFromAddress'] = dicJSONData["NightlyBatchEmailFromAddress"]
        self._tNightlyBatch['Domain'] = dicJSONData["NightlyBatchDomain"]
        self._tNightlyBatch['HTMLFilname'] = dicJSONData["NightlyBatchHTMLFilname"]
        # Observation parameters
        self._tObservation = {}
        self._tObservation['StartTimeAsHHMM'] = dicJSONData["ObservationStartTimeAsHHMM"]
        self._tObservation['MaxDurationInHours'] = dicJSONData["ObservationMaxDurationInHours"]
        self._tObservation['MinAltitudeInDeg'] = dicJSONData["ObservationMinAltitudeInDeg"]
        self._tObservation['Always'] = ( dicJSONData["ObservationAlways"] == "Yes")
        self._tObservation['ForceDisplayPlanetMoon'] = ( dicJSONData["ObservationForceDisplayPlanetMoon"] == "Yes")
        self._tObservation['MaximumLunarFeatureSunAltitude'] = dicJSONData["ObservationMaximumLunarFeatureSunAltitude"]
        self._tObservation['ShowWhenTerminatorIsOnLunarFeature'] = ( dicJSONData["ObservationShowWhenTerminatorIsOnLunarFeature"] == "Yes")
        self._tObservation['ShowWhenTerminatorIsOnLunarFeatureWithinDeg'] = dicJSONData["ObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg"]
        self._tObservation['PlaceName'] = dicJSONData["ObservationPlaceName"]


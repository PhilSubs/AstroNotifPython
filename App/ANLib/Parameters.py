#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Parameters
# 
from toolObjectSerializable import toolObjectSerializable
from ParametersLocalization import ParametersLocalization
from ParametersLunarFeatures import ParametersLunarFeatures
from ParametersRendering import ParametersRendering
from ParametersRuntime import ParametersRuntime
from ParametersSkyObjects import ParametersSkyObjects
from ParametersPlaces import ParametersPlaces
from toolJSON import toolJSON

#from toolTrace import toolTrace


class Parameters(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._ParametersLocalization = None
        self._ParametersLunarFeatures = None
        self._ParametersRendering = None
        self._ParametersRuntime = None
        self._ParametersSkyObjects = None
        self._ParametersPlaces = None
        self.__load()

    def Localization(self): return self._ParametersLocalization
    def LunarFeatures(self): return self._ParametersLunarFeatures
    def Rendering(self): return self._ParametersRendering
    def Runtime(self): return self._ParametersRuntime
    def SkyObjects(self): return self._ParametersSkyObjects
    def Places(self): return self._ParametersPlaces
    
    def __load(self):
        self._ParametersRuntime       = ParametersRuntime(toolJSON.getContent('parameters_Runtime.json'))

        self._ParametersLocalization  = ParametersLocalization(toolJSON.getContent('parameters_Localization.json'), self._ParametersRuntime.getLanguage())
        self._ParametersLunarFeatures = ParametersLunarFeatures(toolJSON.getContent('parameters_LunarFeatures.json'))
        self._ParametersRendering     = ParametersRendering(toolJSON.getContent('parameters_Rendering.json'))
        self._ParametersSkyObjects    = ParametersSkyObjects(toolJSON.getContent('parameters_SkyObjects.json'))
        self._ParametersPlaces        = ParametersPlaces(toolJSON.getContent('parameters_Places.json'))

        self._ParametersRuntime.setPlace(self._ParametersPlaces.getPlaceByName(self._ParametersRuntime.getObservationPlaceName()))

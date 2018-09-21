#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class LunarFeatures
# 
from ParametersLunarFeature import ParametersLunarFeature
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace

class ParametersLunarFeatures(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._dicLunarFeatures = {}
        self.__initWithData(dicJSONData)
        
    def getCount(self): return len(self._dicLunarFeatures)
    def getLunarFeatureByName(self, sName): return self._dicLunarFeatures.get(sName)
    def getLunarFeatureByIndex(self, iIndex):
        x = 0
        while (x < len(self._dicLunarFeatures) and self._dicLunarFeatures.values()[x].getIndex() != iIndex):
            x = x + 1
        if x < len(self._dicLunarFeatures):
            return self._dicLunarFeatures.values()[x]
        else:
            raise NameError('Error in getLunarFeatureByIndex: ' + str(x) + ' value reached while searching index ' + str(iIndex) + '/' + str(len(self._dicLunarFeatures)) + '.')
    def __initWithData(self, dicJSONData):
        # init Sky Objects array of LunarFeature objects
        for iId in range (0, len(dicJSONData)):
            sLunarFeatureKey = list(dicJSONData.keys())[iId]
            newLunarFeature = ParametersLunarFeature(iId, dicJSONData[sLunarFeatureKey]["ID"], dicJSONData[sLunarFeatureKey]["Name"], dicJSONData[sLunarFeatureKey]["Longitude"], dicJSONData[sLunarFeatureKey]["LongitudeMin"], dicJSONData[sLunarFeatureKey]["LongitudeMax"], dicJSONData[sLunarFeatureKey]["Latitude"], dicJSONData[sLunarFeatureKey]["IsFavourite"], dicJSONData[sLunarFeatureKey]["NotifyWhenObservable"], dicJSONData[sLunarFeatureKey]["Type"], dicJSONData[sLunarFeatureKey]["Height"], dicJSONData[sLunarFeatureKey]["Diameter"], dicJSONData[sLunarFeatureKey]["Depth"], dicJSONData[sLunarFeatureKey]["Length"], dicJSONData[sLunarFeatureKey]["Breadth"],  dicJSONData[sLunarFeatureKey]["Rukl"])
            self._dicLunarFeatures[newLunarFeature.getName()] = newLunarFeature
            

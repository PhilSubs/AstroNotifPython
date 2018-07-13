#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class LunarFeatures
# 
from LunarFeature import LunarFeature
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace

class LunarFeatures(toolObjectSerializable):
    def __init__(self, dataLunarFeatures):
        toolObjectSerializable.__init__(self)
        self._dicLunarFeatures = {}
        self.__initLunarFeatures(dataLunarFeatures)
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
    def __initLunarFeatures(self, dataLunarFeatures):
        # init Sky Objects array of LunarFeature objects
        for iId in range (0, len(dataLunarFeatures)):
            sLunarFeatureKey = list(dataLunarFeatures.keys())[iId]
            newLunarFeature = LunarFeature(iId, dataLunarFeatures[sLunarFeatureKey]["ID"], dataLunarFeatures[sLunarFeatureKey]["Name"], dataLunarFeatures[sLunarFeatureKey]["Longitude"], dataLunarFeatures[sLunarFeatureKey]["LongitudeMin"], dataLunarFeatures[sLunarFeatureKey]["LongitudeMax"], dataLunarFeatures[sLunarFeatureKey]["Latitude"], dataLunarFeatures[sLunarFeatureKey]["IsFavourite"], dataLunarFeatures[sLunarFeatureKey]["Type"], dataLunarFeatures[sLunarFeatureKey]["Height"], dataLunarFeatures[sLunarFeatureKey]["Diameter"], dataLunarFeatures[sLunarFeatureKey]["Depth"], dataLunarFeatures[sLunarFeatureKey]["Length"], dataLunarFeatures[sLunarFeatureKey]["Breadth"],  dataLunarFeatures[sLunarFeatureKey]["Rukl"])
            self._dicLunarFeatures[newLunarFeature.getName()] = newLunarFeature
            

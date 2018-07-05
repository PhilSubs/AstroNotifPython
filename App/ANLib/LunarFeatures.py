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
        for x in range(0,  len(dataLunarFeatures)):
            newLunarFeature = LunarFeature(x, dataLunarFeatures[x]["ID"], dataLunarFeatures[x]["Name"], dataLunarFeatures[x]["Longitude"], dataLunarFeatures[x]["LongitudeMin"], dataLunarFeatures[x]["LongitudeMax"], dataLunarFeatures[x]["Latitude"], dataLunarFeatures[x]["IsFavourite"], dataLunarFeatures[x]["Type"], dataLunarFeatures[x]["Height"], dataLunarFeatures[x]["Diameter"], dataLunarFeatures[x]["Depth"], dataLunarFeatures[x]["Length"], dataLunarFeatures[x]["Breadth"],  dataLunarFeatures[x]["Rukl"])
            self._dicLunarFeatures[newLunarFeature.getName()] = newLunarFeature
            

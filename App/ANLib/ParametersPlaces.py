#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Places
# 
from ParametersPlace import ParametersPlace
from toolObjectSerializable import toolObjectSerializable
from toolJSON import toolJSON
#from toolTrace import toolTrace

class ParametersPlaces(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._iCount = None
        self._dictPlaces = {}
        self.__initWithData(dicJSONData)
        
    def getCount(self): return self._iCount
    def getPlaceByName(self, sName): return self._dictPlaces.get(sName)
    def getPlaceByIndex(self, iIndex): return self._dictPlaces.values()[iIndex]

    def __initWithData(self, dicJSONData):
        for iId in range (0, len(dicJSONData)):
            sPlaceKey = list(dicJSONData.keys())[iId]
            newPlace = ParametersPlace(dicJSONData[sPlaceKey]["Name"], dicJSONData[sPlaceKey]["Longitude"], dicJSONData[sPlaceKey]["Latitude"])
            self._dictPlaces[newPlace.getName()] = newPlace
            newPlace.initObstructedSkyAreas(dicJSONData[sPlaceKey]["ObstructedSkyAreas"])
        self._iCount = len(self._dictPlaces)

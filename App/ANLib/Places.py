#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Places
# 
from Place import Place
from toolObjectSerializable import toolObjectSerializable
from toolJSON import toolJSON
#from toolTrace import toolTrace

class Places(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._iCount = None
        self._dictPlaces = {}
        self.__loadFromFile()
    def getCount(self): return self._iCount
    def getPlaceByName(self, sName): return self._dictPlaces.get(sName)
    def getPlaceByIndex(self, iIndex): return self._dictPlaces.values()[iIndex]
    def __loadFromFile(self):
        data = toolJSON.getContent('parameters_Places.json')
        for iId in range (0, len(data)):
            sPlaceKey = list(data.keys())[iId]
            newPlace = Place(data[sPlaceKey]["Name"], data[sPlaceKey]["Longitude"], data[sPlaceKey]["Latitude"])
            self._dictPlaces[newPlace.getName()] = newPlace
            newPlace.initObstructedSkyAreas(data[sPlaceKey]["ObstructedSkyAreas"])
        self._iCount = len(self._dictPlaces)

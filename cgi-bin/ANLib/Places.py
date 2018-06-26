#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Places
# 
import json
from Place import Place
from toolObjectSerializable import toolObjectSerializable
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
        with open('parameters_Places.json', 'r') as f:
             data = json.load(f)
        for x in range(0,  len(data)):
            newPlace = Place(data[x]["Name"], data[x]["Longitude"], data[x]["Latitude"])
            self._dictPlaces[newPlace.getName()] = newPlace
            newPlace.initObstructedSkyAreas(data[x]["ObstructedSkyAreas"])
        self._iCount = len(self._dictPlaces)
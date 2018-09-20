#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Place
# 
from toolObjectSerializable import toolObjectSerializable
from ParametersObstructedSkyAreas import ParametersObstructedSkyAreas

#from toolTrace import toolTrace


class ParametersPlace(toolObjectSerializable):
    def __init__(self, sName, fLocalTimeDifferenceWithGMT, fLongitude, fLatitude):
        toolObjectSerializable.__init__(self)
        self._sName = sName
        self._fLocalTimeDifferenceWithGMT = fLocalTimeDifferenceWithGMT
        self._fLongitude = fLongitude
        self._fLatitude = fLatitude
        self._theObstructedSkyAreas = None
    def getName(self): return self._sName
    def setName(self, sName): self._sName = sName
    def getLocalTimeDifferenceWithGMT(self): return self._fLocalTimeDifferenceWithGMT
    def setLocalTimeDifferenceWithGMT(self, fLocalTimeDifferenceWithGMT): self._fLocalTimeDifferenceWithGMT = fLocalTimeDifferenceWithGMT
    def getLongitude(self): return self._fLongitude
    def setLongitude(self, fLongitude): self._fLongitude = fLongitude
    def getLatitude(self): return self._fLatitude
    def setLatitude(self, fLatitude): self._fLatitude = fLatitude
    def getObstructedSkyAreas(self): return self._theObstructedSkyAreas
    def initObstructedSkyAreas(self, dataObstructedSkyAreas):
        self._theObstructedSkyAreas= ParametersObstructedSkyAreas(dataObstructedSkyAreas)

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ObstructedSkyAreas
# 
from ObstructedSkyArea import ObstructedSkyArea
from toolObjectSerializable import toolObjectSerializable
import math
#from toolTrace import toolTrace

class ObstructedSkyAreas(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._iCount = None
        self._arrObstructedSkyAreas = []
        self._sObstructedSkyAreasMap = ""
    def getCount(self): return self._iCount
    def getObstructedSkyAreaByIndex(self, iIndex): return self._arrObstructedSkyAreas[iIndex]
    def initObstructedSkyAreas(self, dataObstructedSkyAreas):
        # init ObstructedSkyAreas array of ObstructedSkyArea objects
        for x in range(0,  len(dataObstructedSkyAreas)):
            newObstructedSkyArea = ObstructedSkyArea(dataObstructedSkyAreas[x]["Azimut-Min"], dataObstructedSkyAreas[x]["Azimut-Max"], dataObstructedSkyAreas[x]["Altitude-Min"], dataObstructedSkyAreas[x]["Altitude-Max"])
            self._arrObstructedSkyAreas.append(newObstructedSkyArea)
        self._iCount = len(self._arrObstructedSkyAreas)
        # init Visibility Zones maps
        self._sObstructedSkyAreasMap = "1"*180*360
        # override with ObstructedSkyAreas
        iPos = 0
        for i in range(0, self._iCount):
            fAz = self._arrObstructedSkyAreas[i].getAzimutMinInDeg()
            while (fAz <= self._arrObstructedSkyAreas[i].getAzimutMaxInDeg()):
                fAlt = self._arrObstructedSkyAreas[i].getAltitudeMinInDeg()
                while (fAlt <= self._arrObstructedSkyAreas[i].getAltitudeMaxInDeg()):
                    iPos = self.__getIndexFromAzimutAltitude(fAz, fAlt)
                    if (iPos == 0):
                        self._sObstructedSkyAreasMap = "0" + self._sObstructedSkyAreasMap[1:]
                    elif (iPos == 64799):
                        self._sObstructedSkyAreasMap = self._sObstructedSkyAreasMap[:iPos] + "0"
                    else:
                        self._sObstructedSkyAreasMap = self._sObstructedSkyAreasMap[:iPos] + "0" + self._sObstructedSkyAreasMap[iPos + 1:]
                    fAlt = fAlt + 1.0
                fAz = fAz + 1.0
    def getObstructedSkyAreasMap(self): return self._sObstructedSkyAreasMap
    def getVisibilityStatus(self, fAzimut, fAltitude): 
        # Visibility Status:
        #         0: Obstructed
        #         1: Clear unobstructed
        return self._sObstructedSkyAreasMap[self.__getIndexFromAzimutAltitude(fAzimut, fAltitude)]
    def __getIndexFromAzimutAltitude(self, fAzimut, fAltitude): 
        # Azimut between 0.0 and 359.9
        # Altitude between -89.9 and 89.9
        iAzimut = math.floor(fAzimut)
        if (fAltitude > 0):
            iAltitude = math.ceil(fAltitude)
        else:
            iAltitude = math.floor(fAltitude)
        return int(iAzimut*180 + (90 + iAltitude))
            

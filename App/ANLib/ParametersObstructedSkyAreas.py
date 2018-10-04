#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ObstructedSkyAreas
# 
from ParametersObstructedSkyArea import ParametersObstructedSkyArea
from toolObjectSerializable import toolObjectSerializable
import math
#from toolTrace import toolTrace

class ParametersObstructedSkyAreas(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._iCount = None
        self._arrObstructedSkyAreas = []
        self._sObstructedSkyAreasMap = ""
        self.__initWithData(dicJSONData)
        
    def getCount(self): return self._iCount
    def getObstructedSkyAreaByIndex(self, iIndex): return self._arrObstructedSkyAreas[iIndex]
    def getObstructedSkyAreasMap(self): return self._sObstructedSkyAreasMap
    def getVisibilityStatus(self, fAzimut, fAltitude): 
        # Visibility Status:
        #         0: Obstructed
        #         1: Clear unobstructed
        return self._sObstructedSkyAreasMap[self.__getIndexFromAzimutAltitude(fAzimut, fAltitude)]
    def getMinMaxAltitudeObstructedForAzimut(self, fAzimut):
        fMinAltitude = 999.0
        fMaxAltitude = -999.0
        fAzimut360 = (fAzimut + 360.0) % 360.0
        for iAltitude in range (0, 90):
            fAltitude = float(iAltitude)
            if self.getVisibilityStatus(fAzimut360, fAltitude) == "0":
                if fAltitude > fMaxAltitude: fMaxAltitude = fAltitude
                if fAltitude < fMinAltitude: fMinAltitude = fAltitude
        if fMinAltitude == 999.0:
            fMinAltitude = 0
            fMaxAltitude = 0
        return fMinAltitude, fMaxAltitude
    def __getIndexFromAzimutAltitude(self, fAzimut, fAltitude): 
        # Azimut between 0.0 and 359.9
        # Altitude between -89.9 and 89.9
        iAzimut = math.floor(fAzimut)
        if (fAltitude > 0):
            iAltitude = math.ceil(fAltitude)
        else:
            iAltitude = math.floor(fAltitude)
        return int(iAzimut*180 + (90 + iAltitude))
            
    def __initWithData(self, dicJSONData):
        # init ObstructedSkyAreas array of ObstructedSkyArea objects
        for iId in range (0, len(dicJSONData)):
            sObstructedSkyAreaKey = list(dicJSONData.keys())[iId]
            newObstructedSkyArea = ParametersObstructedSkyArea(dicJSONData[sObstructedSkyAreaKey]["Comment"], eval(dicJSONData[sObstructedSkyAreaKey]["Color"]), dicJSONData[sObstructedSkyAreaKey]["Azimut-Min"], dicJSONData[sObstructedSkyAreaKey]["Azimut-Max"], dicJSONData[sObstructedSkyAreaKey]["Altitude-Min"], dicJSONData[sObstructedSkyAreaKey]["Altitude-Max"])
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

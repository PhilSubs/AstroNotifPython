#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class EphemeridesMoon
# 
import math
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes
from MeeusAlgorithms import MeeusAlgorithms

#from toolTrace import toolTrace

class EphemeridesMoonMeeus(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._sName = "Moon"
        self._sType = "Moon"
        self._oMeeusAlgorithm = None
        
    def getDistInKM(self):                                          return self._oMeeusAlgorithm.getDistanceInKm("Moon")
    def getIllumination(self):                                      return self._oMeeusAlgorithm.getIllumination("Moon")
    def getPositionAngle(self):                                     return self._oMeeusAlgorithm.getPositionAngle("Moon")
    def getMoonSelenographicColongitude(self):                      return self._oMeeusAlgorithm.getSelenographicColongitude("Moon")
    def getMoonSelenographicLatitude(self):                         return self._oMeeusAlgorithm.getSubSolarSelenographicLatitude("Moon")
    def getMoonSelenographicLongitude(self):                        return self._oMeeusAlgorithm.getSubSolarSelenographicLongitude("Moon")
    def getName(self):                                              return self._sName
    def getPhase(self):                                             return self._oMeeusAlgorithm.getPhaseAngle("Moon")
    def getDeclination(self):                                       return self._oMeeusAlgorithm.getDeclination("Moon")
    def getRightAscension(self):                                    return self._oMeeusAlgorithm.getRightAscension("Moon")
    def getAzimut(self, fObserverLongitude, fObserverLatitude):     return self._oMeeusAlgorithm.getAzimut("Moon", fObserverLongitude, fObserverLatitude)
    def getElevation(self, fObserverLongitude, fObserverLatitude):  return self._oMeeusAlgorithm.getElevation("Moon", fObserverLongitude, fObserverLatitude)
    def getType(self):                                              return self._sType    
    
    def computeEphemerides(self, sDate, sTime, fSunMeanAnoInDeg, fSunArgPerihelInDeg):
        self._oMeeusAlgorithm = MeeusAlgorithms( sDate, sTime)

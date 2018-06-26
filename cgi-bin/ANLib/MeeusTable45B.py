#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class MeeusTable45B
# 
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace
import math

class MeeusTable45B(toolObjectSerializable):
    iArgD = [0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 4, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4, 4, 0, 4, 2, 2, 2, 2, 0, 2, 2, 2, 2, 4, 2, 2, 0, 2, 1, 1, 0, 2, 1, 2, 0, 4, 4, 1, 4, 1, 4, 2]
    iArgM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, -1, -1, -1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 1, 0, -1, -2, 0, 1, 1, 1, 1, 1, 0, -1, 1, 0, -1, 0, 0, 0, -1, -2]
    iArgMprime = [0, 1, 1, 0, -1, -1, 0, 2, 1, 2, 0, -2, 1, 0, -1, 0, -1, -1, -1, 0, 0, -1, 0, 1, 1, 0, 0, 3, 0, -1, 1, -2, 0, 2, 1, -2, 3, 2, -3, -1, 0, 0, 1, 0, 1, 1, 0, 0, -2, -1, 1, -2, 2, -2, -1, 1, 1, -1, 0, 0]
    iArgF = [1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 3, 1, 1, 1, -1, -1, -1, 1, -1, 1, -3, 1, -3, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 3, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1]
    iArgEpsilonb = [5128122, 280602, 277693, 173237, 55413, 46271, 32573, 17198, 9266, 5522, 8216, 4324, 4200, -3359, 2463, 2211, 2065, -1870, 1828, -1794, -1749, -1565, -1491, -1475, -1410, -1344, -1335, 1107, 1021, 833, 777, 671, 607, 596, 491, -451, 439, 422, 421, -366, -351, 331, 315, 302, -283, -229, 223, 223, -220, -220, -185, 181, -177, 176, 166, -164, 132, -119, 115, 107]

    def __init__(self, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity):
        toolObjectSerializable.__init__(self)
        self._fMoonMeanElongation = fMoonMeanElongation
        self._fSunMeanAnomaly = fSunMeanAnomaly
        self._fMoonMeanAnomaly = fMoonMeanAnomaly
        self._fMoonArgumentOfLatitude = fMoonArgumentOfLatitude
        self._fEccentricity = fEccentricity
        
    def getArgument(self, iIndex): return (MeeusTable45B.iArgD[iIndex] * self._fMoonMeanElongation + MeeusTable45B.iArgM[iIndex] * self._fSunMeanAnomaly + MeeusTable45B.iArgMprime[iIndex] * self._fMoonMeanAnomaly + MeeusTable45B.iArgF[iIndex] * self._fMoonArgumentOfLatitude) / 360.0 * 2.0 * math.pi
    def getTermEpsilonB(self, iIndex): return MeeusTable45B.iArgEpsilonb[iIndex] * math.sin(self.getArgument(iIndex))
    def getTermEpsilonBWithEccentricity(self, iIndex): 
        if (MeeusTable45B.iArgM[iIndex] == 1 or MeeusTable45B.iArgM[iIndex] == -1): 
            return self.getTermEpsilonB(iIndex) * self._fEccentricity
        elif (MeeusTable45B.iArgM[iIndex] == 2 or MeeusTable45B.iArgM[iIndex] == -2): 
            return self.getTermEpsilonB(iIndex) * self._fEccentricity**2
        else:
            return self.getTermEpsilonB(iIndex)
    def getSumEpsilonB(self):
        fSum = 0.0
        for iIndex in range(0, 60):
            fSum += self.getTermEpsilonBWithEccentricity(iIndex)
        return fSum

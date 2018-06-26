#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class MeeusTable45A
# 
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace
import math

class MeeusTable45A(toolObjectSerializable):
    iArgD = [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1, 1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2, 4, 0, 3, 2, 4, 0, 2, 2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2, 2]
    iArgM = [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2, 0, 0, -1, 0, 0, 1, -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0, 0]
    iArgMprime = [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 3, -2, -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0, 2, 0, -1, 1, 0, -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, 2, 1, -2, -3, 2, 1, -1, 3, -1]
    iArgF = [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2, 2, 0, 2, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, -2]
    iArgEpsilon1 = [6288774, 1274027, 658314, 213618, -185116, -114332, 58793, 57066, 53322, 45758, -40923, -34720, -30383, 15327, -12528, 10980, 10675, 10034, 8548, -7888, -6766, -5163, 4987, 4036, 3994, 3861, 3665, -2689, -2602, 2390, -2348, 2236, -2120, -2069, 2048, -1773, -1595, 1215, -1110, -892, -810, 759, -713, -700, 691, 596, 549, 537, 520, -487, -399, -381, 351, -340, 330, 327, -323, 299, 294, 0]
    iArgEpsilonR = [-20905355, -3699111, -2955968, -569925, 48888, -3149, 246158, -152138, -170733, -204586, -129620, 108743, 104755, 10321, 0, 79661, -34782, -23210, -21636, 24208, 30824, -8379, -16675, -12831, -10445, -11650, 14403, -7003, 0, 10056, 6322, -9884, 5751, 0, -4950, 4130, 0, -3958, 0, 3258, 2616, -1897, -2117, 2354, 0, 0, -1423, -1117, -1571, -1739, 0, -4421, 0, 0, 0, 0, 1165, 0, 0, 8752]

    def __init__(self, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity):
        toolObjectSerializable.__init__(self)
        self._fMoonMeanElongation = fMoonMeanElongation
        self._fSunMeanAnomaly = fSunMeanAnomaly
        self._fMoonMeanAnomaly = fMoonMeanAnomaly
        self._fMoonArgumentOfLatitude = fMoonArgumentOfLatitude
        self._fEccentricity = fEccentricity
        
    def getArgument(self, iIndex): return (MeeusTable45A.iArgD[iIndex] * self._fMoonMeanElongation + MeeusTable45A.iArgM[iIndex] * self._fSunMeanAnomaly + MeeusTable45A.iArgMprime[iIndex] * self._fMoonMeanAnomaly + MeeusTable45A.iArgF[iIndex] * self._fMoonArgumentOfLatitude) / 360.0 * 2.0 * math.pi
    def getTermEpsilon1(self, iIndex): return MeeusTable45A.iArgEpsilon1[iIndex] * math.sin(self.getArgument(iIndex))
    def getTermEpsilonR(self, iIndex): return MeeusTable45A.iArgEpsilonR[iIndex] * math.cos(self.getArgument(iIndex))
    def getTermEpsilon1WithEccentricity(self, iIndex): 
        if (MeeusTable45A.iArgM[iIndex] == 1 or MeeusTable45A.iArgM[iIndex] == -1): 
            return self.getTermEpsilon1(iIndex) * self._fEccentricity
        elif (MeeusTable45A.iArgM[iIndex] == 2 or MeeusTable45A.iArgM[iIndex] == -2): 
            return self.getTermEpsilon1(iIndex) * self._fEccentricity**2
        else:
            return self.getTermEpsilon1(iIndex)
    def getTermEpsilonRWithEccentricity(self, iIndex): 
        if (MeeusTable45A.iArgM[iIndex] == 1 or MeeusTable45A.iArgM[iIndex] == -1): 
            return self.getTermEpsilonR(iIndex) * self._fEccentricity
        elif (MeeusTable45A.iArgM[iIndex] == 2 or MeeusTable45A.iArgM[iIndex] == -2): 
            return self.getTermEpsilonR(iIndex) * self._fEccentricity**2
        else:
            return self.getTermEpsilonR(iIndex)
    def getSumEpsilon1(self):
        fSum = 0.0
        for iIndex in range(0, 60):
            fSum += self.getTermEpsilon1WithEccentricity(iIndex)
        return fSum
    def getSumEpsilonR(self):
        fSum = 0.0
        for iIndex in range(0, 60):
            fSum += self.getTermEpsilonRWithEccentricity(iIndex)
        return fSum
    
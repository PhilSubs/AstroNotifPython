#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class EphemeridesSun
# 
import math
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes

#from toolTrace import toolTrace

class EphemeridesSun(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._sName = "Sun"
        self._sType = "Star"
        
        self._fObliqEclipInDeg = 0.0;     # ecl = obliquity of the ecliptic
        self._fLongAscNodeInDeg = 0.0;    # N = longitude of the ascending node
        self._fInclEclipInDeg = 0.0;      # i = inclination to the ecliptic (plane of the Earth's orbit)
        self._fArgPerihelInDeg = 0.0;     # w = argument of perihelion
        self._fMeanDistSunInAU = 0.0;     # a = semi-major axis, or mean distance from Sun
        self._fEccentricInDeg = 0.0;      # e = eccentricity (0=circle, 0-1=ellipse, 1=parabola)
        self._fMeanAnoInDeg = 0.0;        # M = mean anomaly (0 at perihelion; increases uniformly with time)  
        self._fLongPerihelion = 0.0;      # w1 = longitude of perihelion
        self._fMeanLongInDeg = 0.0;       # L = mean longitude
        self._fPerihelionDistInUA = 0.0;  # q = perihelion distance
        self._fAphelionDistInUA = 0.0;    # Q = aphelion distance
        self._fOrbPeriodInYears = 0.0;    # P = orbital period (years if a is in AU, astronomical units)
        self._fEccentricAnoInDeg = 0.0;   # E = Eccentric Anomaly
        self._fSunDistInUA = 0.0;         # r = Sun's distance
        self._fTrueAnoInDeg = 0.0;        # v = True Anomaly
        self._fRAInDeg = 0.0;             # RA = Right Ascension
        self._fDecInDeg = 0.0;            # Dec = Declination
        
    def getName(self): return self._sName
    def getType(self): return self._sType
    def computeEphemerides(self, fDateValue):
        self._fObliqEclipInDeg = CommonAstroFormulaes.getObliqEclipInDegForDateValue(fDateValue)
        # Orbital elements of the Sun
        self._fLongAscNodeInDeg = 0.0
        self._fInclEclipInDeg = 0.0
        self._fArgPerihelInDeg = (282.9404 + 4.70935 * math.pow(10, -5) * fDateValue) % 360
        self._fMeanDistSunInAU = 1.000000
        self._fEccentricInDeg = (0.016709 - 1.151 * math.pow(10, -9) * fDateValue) % 360
        self._fMeanAnoInDeg = (356.0470 + 0.9856002585 * fDateValue) % 360
        # Related orbital elements
        self._fLongPerihelion = self._fLongAscNodeInDeg + self._fArgPerihelInDeg
        self._fMeanLongInDeg  = self._fMeanAnoInDeg + self._fLongPerihelion
        self._fPerihelionDistInUA = self._fMeanDistSunInAU * (1 - self._fEccentricInDeg)
        self._fAphelionDistInUA = self._fMeanDistSunInAU * (1 + self._fEccentricInDeg)
        self._fOrbPeriodInYears = math.pow(self._fMeanDistSunInAU, 1.5)
        #eccentric anomaly E from the mean anomaly M and from the eccentricity e (E and M in degrees)
        self._fEccentricAnoInDeg = self._fMeanAnoInDeg + self._fEccentricInDeg * (180.0 / math.pi) * math.sin(math.radians(self._fMeanAnoInDeg)) * ( 1.0 + self._fEccentricInDeg * math.cos(math.radians(self._fMeanAnoInDeg)) )   
        # Sun's distance r and its true anomaly v
        fXV = math.cos(math.radians(self._fEccentricAnoInDeg)) - self._fEccentricInDeg
        fYV = math.sqrt(1.0 - self._fEccentricInDeg * self._fEccentricInDeg) * math.sin(math.radians(self._fEccentricAnoInDeg))
        self._fSunDistInUA = math.sqrt( fXV * fXV + fYV * fYV )
        self._fTrueAnoInDeg = math.degrees(math.atan2( fYV, fXV ))
        # Sun's true longitude
        self._fLonSunInDeg = self._fTrueAnoInDeg + self._fArgPerihelInDeg
        # Rectangular geocentric coordinates
        fXS = self._fSunDistInUA * math.cos(math.radians(self._fLonSunInDeg))
        fYS = self._fSunDistInUA * math.sin(math.radians(self._fLonSunInDeg))
        # Equatorial rectangular geocentric coordinates
        fXE = fXS
        fYE = fYS * math.cos(math.radians(self._fObliqEclipInDeg))
        fZE = fYS * math.sin(math.radians(self._fObliqEclipInDeg))
        # Sun's Right Ascension and Declination
        self._fRAInDeg = math.degrees(math.atan2(fYE, fXE))
        self._fDecInDeg = math.degrees(math.atan2(fZE, math.sqrt(fXE * fXE + fYE * fYE)))
  
    def getObliqEclipInDeg(self):   return self._fObliqEclipInDeg
    def getLongAscNodeInDeg(self):  return self._fLongAscNodeInDeg
    def getInclEclipInDeg(self):    return self._fInclEclipInDeg
    def getArgPerihelInDeg(self):   return self._fArgPerihelInDeg
    def getMeanDistSunInAU(self):   return self._fMeanDistSunInAU
    def getEccentricInDeg(self):    return self._fEccentricInDeg
    def getMeanAnoInDeg(self):      return self._fMeanAnoInDeg
    def getMeanLongInDeg(self):     return self._fMeanLongInDeg
    def getEccentricAnoInDeg(self): return self._fEccentricAnoInDeg
    def getSunDistInUA(self):       return self._fSunDistInUA
    def getTrueAnoInDeg(self):      return self._fTrueAnoInDeg
    def getRAInDeg(self):           return self._fRAInDeg
    def getDecInDeg(self):          return self._fDecInDeg
    def getDistanceInKm(self):      return int(round((self._fSunDistInUA * 149600) / 10.0, 0) * 10000)

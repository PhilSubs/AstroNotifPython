#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class EphemeridesMoon
# 
import math
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes

#from toolTrace import toolTrace

class EphemeridesMoon(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._sName = "Moon"
        self._sType = "Moon"
        
        self._fLongPerihelion = 0.0       # w1 = longitude of perihelion
        self._fLongAscNodeInDeg = 0.0     # N = longitude of the ascending node
        self._fArgPerihelInDeg = 0.0      # w = argument of perihelion
        self._fMeanLongInDeg = 0.0        # L = mean longitude
        self._fInclEclipInDeg = 0.0;      # i = inclination to the ecliptic (plane of the Earth's orbit)
        self._fMeanAnoInDeg = 0.0         # M = mean anomaly (0 at perihelion; increases uniformly with time)  
        self._fPerihelionDistInUA = 0.0   # q = perihelion distance
        self._fMeanDistSunInAU = 0.0      # a = semi-major axis, or mean distance from Sun
        self._fEccentricInDeg = 0.0       # e = eccentricity (0=circle, 0-1=ellipse, 1=parabola)
        self._fAphelionDistInUA = 0.0     # Q = aphelion distance
        self._fOrbPeriodInYears = 0.0     # P = orbital period (years if a is in AU, astronomical units)
        self._fEccentricAnoInDeg = 0.0    # E = Eccentric Anomaly
        self._fTrueAnoInDeg = 0.0         # v = True Anomaly
        self._fSunDistInUA = 0.0          # r = Sun's distance
        self._fLongitudeEcliptic = 0.0    # LonEcl = Longitude Ecliptic
        self._fLatitudeEcliptic = 0.0     # LatEcl = Longitude Ecliptic
        self._fGeocentricCoordX = 0.0     # xg = Geocentric Coordinate X
        self._fGeocentricCoordY = 0.0     # yg = Geocentric Coordinate Y
        self._fGeocentricCoordZ = 0.0     # zg = Geocentric Coordinate Z
        self._fRAInDeg = 0.0;             # RA = Right Ascension
        self._fDecInDeg = 0.0;            # Dec = Declination
        self._fTopoRAInDeg = 0.0;         # TopoRA = Right Ascension
        self._fTopoDecInDeg = 0.0;        # TopoDec = Declination
        
    def getName(self): return self._sName
    def getType(self): return self._sType
    def computeEphemerides(self, fDateValue, fSunMeanAnoInDeg, fSunArgPerihelInDeg):
        self._fObliqEclipInDeg = CommonAstroFormulaes.getObliqEclipInDegForDateValue(fDateValue)
        #Orbital elements of the Moon:
        self._fLongAscNodeInDeg = (125.1228 - 0.0529538083 * fDateValue) % 360.0
        self._fInclEclipInDeg = 5.1454
        self._fArgPerihelInDeg = (318.0634 + 0.1643573223 * fDateValue) % 360.0
        self._fMeanDistSunInAU = 60.2666  
        self._fEccentricInDeg = 0.054900
        self._fMeanAnoInDeg = (115.3654 + 13.0649929509 * fDateValue) % 360.0
        # Related orbital elements are
        self._fLongPerihelion = self._fLongAscNodeInDeg + self._fArgPerihelInDeg
        self._fMeanLongInDeg  = self._fMeanAnoInDeg + self._fLongPerihelion
        self._fPerihelionDistInUA  = self._fMeanDistSunInAU * (1.0 - self._fEccentricInDeg)
        self._fPerihelionDistInUA  = self._fMeanDistSunInAU * (1.0 + self._fEccentricInDeg)
        self._fOrbPeriodInYears  = self._fMeanDistSunInAU ** 1.5
        # compute the eccentric anomaly, E, from M, the mean anomaly, and e, the eccentricity (E and M in degrees)
        self._fEccentricAnoInDeg = self._fMeanAnoInDeg + self._fEccentricInDeg * (180.0 / math.pi) * math.sin(math.radians(self._fMeanAnoInDeg)) * ( 1.0 + self._fEccentricInDeg * math.cos(math.radians(self._fMeanAnoInDeg)) )
        if self._fEccentricAnoInDeg > 0.5:
            fE1 = self._fEccentricAnoInDeg
            fE0 = 9999.0 # init value to pass the while test on first iteration
            iIter = 0
            while iIter < 1000 and math.fabs(fE0 - fE1) > 0.001:
                fE0 = fE1
                fE1 = fE0 - ( fE0 - self._fEccentricInDeg * (180.0 / math.pi) * math.sin(math.radians(fE0)) - self._fMeanAnoInDeg ) / ( 1.0 - self._fEccentricInDeg * math.cos(math.radians(fE0)) )
            self._fEccentricAnoInDeg = fE1
        # planet's distance and true anomaly
        fxv = self._fMeanDistSunInAU * ( math.cos(math.radians(self._fEccentricAnoInDeg)) - self._fEccentricInDeg )
        fyv = self._fMeanDistSunInAU * ( math.sqrt( 1.0 - self._fEccentricInDeg * self._fEccentricInDeg ) * math.sin(math.radians(self._fEccentricAnoInDeg)) )
        self._fTrueAnoInDeg = math.degrees(math.atan2( fyv, fxv )) #planet true anomaly
        self._fSunDistInUA = math.sqrt( fxv*fxv + fyv * fyv ) #planet distance (UA)
        # geocentric position in the ecliptic coordinate system
        fxh = self._fSunDistInUA * ( math.cos(math.radians(self._fLongAscNodeInDeg)) * math.cos(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) - math.sin(math.radians(self._fLongAscNodeInDeg)) * math.sin(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) * math.cos(math.radians(self._fInclEclipInDeg)) )
        fyh = self._fSunDistInUA * ( math.sin(math.radians(self._fLongAscNodeInDeg)) * math.cos(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) + math.cos(math.radians(self._fLongAscNodeInDeg)) * math.sin(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) * math.cos(math.radians(self._fInclEclipInDeg)) )
        fzh = self._fSunDistInUA * ( math.sin(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) * math.sin(math.radians(self._fInclEclipInDeg)) )
        # ecliptic longitude and latitude 
        self._fLongitudeEcliptic = math.degrees(math.atan2(fyh , fxh))
        self._fLatitudeEcliptic = math.degrees(math.atan2(fzh , math.sqrt(fxh * fxh + fyh * fyh )))
        # Perturbation of the moon
        fLS = fSunMeanAnoInDeg + fSunArgPerihelInDeg                      # Mean Longitude of the Sun (Ns=0)
        fLm = self._fMeanAnoInDeg + self._fArgPerihelInDeg + self._fArgPerihelInDeg  # Mean longitude of the Moon
        fD = fLm - fLS                                             # Mean elongation of the Moon
        fF = fLm - self._fLongAscNodeInDeg                                 # Argument of latitude for the Moon
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 1.274 * math.sin(math.radians(self._fMeanAnoInDeg - 2.0 * fD))                    # (the Evection)
        self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.658 * math.sin(math.radians(2.0 * fD))                                      # (the Variation)
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.186 * math.sin(math.radians(fSunMeanAnoInDeg))                              # (the Yearly Equation)
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.059 * math.sin(math.radians(2.0 * self._fMeanAnoInDeg - 2.0 * fD))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.057 * math.sin(math.radians(self._fMeanAnoInDeg - 2.0 * fD + fSunMeanAnoInDeg))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.053 * math.sin(math.radians(self._fMeanAnoInDeg + 2.0 * fD))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.046 * math.sin(math.radians(2.0 * fD - fSunMeanAnoInDeg))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.041 * math.sin(math.radians(self._fMeanAnoInDeg - fSunMeanAnoInDeg))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.035 * math.sin(math.radians(fD))                                        # (the Parallactic Equation)
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.031 * math.sin(math.radians(self._fMeanAnoInDeg + fSunMeanAnoInDeg))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.015 * math.sin(math.radians(2.0 * fF - 2.0 * fD))
        self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.011 * math.sin(math.radians(self._fMeanAnoInDeg - 4.0 * fD))
        self._fLatitudeEcliptic = self._fLatitudeEcliptic -0.173 * math.sin(math.radians(fF - 2.0 * fD))
        self._fLatitudeEcliptic = self._fLatitudeEcliptic -0.055 * math.sin(math.radians(self._fMeanAnoInDeg - fF - 2.0 * fD))
        self._fLatitudeEcliptic = self._fLatitudeEcliptic -0.046 * math.sin(math.radians(self._fMeanAnoInDeg + fF - 2.0 * fD))
        self._fLatitudeEcliptic = self._fLatitudeEcliptic +0.033 * math.sin(math.radians(fF + 2.0 * fD))
        self._fLatitudeEcliptic = self._fLatitudeEcliptic +0.017 * math.sin(math.radians(2.0 * self._fMeanAnoInDeg + fF))
        self._fSunDistInUA = self._fSunDistInUA - 0.58 *  math.cos(math.radians( self._fMeanAnoInDeg -  2.0 * fD))
        self._fSunDistInUA = self._fSunDistInUA - 0.46 *  math.cos(math.radians( 2.0 * fD))
        # Geocentric coordinates
        fxh = self._fSunDistInUA * ( math.cos(math.radians(self._fLongitudeEcliptic)) * math.cos(math.radians(self._fLatitudeEcliptic)))
        fyh = self._fSunDistInUA * ( math.sin(math.radians(self._fLongitudeEcliptic)) * math.cos(math.radians(self._fLatitudeEcliptic)))
        fzh = self._fSunDistInUA * math.sin(math.radians(self._fLatitudeEcliptic))
        self._fGeocentricCoordX = fxh
        self._fGeocentricCoordY = fyh
        self._fGeocentricCoordZ = fzh
        # Equatorial coordinates
        fxe = self._fGeocentricCoordX
        fye = self._fGeocentricCoordY * math.cos(math.radians(self._fObliqEclipInDeg)) - self._fGeocentricCoordZ * math.sin(math.radians(self._fObliqEclipInDeg))
        fze = self._fGeocentricCoordY * math.sin(math.radians(self._fObliqEclipInDeg)) + self._fGeocentricCoordZ * math.cos(math.radians(self._fObliqEclipInDeg))
        self._fRAInDeg = math.degrees(math.atan2( fye, fxe ))
        self._fDecInDeg = math.degrees(math.atan2( fze, math.sqrt(fxe*fxe+fye*fye) ))
        # Compute topocentric position
#        fmpar = math.degrees(math.asin( 1.0 / self._fSunDistInUA))
#        fGclat = self._fLatitude - 0.1924 * math.sin(math.radians(2.0 * self._fLatitude))
#        fRho = 0.99833 + 0.00167 * math.cos(math.radians(2.0 * self._fLatitude))
#        fHA = self._LocalSideralTimeInHour - self._fRAInDeg
#        fg = math.degrees(math.atan(math.tan(math.radians(fGclat)) / math.cos(math.radians(fHA))))
#        self._fTopoRAInDeg = self._fRAInDeg - fmpar * fRho * math.cos(math.radians(fGclat)) * math.sin(math.radians(fHA)) / math.cos(math.radians(self._fDecInDeg))
#        if self._fDecInDeg == 90.0:
#            self._fTopoDecInDeg = self._fDecInDeg - fmpar * fRho * math.sin(math.radians(- self._fDecInDeg)) * math.cos(math.radians(fHA))
#        else:
#            self._fTopoDecInDeg = self._fDecInDeg - fmpar * fRho * math.sin(math.radians(fGclat)) * math.sin(math.radians(fg - self._fDecInDeg)) / math.sin(math.radians(fg))

    def getLongPerihelion(self):     return self._fLongPerihelion
    def getLongAscNodeInDeg(self):   return self._fLongAscNodeInDeg
    def getArgPerihelInDeg(self):    return self._fArgPerihelInDeg
    def getMeanLongInDeg(self):      return self._fMeanLongInDeg
    def getMeanAnoInDeg(self):       return self._fMeanAnoInDeg
    def getPerihelionDistInUA(self): return self._fPerihelionDistInUA
    def getMeanDistSunInAU(self):    return self._fMeanDistSunInAU
    def getEccentricInDeg(self):     return self._fEccentricInDeg
    def getAphelionDistInUA(self):   return self._fAphelionDistInUA
    def getOrbPeriodInYears(self):   return self._fOrbPeriodInYears
    def getEccentricAnoInDeg(self):  return self._fEccentricAnoInDeg
    def getTrueAnoInDeg(self):       return self._fTrueAnoInDeg
    def getSunDistInUA(self):        return self._fSunDistInUA
    def getLongitudeEcliptic(self):  return self._fLongitudeEcliptic
    def getLatitudeEcliptic(self):   return self._fLatitudeEcliptic
    def getGeocentricCoordX(self):   return self._fGeocentricCoordX
    def getGeocentricCoordY(self):   return self._fGeocentricCoordY
    def getGeocentricCoordZ(self):   return self._fGeocentricCoordZ
    def getRAInDeg(self):            return self._fRAInDeg
    def getDecInDeg(self):           return self._fDecInDeg
    def getTopoRAInDeg(self):        return self._fTopoRAInDeg
    def getTopoDecInDeg(self):       return self._fTopoDecInDeg

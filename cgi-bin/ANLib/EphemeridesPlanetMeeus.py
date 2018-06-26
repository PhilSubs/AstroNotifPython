#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class EphemeridesPlanet
# 
import math
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes
#from toolTrace import toolTrace

class EphemeridesPlanet(toolObjectSerializable):
    def __init__(self, sPlanetName):
        toolObjectSerializable.__init__(self)
        self._sName = sPlanetName
        self._sType = "planet"
        
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
    def computeEphemerides(self, fDateValue, fSunMeanAnoInDeg, fSunArgPerihelInDeg, fSunDistInUA, fMeanAnoJupiterInDeg, fMeanAnoSaturnInDeg):
        self._fObliqEclipInDeg = CommonAstroFormulaes.getObliqEclipInDegForDateValue(fDateValue)
        # Orbital elements
        self._fLongAscNodeInDeg = self.getLongAscNodeInDeg(fDateValue)
        self._fInclEclipInDeg = self.getInclEclipInDeg(fDateValue)
        self._fArgPerihelInDeg = self.getArgPerihelInDeg(fDateValue)
        self._fMeanDistSunInAU = self.getMeanDistSunInAU(fDateValue)
        self._fEccentricInDeg = self.getEccentricInDeg(fDateValue)
        self._fMeanAnoInDeg = self.getMeanAnoInDeg(fDateValue)
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
        # heliocentric position in the ecliptic coordinate system
        fxh = self._fSunDistInUA * ( math.cos(math.radians(self._fLongAscNodeInDeg)) * math.cos(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) - math.sin(math.radians(self._fLongAscNodeInDeg)) * math.sin(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) * math.cos(math.radians(self._fInclEclipInDeg)) )
        fyh = self._fSunDistInUA * ( math.sin(math.radians(self._fLongAscNodeInDeg)) * math.cos(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) + math.cos(math.radians(self._fLongAscNodeInDeg)) * math.sin(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) * math.cos(math.radians(self._fInclEclipInDeg)) )
        fzh = self._fSunDistInUA * ( math.sin(math.radians(self._fTrueAnoInDeg + self._fArgPerihelInDeg)) * math.sin(math.radians(self._fInclEclipInDeg)) )    
        # ecliptic longitude and latitude 
        self._fLongitudeEcliptic = math.degrees(math.atan2(fyh , fxh))
        self._fLatitudeEcliptic = math.degrees(math.atan2(fzh , math.sqrt(fxh * fxh + fyh * fyh )))

        # Perturbation of Jupiter, Saturn and Uranus
        if self._sName == "jupiter" and fMeanAnoSaturnInDeg != 0.0:
            self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.332 * math.sin(math.radians(2.0 * self._fMeanAnoInDeg- 5.0 * fMeanAnoSaturnInDeg - 67.6))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.056 * math.sin(math.radians(2.0 * self._fMeanAnoInDeg- 2.0 * fMeanAnoSaturnInDeg + 21.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.042 * math.sin(math.radians(3.0 * self._fMeanAnoInDeg- 5.0 * fMeanAnoSaturnInDeg + 21.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.036 * math.sin(math.radians(self._fMeanAnoInDeg- 2.0 * fMeanAnoSaturnInDeg))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.022 * math.cos(math.radians(self._fMeanAnoInDeg- fMeanAnoSaturnInDeg))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.023 * math.sin(math.radians(2.0 * self._fMeanAnoInDeg- 3.0 * fMeanAnoSaturnInDeg + 52.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.016 * math.sin(math.radians(self._fMeanAnoInDeg- 5.0 * fMeanAnoSaturnInDeg - 69.0))
        elif self._sName == "saturn" and fMeanAnoJupiterInDeg != 0.0:
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.812 * math.sin(math.radians(2.0 * fMeanAnoJupiterInDeg - 5.0 * self._fMeanAnoInDeg - 67.6))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.229 * math.cos(math.radians(2.0 * fMeanAnoJupiterInDeg - 4.0 * self._fMeanAnoInDeg - 2.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.119 * math.sin(math.radians(fMeanAnoJupiterInDeg - 2.0 * self._fMeanAnoInDeg - 3.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.046 * math.sin(math.radians(2.0 * fMeanAnoJupiterInDeg - 6.0 * self._fMeanAnoInDeg - 69.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.014 * math.sin(math.radians(fMeanAnoJupiterInDeg - 3.0 * self._fMeanAnoInDeg + 32.0))
            self._fLatitudeEcliptic = self._fLatitudeEcliptic - 0.020 * math.cos(math.radians(2.0 * fMeanAnoJupiterInDeg - 4.0 * self._fMeanAnoInDeg - 2.0))
            self._fLatitudeEcliptic = self._fLatitudeEcliptic + 0.018 * math.sin(math.radians(2.0 * fMeanAnoJupiterInDeg - 6.0 * self._fMeanAnoInDeg - 49.0))
        elif self._sName == "uranus":
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.040 * math.sin(math.radians(fMeanAnoSaturnInDeg - 2.0 * self._fMeanAnoInDeg + 6.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic + 0.035 * math.sin(math.radians(fMeanAnoSaturnInDeg - 3.0 * self._fMeanAnoInDeg + 33.0))
            self._fLongitudeEcliptic = self._fLongitudeEcliptic - 0.015 * math.sin(math.radians(fMeanAnoJupiterInDeg - self._fMeanAnoInDeg + 20.0))

        fxh = self._fSunDistInUA * ( math.cos(math.radians(self._fLongitudeEcliptic)) * math.cos(math.radians(self._fLatitudeEcliptic)))
        fyh = self._fSunDistInUA * ( math.sin(math.radians(self._fLongitudeEcliptic)) * math.cos(math.radians(self._fLatitudeEcliptic)))
        fzh = self._fSunDistInUA * math.sin(math.radians(self._fLatitudeEcliptic))
        # Sun's true longitude
        fSunTrueLon = fSunMeanAnoInDeg + fSunArgPerihelInDeg
        # Ecliptic Rectangular Geocentric Coordinates
        fxs = fSunDistInUA * math.cos(math.radians(fSunTrueLon))
        fys = fSunDistInUA * math.sin(math.radians(fSunTrueLon))
        fxg = fxh + fxs
        fyg = fyh + fys
        fzg = fzh
        # Equatorial Rectangular Geocentric Coordinates
        fxe = fxg
        fye = fyg * math.cos(math.radians(self._fObliqEclipInDeg)) - fzg * math.sin(math.radians(self._fObliqEclipInDeg))
        fze = fyg * math.sin(math.radians(self._fObliqEclipInDeg)) + fzg * math.cos(math.radians(self._fObliqEclipInDeg))
        # Equatorial Coordinates
        self._fRAInDeg = math.degrees(math.atan2( fye, fxe ))
        self._fDecInDeg = math.degrees(math.atan2( fze, math.sqrt(fxe*fxe+fye*fye) ))
    
    def getLongAscNodeInDeg(self, fDateValue):
        if (self._sName == "Mercury"):
            return 48.3313 + 3.24587 * 10**-5 * fDateValue
        elif (self._sName == "Venus"):
            return  76.6799 + 2.46590 * 10**-5 * fDateValue
        elif (self._sName == "Mars"):
            return  49.5574 + 2.11081 * 10**-5 * fDateValue
        elif (self._sName == "Jupiter"):
            return 100.4542 + 2.76854 * 10**-5 * fDateValue
        elif (self._sName == "Saturn"):
            return 113.6634 + 2.38980 * 10**-5 * fDateValue
        elif (self._sName == "Uranus"):
            return  74.0005 + 1.3978 * 10**-5 * fDateValue
        elif (self._sName == "Neptune"):
            return 131.7806 + 3.0173 * 10**-5 * fDateValue
    def getInclEclipInDeg(self, fDateValue):
        if (self._sName == "Mercury"):
            return 7.0047 + 5.00 * 10**-8 * fDateValue
        elif (self._sName == "Venus"):
            return 3.3946 + 2.75 * 10**-8 * fDateValue
        elif (self._sName == "Mars"):
            return 1.8497 - 1.78 * 10**-8 * fDateValue
        elif (self._sName == "Jupiter"):
            return 1.3030 - 1.557 * 10**-7 * fDateValue
        elif (self._sName == "Saturn"):
            return 2.4886 - 1.081 * 10**-7 * fDateValue
        elif (self._sName == "Uranus"):
            return 0.7733 + 1.9 * 10**-8 * fDateValue
        elif (self._sName == "Neptune"):
            return 1.7700 - 2.55 * 10**-7 * fDateValue
    def getArgPerihelInDeg(self, fDateValue):
        if (self._sName == "Mercury"):
            return 29.1241 + 1.01444 * 10**-5 * fDateValue
        elif (self._sName == "Venus"):
            return  54.8910 + 1.38374 * 10**-5 * fDateValue
        elif (self._sName == "Mars"):
            return 286.5016 + 2.92961 * 10**-5 * fDateValue
        elif (self._sName == "Jupiter"):
            return 273.8777 + 1.64505 * 10**-5 * fDateValue
        elif (self._sName == "Saturn"):
            return 339.3939 + 2.97661 * 10**-5 * fDateValue
        elif (self._sName == "Uranus"):
            return  96.6612 + 3.0565 * 10**-5 * fDateValue
        elif (self._sName == "Neptune"):
            return 272.8461 - 6.027 * 10**-6 * fDateValue
    def getMeanDistSunInAU(self, fDateValue):
        if (self._sName == "Mercury"):
            return 0.387098  
        elif (self._sName == "Venus"):
            return 0.723330  
        elif (self._sName == "Mars"):
            return 1.523688
        elif (self._sName == "Jupiter"):
            return 5.20256
        elif (self._sName == "Saturn"):
            return 9.55475
        elif (self._sName == "Uranus"):
            return 19.18171 - 1.55 * 10**-8 * fDateValue
        elif (self._sName == "Neptune"):
            return 30.05826 + 3.313 * 10**-8 * fDateValue
    def getEccentricInDeg(self, fDateValue):
        if (self._sName == "Mercury"):
            return 0.205635 + 5.59 * 10**-10 * fDateValue
        elif (self._sName == "Venus"):
            return 0.006773 - 1.302 * 10**-9 * fDateValue
        elif (self._sName == "Mars"):
            return 0.093405 + 2.516 * 10**-9 * fDateValue
        elif (self._sName == "Jupiter"):
            return 0.048498 + 4.469 * 10**-9 * fDateValue
        elif (self._sName == "Saturn"):
            return 0.055546 - 9.499 * 10**-9 * fDateValue
        elif (self._sName == "Uranus"):
            return 0.047318 + 7.45 * 10**-9 * fDateValue
        elif (self._sName == "Neptune"):
            return 0.008606 + 2.15 * 10**-9 * fDateValue
    def getMeanAnoInDeg(self, fDateValue):
        if (self._sName == "Mercury"):
            return 168.6562 + 4.0923344368 * fDateValue
        elif (self._sName == "Venus"):
            return  48.0052 + 1.6021302244 * fDateValue
        elif (self._sName == "Mars"):
            return  18.6021 + 0.5240207766 * fDateValue
        elif (self._sName == "Jupiter"):
            return  19.8950 + 0.0830853001 * fDateValue
        elif (self._sName == "Saturn"):
            return 316.9670 + 0.0334442282 * fDateValue
        elif (self._sName == "Uranus"):
            return 142.5905 + 0.011725806 * fDateValue
        elif (self._sName == "Neptune"):
            return 260.2471 + 0.005995147 * fDateValue
        
    def getAphelionDistInUA(self):   return self._fAphelionDistInUA
    def getEccentricAnoInDeg(self):  return self._fEccentricAnoInDeg
    def getLongPerihelion(self):     return self._fLongPerihelion
    def getLatitudeEcliptic(self):   return self._fLatitudeEcliptic
    def getLongitudeEcliptic(self):  return self._fLongitudeEcliptic
    def getMeanLongInDeg(self):      return self._fMeanLongInDeg
    def getOrbPeriodInYears(self):   return self._fOrbPeriodInYears
    def getPerihelionDistInUA(self): return self._fPerihelionDistInUA
    def getSunDistInUA(self):        return self._fSunDistInUA
    def getTrueAnoInDeg(self):       return self._fTrueAnoInDeg
    def getGeocentricCoordX(self):   return self._fGeocentricCoordX
    def getGeocentricCoordY(self):   return self._fGeocentricCoordY
    def getGeocentricCoordZ(self):   return self._fGeocentricCoordZ
    def getRAInDeg(self):            return self._fRAInDeg
    def getDecInDeg(self):           return self._fDecInDeg
    def getTopoRAInDeg(self):        return self._fTopoRAInDeg
    def getTopoDecInDeg(self):       return self._fTopoDecInDeg

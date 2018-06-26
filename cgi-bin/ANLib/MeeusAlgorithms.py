#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class MeeusAlgorithms
# 
from toolObjectSerializable import toolObjectSerializable
import math
from MeeusTable45A import MeeusTable45A
from MeeusTable45B import MeeusTable45B
from MeeusAlgorithmsFormulas import MeeusAlgorithmsFormulas

#from toolTrace import toolTrace


class MeeusAlgorithms(toolObjectSerializable):
    # Class Methods
    @staticmethod
    def getSunAltitudeFromMoonFeature(fFeatureLongitudeOnTheMoon, fFeatureLatitudeOnTheMoon, fMoonSelenographicLongitude, fMoonSelenographicLatitude):
        fSunToFeatureAltitude = math.degrees(math.acos(math.sin(math.radians(fMoonSelenographicLatitude)) * math.sin(math.radians(fFeatureLatitudeOnTheMoon)) + math.cos(math.radians(fMoonSelenographicLatitude)) * math.cos(math.radians(fFeatureLatitudeOnTheMoon)) * math.cos(math.radians(fFeatureLongitudeOnTheMoon - fMoonSelenographicLongitude))))
        return (90.0 - fSunToFeatureAltitude)
    @staticmethod
    def getSunAzimutFromMoonFeature(fFeatureLongitudeOnTheMoon, fFeatureLatitudeOnTheMoon, fMoonSelenographicLongitude, fMoonSelenographicLatitude):
        fSunToFeatureAzimut = math.degrees(math.atan2( math.cos(math.radians(fMoonSelenographicLatitude)) * math.sin(math.radians(fMoonSelenographicLongitude - fFeatureLongitudeOnTheMoon)), math.cos(math.radians(fFeatureLatitudeOnTheMoon)) * math.sin(math.radians(fMoonSelenographicLatitude)) - math.sin(math.radians(fFeatureLatitudeOnTheMoon)) * math.cos(math.radians(fMoonSelenographicLatitude)) * math.cos(math.radians(fMoonSelenographicLongitude - fFeatureLongitudeOnTheMoon))))
        return ((fSunToFeatureAzimut + 360.0) % 360.0)

    # Constructor
    def __init__(self, sDate, sTime):
        toolObjectSerializable.__init__(self)
        self._date = sDate # date as YYYYMMDD
        self._time = sTime # Time as HHMMSS (GMT)
        self._iYear = int(sDate[0:4])
        self._iMonth = int(sDate[4:6])
        self._iDay = int(sDate[6:8])
        self._iHour = int(sTime[0:2])
        self._iMinute = int(sTime[2:4])
        self._iSecond = int(sTime[4:6])

        self._fJuliandDay = 0.0
        self._fJuliandEphemerisDay = 0.0
        self._fJulianCenturies = 0.0
        self._fJulianEphemerisCenturies = 0
        self._fDeltaT = 0.0
        self._fMeanSideralTimeGreenwich = 0.0
        self._fApparentSideralTimeGreenwich = 0.0
        
        self._fApparentGeometricLongitude = {} 
        self._fArgumentOfLatitude = {} 
        self._fApparentGeocentricLongitude = {} 
        self._fApparentGeocentricLatitude = {} 
        self._fDeclination = {} 
        self._fDistanceInKm = {}
        self._fDistanceInUA = {}
        self._fEquationCenter = {} 
        self._fEccentricity = {} 
        self._fGeocentricLatitude = {} 
        self._fGeocentricLongitude = {} 
        self._fGeometricMeanLongitude = {} 
        self._fIllumination = {} 
        self._fAscendNodeLongitude = {} 
        self._fMeanAscendingNodeLongitude = {} 
        self._fMeanAnomaly = {} 
        self._fMeanElongation = {} 
        self._fMeanLongitude = {} 
        self._fMeanObliquityEcliptic = {}
        self._fNutationInLongitude = {}
        self._fOpticalLibrationInLongitude = {}
        self._fOpticalLibrationInLatitude = {}
        self._fPhaseAngle = {} 
        self._fRightAscension = {}
        self._fSelenographicColongitude = {}
        self._fSubSolarSelenographicLongitude = {} 
        self._fSubSolarSelenographicLatitude = {} 
        self._fTrueAnomaly = {} 
        self._fTrueGeometricLongitude = {} 
        

        self._compute()

    # Getters & Setters
    def getJulianDay(self): return self._fJuliandDay
    def getJulianEphemerisDay(self): return self._fJuliandEphemerisDay
    def getJulianCenturies(self): return self._fJulianCenturies
    def getJulianEphemerisCenturies(self): return self._fJulianEphemerisCenturies
    def getDeltaT(self): return self._fDeltaT
    def getMeanSideralTimeGreenwich(self): return self._fMeanSideralTimeGreenwich
    def getApparentSideralTimeGreenwich(self): return self._fApparentSideralTimeGreenwich
    
    def getApparentGeometricLongitude(self, sObjectID): return self._fApparentGeometricLongitude[sObjectID]
    def getArgumentOfLatitude(self, sObjectID): return self._fArgumentOfLatitude[sObjectID]
    def getAzimut(self, sObjectID, fObserverLongitude, fObserverLatitude): return MeeusAlgorithmsFormulas.TransformationCoordinates_12_05(self._fRightAscension[sObjectID], self._fDeclination[sObjectID], fObserverLongitude, fObserverLatitude, self._fMeanSideralTimeGreenwich)
    def getDeclination(self, sObjectID): return self._fDeclination[sObjectID]
    def getDistanceInKm(self, sObjectID): return self._fDistanceInKm[sObjectID]
    def getDistanceInUA(self, sObjectID): return self._fDistanceInUA[sObjectID]
    def getEccentricity(self, sObjectID): return self._fEccentricity[sObjectID]
    def getElevation(self, sObjectID, fObserverLongitude, fObserverLatitude): return MeeusAlgorithmsFormulas.TransformationCoordinates_12_06(self._fRightAscension[sObjectID], self._fDeclination[sObjectID], fObserverLongitude, fObserverLatitude, self._fMeanSideralTimeGreenwich)
    def getEquationCenter(self, sObjectID): return self._fEquationCenter[sObjectID]
    def getGeocentricLatitude(self, sObjectID): return self._fGeocentricLatitude[sObjectID]
    def getGeocentricLongitude(self, sObjectID): return self._fGeocentricLongitude[sObjectID]
    def getGeometricMeanLongitude(self, sObjectID): return self._fGeometricMeanLongitude[sObjectID]
    def getIllumination(self, sObjectID): return self._fIllumination[sObjectID]
    def getLongitudeAscendNode(self, sObjectID): return self._fAscendNodeLongitude[sObjectID]
    def getMeanAscendingNodeLongitude(self, sObjectID): return self._fMeanAscendingNodeLongitude[sObjectID]
    def getMeanAnomaly(self, sObjectID): return self._fMeanAnomaly[sObjectID]
    def getMeanElongation(self, sObjectID): return self._fMeanElongation[sObjectID]
    def getMeanLongitude(self, sObjectID): return self._fMeanLongitude[sObjectID]
    def getMeanObliquityEcliptic(self, sObjectID): return self._fMeanObliquityEcliptic[sObjectID]
    def getNutationInLongitude(self, sObjectID): return self._fNutationInLongitude[sObjectID]
    def getPhaseAngle(self, sObjectID): return self._fPhaseAngle[sObjectID]
    def getRightAscension(self, sObjectID): return self._fRightAscension[sObjectID]
    def getSelenographicColongitude(self, sObjectID): return self._fSelenographicColongitude[sObjectID]
    def getSubSolarSelenographicLatitude(self, sObjectID): return self._fSubSolarSelenographicLatitude[sObjectID]
    def getSubSolarSelenographicLongitude(self, sObjectID): return self._fSubSolarSelenographicLongitude[sObjectID]
    def getTrueAnomaly(self, sObjectID): return self._fTrueAnomaly[sObjectID]
    def getTrueGeometricLongitude(self, sObjectID): return self._fTrueGeometricLongitude[sObjectID]

#    def getMoonHeliocentricEclipticLatitude(self): return self._fMoonHeliocentricEclipticLatitude
#    def getMoonHeliocentricEclipticLongitude(self): return self._fMoonHeliocentricEclipticLongitude

    # Internal methods
    def _compute(self):
        # Date
        self._fJuliandDay = MeeusAlgorithmsFormulas.JulianDay_07_01(self._iYear, self._iMonth, self._iDay, self._iHour, self._iMinute, self._iSecond)
        self._fJuliandEphemerisDay, self._fJulianCenturies, self._fJulianEphemerisCenturies = MeeusAlgorithmsFormulas.NutationObliquity_21_00(self._fJuliandDay)
        # Earth
        self._fMeanObliquityEcliptic['Earth'] = MeeusAlgorithmsFormulas.NutationObliquity_21_02(self._fJulianCenturies)
        self._fEccentricity['Earth'] = MeeusAlgorithmsFormulas.SunCoordinates_24_04(self._fJulianCenturies)
        # Time
        self._fDeltaT = MeeusAlgorithmsFormulas.DynamicalTime_09_01(self._fJuliandDay) 
        self._fGeometricMeanLongitude['Sun'] = MeeusAlgorithmsFormulas.SunCoordinates_24_02(self._fJulianCenturies)
        self._fMeanLongitude['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_01(self._fJulianCenturies)
        self._fAscendNodeLongitude['Moon'], self._fNutationInLongitude['Earth'] = MeeusAlgorithmsFormulas.NutationObliquity_21_01(self._fJulianCenturies, self._fGeometricMeanLongitude['Sun'], self._fMeanLongitude['Moon'])
        self._fMeanSideralTimeGreenwich, self._fApparentSideralTimeGreenwich = MeeusAlgorithmsFormulas.SideralTimeGreenwich_11_01(self._fJuliandDay, self._fJulianCenturies, self._fNutationInLongitude['Earth'], self._fMeanObliquityEcliptic['Earth'])
        # Sun
        self._fMeanAnomaly['Sun'] = MeeusAlgorithmsFormulas.PositionMoon_45_03(self._fJulianCenturies)
        self._fEquationCenter['Sun'], self._fTrueGeometricLongitude['Sun'], self._fTrueAnomaly['Sun'], self._fDistanceInUA['Sun'], self._fDistanceInKm['Sun'], self._fApparentGeometricLongitude['Sun'] = MeeusAlgorithmsFormulas.SunCoordinates_24_05(self._fJulianCenturies, self._fMeanAnomaly['Sun'], self._fGeometricMeanLongitude['Sun'], self._fEccentricity['Earth'])
        self._fRightAscension['Sun'] = MeeusAlgorithmsFormulas.SunCoordinates_24_06(self._fTrueGeometricLongitude['Sun'], self._fMeanObliquityEcliptic['Earth'], self._fJulianCenturies)
        self._fDeclination['Sun'] = MeeusAlgorithmsFormulas.SunCoordinates_24_07(self._fTrueGeometricLongitude['Sun'], self._fMeanObliquityEcliptic['Earth'], self._fJulianCenturies)
        self._fApparentGeocentricLongitude['Sun'], self._fApparentGeocentricLatitude['Sun'] = MeeusAlgorithmsFormulas.SunCoordinates_24_09(self._fGeometricMeanLongitude['Sun'], 0.0)
        # Moon
        self._fMeanElongation['Moon'] =  MeeusAlgorithmsFormulas.PositionMoon_45_02(self._fJulianCenturies)
        self._fMeanAnomaly['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_04(self._fJulianCenturies)
        self._fMeanAscendingNodeLongitude['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_07(self._fJulianCenturies)
        self._fArgumentOfLatitude['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_05(self._fJulianCenturies)
        self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'], self._fDistanceInKm['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_06(self._fJulianCenturies, self._fMeanElongation['Moon'], self._fMeanAnomaly['Sun'], self._fMeanAnomaly['Moon'], self._fArgumentOfLatitude['Moon'], self._fMeanLongitude['Moon'])
        self._fPhaseAngle['Moon'] = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_04(self._fMeanElongation['Moon'], self._fMeanAnomaly['Moon'], self._fMeanAnomaly['Sun'])
        self._fIllumination['Moon'] = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_01(self._fPhaseAngle['Moon'])
        self._fRightAscension['Moon'] = MeeusAlgorithmsFormulas.TransformationCoordinates_12_03(self._fMeanObliquityEcliptic['Earth'], self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'])
        self._fDeclination['Moon'] = MeeusAlgorithmsFormulas.TransformationCoordinates_12_04(self._fMeanObliquityEcliptic['Earth'], self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'])
        self._fOpticalLibrationInLongitude['Moon'], self._fOpticalLibrationInLatitude['Moon'], self._fSubSolarSelenographicLongitude['Moon'], self._fSubSolarSelenographicLatitude['Moon'], self._fSelenographicColongitude['Moon'] = MeeusAlgorithmsFormulas.PhysicalEphemerisMoon_51(self._fJulianCenturies, self._fApparentGeocentricLongitude['Sun'], self._fDistanceInKm['Moon'], self._fDistanceInKm['Sun'], self._fMeanAnomaly['Moon'], self._fMeanAnomaly['Sun'], self._fMeanElongation['Moon'], self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'], self._fNutationInLongitude['Earth'], self._fMeanAscendingNodeLongitude['Moon'], self._fArgumentOfLatitude['Moon'])
       
        # Planets

        # chapter 51, page 342

        #self._fMoonMeanAscendingNodeLongitude = 125.044555 - 1934.1361849 * self._fJulianCenturies + 0.0020762 * self._fJulianCenturies**2 + self._fJulianCenturies**3 / 467410.0 - self._fJulianCenturies**4 / 60616000.0
        #self._fMoonHeliocentricEclipticLongitude = self._fSunApparentGeometricLongitude + 180.0 + self._fMoonDistanceInKm / self._fSunDistanceInKm * 57.296 * math.cos(self._fMoonGeocentricLatitude / 360.0 * 2.0 * math.pi) * math.sin((self._fSunApparentGeometricLongitude - self._fMoonGeocentricLongitude) / 360.0 * 2.0 * math.pi)
        #self._fMoonHeliocentricEclipticLatitude = self._fMoonDistanceInKm / self._fSunDistanceInKm * self._fMoonGeocentricLatitude
        #fW = self._fMoonHeliocentricEclipticLongitude - self._fEarthNutationInLongitude - self._fMoonMeanAscendingNodeLongitude
        #if fW < 0: fW = fW + 360.0
        #fARad = math.atan(((math.sin(fW / 360.0 * 2.0 * math.pi) * math.cos(self._fMoonHeliocentricEclipticLatitude / 360.0 * 2.0 * math.pi) * math.cos(1.54242 / 360.0 * 2.0 * math.pi)) - (math.sin(self._fMoonHeliocentricEclipticLatitude / 360.0 * 2.0 * math.pi) * math.sin(1.54242 / 360.0 * 2.0 * math.pi))) / (math.cos(fW / 360.0 * 2.0 * math.pi) * math.cos(self._fMoonHeliocentricEclipticLatitude / 360.0 * 2.0 * math.pi)))
        #if fARad < 0: fARad = fARad + 2.0 * math.pi
        #fA = fARad / math.pi * 180.0
        #fLambdaPrimeO = fA - self._fMoonArgumentOfLatitude
        #fBetaPrimeORad = math.asin(-1.0 * math.sin(fW / 360.0 * 2.0 * math.pi) * math.cos(self._fMoonHeliocentricEclipticLatitude / 360.0 * 2.0 * math.pi) * math.sin(1.54242 / 360.0 * 2.0 * math.pi) - math.sin(self._fMoonHeliocentricEclipticLatitude / 360.0 * 2.0 * math.pi) * math.cos(1.54242 / 360.0 * 2.0 * math.pi))
        #if fBetaPrimeORad < 0: fBetaPrimeORad = fBetaPrimeORad + 2.0 * math.pi
        #fBetaPrimeO = fBetaPrimeORad / math.pi * 180.0
        #fRadMoonMeanAnomaly = math.radians(self._fMoonMeanAnomaly)
        #fRadMoonArgumentOfLatitude = math.radians(self._fMoonArgumentOfLatitude)
        #fRadMoonMeanElongation = math.radians(self._fMoonMeanElongation)
        #fRadMoonMeanAnomalyX2 = 2.0 * fRadMoonMeanAnomaly
        #fRadMoonArgumentOfLatitudeX2 = 2.0 * fRadMoonArgumentOfLatitude
        #fRadMoonMeanElongationX2 = 2.0 * fRadMoonMeanElongation
        #fRadMoonArgumentOfLatitudeX3 = 3.0 * fRadMoonArgumentOfLatitude
        #fRadK1 = math.radians(119.75 + 131.849 * self._fJulianCenturies)
        #fRadK2 = math.radians(72.56 + 20.186 * self._fJulianCenturies)
        #fRadMoonMeanAscendingNodeLongitude = math.radians(self._fMoonMeanAscendingNodeLongitude)
        #fRadSunMeanAnomaly = math.radians(self._fSunMeanAnomaly)
        #fRadSunMeanAnomalyX2 = fRadSunMeanAnomaly * 2.0
        #fT_p = -0.02752 * math.cos(fRadMoonMeanAnomaly) - 0.02245 * math.sin(fRadMoonArgumentOfLatitude) + 0.00684 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX2) - 0.00293 * math.cos(fRadMoonArgumentOfLatitudeX2) - 0.00085 * math.cos(fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) - 0.00054 * math.cos(fRadMoonMeanAnomaly - fRadMoonMeanElongationX2) - 0.0002 * math.sin(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitude) - 0.0002 * math.cos(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2) - 0.0002 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) + 0.00014  * math.cos(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2)
        #fT_o = -0.02816 * math.sin(fRadMoonMeanAnomaly) + 0.02244 * math.cos(fRadMoonArgumentOfLatitude) - 0.00682 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX2) - 0.00279 * math.sin(fRadMoonArgumentOfLatitudeX2) - 0.00083 * math.sin(fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) + 0.00069 * math.sin(fRadMoonMeanAnomaly - fRadMoonMeanElongationX2) + 0.0004 * math.cos(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitude) - 0.00025 * math.sin(fRadMoonMeanAnomalyX2) - 0.00023 * math.sin(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2) + 0.0002 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) + 0.00019 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) + 0.00013 * math.sin(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) - 0.0001 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX3)
        #fT_t = 0.0252 * self._fE * math.sin(fRadSunMeanAnomaly) + 0.00473 * math.sin(fRadMoonMeanAnomalyX2 - fRadMoonArgumentOfLatitudeX2) - 0.00467 * math.sin(fRadMoonMeanAnomaly) + 0.00396 * math.sin(fRadK1) + 0.00276 * math.sin(fRadMoonMeanAnomalyX2 - fRadMoonMeanElongationX2) + 0.00196 * math.sin(fRadMoonMeanAscendingNodeLongitude) - 0.00183 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) + 0.00115 * math.sin(fRadMoonMeanAnomaly - fRadMoonMeanElongationX2) - 0.00096 * math.sin(fRadMoonMeanAnomaly - fRadMoonMeanElongation) + 0.00046 * math.sin(fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) - 0.00039 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) - 0.00032 * math.sin(fRadMoonMeanAnomaly - fRadSunMeanAnomaly - fRadMoonMeanElongation) + 0.00027 * math.sin(fRadMoonMeanAnomalyX2 - fRadSunMeanAnomaly - fRadMoonMeanElongationX2) + 0.00023 * math.sin(fRadK2) - 0.00014 * math.sin(fRadMoonMeanElongationX2) + 0.00014 * math.cos(fRadMoonMeanAnomalyX2 - fRadMoonArgumentOfLatitudeX2) - 0.00012 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX2) - 0.00012 * math.sin(fRadMoonMeanAnomalyX2) + 0.00011 * math.sin(fRadMoonMeanAnomalyX2 - fRadSunMeanAnomalyX2 - fRadMoonMeanElongationX2)
        #fLambdaSecondO = -fT_t + (fT_p * math.cos(math.radians(fA)) + fT_o * math.sin(math.radians(fA))) * math.tan(fBetaPrimeORad)
        #fBetaSecondO = fT_o * math.cos(fARad) - fT_p * math.sin(fARad)
        #self._fMoonSelenographicLongitude = (fLambdaSecondO + fLambdaPrimeO) - int((fLambdaSecondO + fLambdaPrimeO) / 360.0) * 360.0
        #self._fMoonSelenographicLatitude = (fBetaPrimeO + fBetaSecondO) - int((fBetaPrimeO + fBetaSecondO) / 360.0) * 360.0
        
        #self._fMoonSelenographicColongitude = (self._fMoonSelenographicLongitude - 90.0 + 360.0) % 360.0 #(450.0 - self._fMoonSelenographicLongitude) - int((450.0 - self._fMoonSelenographicLongitude) / 360.0) * 360.0
        #if self._fMoonSelenographicColongitude > 180.0: self._fMoonSelenographicColongitude = self._fMoonSelenographicColongitude - 360.0
        
        # Geocentric coordinates
        #fxh = self._fMoonDistanceInKm * ( math.cos(math.radians(self._fMoonGeocentricLongitude)) * math.cos(math.radians(self._fMoonGeocentricLatitude)))
        #fyh = self._fMoonDistanceInKm * ( math.sin(math.radians(self._fMoonGeocentricLongitude)) * math.cos(math.radians(self._fMoonGeocentricLatitude)))
        #fzh = self._fMoonDistanceInKm * math.sin(math.radians(self._fMoonGeocentricLatitude))
        #self._fMoonGeocentricCoordX = fxh
        #self._fMoonGeocentricCoordY = fyh
        #self._fMoonGeocentricCoordZ = fzh
        # Equatorial coordinates
        #self._fObliqEclipInDeg = 23.0 + 26.0/60.0 + 21.448/3600.0 - 46.0/3600.0 * self._fJulianCenturies - 0.00059/3600.0 * self._fJulianCenturies**2 + 0.001813/3600.0 * self._fJulianCenturies**3
        #fxe = self._fMoonGeocentricCoordX
        #fye = self._fMoonGeocentricCoordY * math.cos(math.radians(self._fObliqEclipInDeg)) - self._fMoonGeocentricCoordZ * math.sin(math.radians(self._fObliqEclipInDeg))
        #fze = self._fMoonGeocentricCoordY * math.sin(math.radians(self._fObliqEclipInDeg)) + self._fMoonGeocentricCoordZ * math.cos(math.radians(self._fObliqEclipInDeg))
        #self._fMoonRAInDeg = math.degrees(math.atan2( fye, fxe ))
        #self._fMoonDecInDeg = math.degrees(math.atan2( fze, math.sqrt(fxe*fxe+fye*fye) ))
        #if self._fMoonDecInDeg > 180: self._fMoonDecInDeg = self._fMoonDecInDeg - 360
        #if self._fMoonDecInDeg < -180: self._fMoonDecInDeg = self._fMoonDecInDeg + 360
       

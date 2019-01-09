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
        # Co: Colongitude of the Sun0
        # Bo: Subsolar point Lat
        #     Now you are ready to calculate the angle of the Sun above your mountain. Do it in two steps:
        #       Step 1:
        #           x  =  sin(Bo)*sin(latitude)  +  cos(Bo)*cos(latitude)*sin(Co + longitude)
        #       Step 2:
        #           angle theta  =  arcsin(x)
#        Co = fMoonColongitude
#        Bo = fMoonSelenographicLatitude
#        x= math.sin(math.radians(Bo)) * math.sin(math.radians(fFeatureLatitudeOnTheMoon)) + math.cos(math.radians(Bo)) * math.cos(math.radians(fFeatureLatitudeOnTheMoon)) * math.sin(math.radians(Co + fFeatureLongitudeOnTheMoon))
#        fSunToFeatureAltitude1 = math.degrees(math.asin(x))
        fSunToFeatureAltitude = math.degrees(math.acos(math.sin(math.radians(fMoonSelenographicLatitude)) * math.sin(math.radians(fFeatureLatitudeOnTheMoon)) + math.cos(math.radians(fMoonSelenographicLatitude)) * math.cos(math.radians(fFeatureLatitudeOnTheMoon)) * math.cos(math.radians(fFeatureLongitudeOnTheMoon - fMoonSelenographicLongitude))))
#        print "  ===>  fSunToFeatureAltitude1: " + str(fSunToFeatureAltitude1) + "    fSunToFeatureAltitude: " + str(90.0 - fSunToFeatureAltitude) 
##        return (90.0 - fSunToFeatureAltitude)
        return (fSunToFeatureAltitude - 90.0)
    @staticmethod
    def getSunAzimutFromMoonFeature(fFeatureLongitudeOnTheMoon, fFeatureLatitudeOnTheMoon, fMoonSelenographicLongitude, fMoonSelenographicLatitude):
        fSunToFeatureAzimut = math.degrees(math.atan2( math.cos(math.radians(fMoonSelenographicLatitude)) * math.sin(math.radians(fMoonSelenographicLongitude - fFeatureLongitudeOnTheMoon)), math.cos(math.radians(fFeatureLatitudeOnTheMoon)) * math.sin(math.radians(fMoonSelenographicLatitude)) - math.sin(math.radians(fFeatureLatitudeOnTheMoon)) * math.cos(math.radians(fMoonSelenographicLatitude)) * math.cos(math.radians(fMoonSelenographicLongitude - fFeatureLongitudeOnTheMoon))))
        return ((fSunToFeatureAzimut + 360.0) % 360.0)
    @staticmethod
    def getAngularSeparation(fRightAscensionA, fDeclinationA, fRightAscensionB, fDeclinationB):
        return MeeusAlgorithmsFormulas.AngularSeparation_16_01(fRightAscensionA, fDeclinationA, fRightAscensionB, fDeclinationB)
        
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
        self._fApparentGeocentricLongitude = {} 
        self._fApparentGeocentricLatitude = {} 
        self._fApparentRightAscension = {}
        self._fArgumentOfLatitude = {} 
        self._fAscendNodeLongitude = {} 
        self._fDeclination = {} 
        self._fDistanceInKm = {}
        self._fDistanceInUA = {}
        self._fEquationCenter = {} 
        self._fEccentricity = {} 
        self._fGeocentricLatitude = {} 
        self._fGeocentricLongitude = {} 
        self._fGeometricMeanLongitude = {} 
        self._fIllumination = {} 
        self._fMeanAscendingNodeLongitude = {} 
        self._fMeanAnomaly = {} 
        self._fMeanElongation = {} 
        self._fMeanLongitude = {} 
        self._fMeanObliquityEcliptic = {}
        self._fNutationInLongitude = {}
        self._fOpticalLibrationInLongitude = {}
        self._fOpticalLibrationInLatitude = {}
        self._fPhaseAngle = {} 
        self._fPositionAngle = {}
        self._fRightAscension = {}
        self._fSelenographicColongitude = {}
        self._fSubSolarSelenographicLongitude = {} 
        self._fSubSolarSelenographicLatitude = {} 
        self._fTrueAnomaly = {} 
        self._fTrueGeometricLongitude = {} 
        self._fTrueObliquityEcliptic = {}

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
    def getPositionAngle(self, sObjectID): return self._fPositionAngle[sObjectID]

#    def getMoonHeliocentricEclipticLatitude(self): return self._fMoonHeliocentricEclipticLatitude
#    def getMoonHeliocentricEclipticLongitude(self): return self._fMoonHeliocentricEclipticLongitude

    # Internal methods
    def _compute(self):
        # Date
        self._fJuliandDay = MeeusAlgorithmsFormulas.JulianDay_07_01(self._iYear, self._iMonth, self._iDay, self._iHour, self._iMinute, self._iSecond)
        self._fJuliandEphemerisDay, self._fJulianCenturies, self._fJulianEphemerisCenturies = MeeusAlgorithmsFormulas.NutationObliquity_21_00(self._fJuliandDay)
        # Moon
        self._fMeanAscendingNodeLongitude['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_07(self._fJulianCenturies)
        # Earth
        self._fMeanObliquityEcliptic['Earth'], self._fTrueObliquityEcliptic['Earth'] = MeeusAlgorithmsFormulas.NutationObliquity_21_02(self._fJulianCenturies, self._fMeanAscendingNodeLongitude['Moon'])
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
        self._fArgumentOfLatitude['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_05(self._fJulianCenturies)
        self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'], self._fDistanceInKm['Moon'] = MeeusAlgorithmsFormulas.PositionMoon_45_06(self._fJulianCenturies, self._fMeanElongation['Moon'], self._fMeanAnomaly['Sun'], self._fMeanAnomaly['Moon'], self._fArgumentOfLatitude['Moon'], self._fMeanLongitude['Moon'])
        self._fPhaseAngle['Moon'] = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_04(self._fMeanElongation['Moon'], self._fMeanAnomaly['Moon'], self._fMeanAnomaly['Sun'])
        self._fIllumination['Moon'] = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_01(self._fPhaseAngle['Moon'])
        self._fRightAscension['Moon'] = MeeusAlgorithmsFormulas.TransformationCoordinates_12_03(self._fMeanObliquityEcliptic['Earth'], self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'])
        self._fApparentRightAscension['Moon'] = self._fRightAscension['Moon']   # !!!!!!!!
        self._fDeclination['Moon'] = MeeusAlgorithmsFormulas.TransformationCoordinates_12_04(self._fMeanObliquityEcliptic['Earth'], self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'])
        self._fOpticalLibrationInLongitude['Moon'], self._fOpticalLibrationInLatitude['Moon'], self._fSubSolarSelenographicLongitude['Moon'], self._fSubSolarSelenographicLatitude['Moon'], self._fSelenographicColongitude['Moon'], self._fPositionAngle['Moon'] = MeeusAlgorithmsFormulas.PhysicalEphemerisMoon_51(self._fJulianCenturies, self._fApparentGeocentricLongitude['Sun'], self._fDistanceInKm['Moon'], self._fDistanceInKm['Sun'], self._fMeanAnomaly['Moon'], self._fMeanAnomaly['Sun'], self._fMeanElongation['Moon'], self._fGeocentricLongitude['Moon'], self._fGeocentricLatitude['Moon'], self._fNutationInLongitude['Earth'], self._fMeanAscendingNodeLongitude['Moon'], self._fArgumentOfLatitude['Moon'], self._fApparentRightAscension['Moon'], self._fTrueObliquityEcliptic['Earth'])

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class MeeusAlgorithms
# 
from toolObjectSerializable import toolObjectSerializable
import math
from CommonAstroFormulaes import CommonAstroFormulaes
#from toolTrace import toolTrace


class MeeusAlgorithmsFormulas(toolObjectSerializable):
    # Terms
    Table45A_iArgD = [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1, 1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2, 4, 0, 3, 2, 4, 0, 2, 2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2, 2]
    Table45A_iArgM = [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2, 0, 0, -1, 0, 0, 1, -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0, 0]
    Table45A_iArgMprime = [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 3, -2, -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0, 2, 0, -1, 1, 0, -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, 2, 1, -2, -3, 2, 1, -1, 3, -1]
    Table45A_iArgF = [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2, 2, 0, 2, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, -2]
    Table45A_iArgEpsilon1 = [6288774, 1274027, 658314, 213618, -185116, -114332, 58793, 57066, 53322, 45758, -40923, -34720, -30383, 15327, -12528, 10980, 10675, 10034, 8548, -7888, -6766, -5163, 4987, 4036, 3994, 3861, 3665, -2689, -2602, 2390, -2348, 2236, -2120, -2069, 2048, -1773, -1595, 1215, -1110, -892, -810, 759, -713, -700, 691, 596, 549, 537, 520, -487, -399, -381, 351, -340, 330, 327, -323, 299, 294, 0]
    Table45A_iArgEpsilonR = [-20905355, -3699111, -2955968, -569925, 48888, -3149, 246158, -152138, -170733, -204586, -129620, 108743, 104755, 10321, 0, 79661, -34782, -23210, -21636, 24208, 30824, -8379, -16675, -12831, -10445, -11650, 14403, -7003, 0, 10056, 6322, -9884, 5751, 0, -4950, 4130, 0, -3958, 0, 3258, 2616, -1897, -2117, 2354, 0, 0, -1423, -1117, -1571, -1739, 0, -4421, 0, 0, 0, 0, 1165, 0, 0, 8752]
    Table45B_iArgD = [0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 4, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4, 4, 0, 4, 2, 2, 2, 2, 0, 2, 2, 2, 2, 4, 2, 2, 0, 2, 1, 1, 0, 2, 1, 2, 0, 4, 4, 1, 4, 1, 4, 2]
    Table45B_iArgM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, -1, -1, -1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 1, 0, -1, -2, 0, 1, 1, 1, 1, 1, 0, -1, 1, 0, -1, 0, 0, 0, -1, -2]
    Table45B_iArgMprime = [0, 1, 1, 0, -1, -1, 0, 2, 1, 2, 0, -2, 1, 0, -1, 0, -1, -1, -1, 0, 0, -1, 0, 1, 1, 0, 0, 3, 0, -1, 1, -2, 0, 2, 1, -2, 3, 2, -3, -1, 0, 0, 1, 0, 1, 1, 0, 0, -2, -1, 1, -2, 2, -2, -1, 1, 1, -1, 0, 0]
    Table45B_iArgF = [1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 3, 1, 1, 1, -1, -1, -1, 1, -1, 1, -3, 1, -3, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 3, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1]
    Table45B_iArgEpsilonb = [5128122, 280602, 277693, 173237, 55413, 46271, 32573, 17198, 9266, 8822, 8216, 4324, 4200, -3359, 2463, 2211, 2065, -1870, 1828, -1794, -1749, -1565, -1491, -1475, -1410, -1344, -1335, 1107, 1021, 833, 777, 671, 607, 596, 491, -451, 439, 422, 421, -366, -351, 331, 315, 302, -283, -229, 223, 223, -220, -220, -185, 181, -177, 176, 166, -164, 132, -119, 115, 107]

    # Class Methods for terms
    @staticmethod
    def _Table45A_getArgument(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude): return (MeeusAlgorithmsFormulas.Table45A_iArgD[iIndex] * fMoonMeanElongation + MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] * fSunMeanAnomaly + MeeusAlgorithmsFormulas.Table45A_iArgMprime[iIndex] * fMoonMeanAnomaly + MeeusAlgorithmsFormulas.Table45A_iArgF[iIndex] * fMoonArgumentOfLatitude) / 360.0 * 2.0 * math.pi
    @staticmethod
    def _Table45A_getTermEpsilon1(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude): return MeeusAlgorithmsFormulas.Table45A_iArgEpsilon1[iIndex] * math.sin(MeeusAlgorithmsFormulas._Table45A_getArgument(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude))
    @staticmethod
    def _Table45A_getTermEpsilonR(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude): return MeeusAlgorithmsFormulas.Table45A_iArgEpsilonR[iIndex] * math.cos(MeeusAlgorithmsFormulas._Table45A_getArgument(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude))
    @staticmethod
    def _Table45A_getTermEpsilon1WithEccentricity(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity): 
        if (MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == 1 or MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == -1): 
            return MeeusAlgorithmsFormulas._Table45A_getTermEpsilon1(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude) * fEccentricity
        elif (MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == 2 or MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == -2): 
            return MeeusAlgorithmsFormulas._Table45A_getTermEpsilon1(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude) * fEccentricity**2
        else:
            return MeeusAlgorithmsFormulas._Table45A_getTermEpsilon1(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude)
    @staticmethod
    def _Table45A_getTermEpsilonRWithEccentricity(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity): 
        if (MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == 1 or MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == -1): 
            return MeeusAlgorithmsFormulas._Table45A_getTermEpsilonR(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude) * fEccentricity
        elif (MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == 2 or MeeusAlgorithmsFormulas.Table45A_iArgM[iIndex] == -2): 
            return MeeusAlgorithmsFormulas._Table45A_getTermEpsilonR(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude) * fEccentricity**2
        else:
            return MeeusAlgorithmsFormulas._Table45A_getTermEpsilonR(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude)
    @staticmethod
    def _Table45A_getSumEpsilon1(fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity):
        fSum = 0.0
        for iIndex in range(0, 60):
            fSum += MeeusAlgorithmsFormulas._Table45A_getTermEpsilon1WithEccentricity(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity)
        return fSum
    @staticmethod
    def _Table45A_getSumEpsilonR(fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity):
        fSum = 0.0
        for iIndex in range(0, 60):
            fSum += MeeusAlgorithmsFormulas._Table45A_getTermEpsilonRWithEccentricity(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity)
        return fSum
    @staticmethod
    def _Table45B_getArgument(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude): return (MeeusAlgorithmsFormulas.Table45B_iArgD[iIndex] * fMoonMeanElongation + MeeusAlgorithmsFormulas.Table45B_iArgM[iIndex] * fSunMeanAnomaly + MeeusAlgorithmsFormulas.Table45B_iArgMprime[iIndex] * fMoonMeanAnomaly + MeeusAlgorithmsFormulas.Table45B_iArgF[iIndex] * fMoonArgumentOfLatitude) / 360.0 * 2.0 * math.pi
    @staticmethod
    def _Table45B_getTermEpsilonB(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude): return MeeusAlgorithmsFormulas.Table45B_iArgEpsilonb[iIndex] * math.sin(MeeusAlgorithmsFormulas._Table45B_getArgument(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude))
    @staticmethod
    def _Table45B_getTermEpsilonBWithEccentricity(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity): 
        if (MeeusAlgorithmsFormulas.Table45B_iArgM[iIndex] == 1 or MeeusAlgorithmsFormulas.Table45B_iArgM[iIndex] == -1): 
            return MeeusAlgorithmsFormulas._Table45B_getTermEpsilonB(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude) * fEccentricity
        elif (MeeusAlgorithmsFormulas.Table45B_iArgM[iIndex] == 2 or MeeusAlgorithmsFormulas.Table45B_iArgM[iIndex] == -2): 
            return MeeusAlgorithmsFormulas._Table45B_getTermEpsilonB(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude) * fEccentricity**2
        else:
            return MeeusAlgorithmsFormulas._Table45B_getTermEpsilonB(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude)
    @staticmethod
    def _Table45B_getSumEpsilonB(fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity):
        fSum = 0.0
        for iIndex in range(0, 60):
            fSum += MeeusAlgorithmsFormulas._Table45B_getTermEpsilonBWithEccentricity(iIndex, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEccentricity)
        return fSum

    # Class Methods
    @staticmethod
    def JulianDay_07_01(iYear, iMonth, iDay, iHour, iMinute, iSecond):     # return fJuliandDay
        # Chapter 7 - Julian Day - Formula 7.1
        #
        #     Input: year, month, day, hour, minutes, seconds
        #
        #     Output: Julian Day (float)
        #
        if iMonth <= 2:
            iM = iMonth + 12
            iY = iYear - 1
        else:
            iM = iMonth
            iY = iYear
        iA = int(iY / 100)
        iB = 2 - iA + int(iA / 4)
        iD = iDay  + (iHour / 24.0) + iMinute / 1440.0 + iSecond / 86400.0
        fJuliandDay = int( 365.25 * (float(iY + 4716))) + int(30.6001 * (float(iM + 1))) + float(iD + iB) - 1524.5
        return fJuliandDay

    @staticmethod
    def DynamicalTime_09_01(fJulianDay):     # return fDeltaT
        # Chapter 9 - Dynamical Time - Formula 9.1
        #
        #     Input: Julian Date
        #
        #     Output: Delta T (difference betwenn UT and Dynamical Time)
        #
        fDeltaT = -15.0 + (((fJulianDay - 2382148.0)**2) / 41048480.0)
        return fDeltaT

    @staticmethod
    def SideralTimeGreenwich_11_01(fJulianDay, fJulianCenturies, fEarthNutationInLongitude, fEarthMeanObliquityEcliptic):     # return fMeanSideralTimeGreenwich, fApparentSideralTimeGreenwich
        # Chapter 9 - Dynamical Time - Formula 11.1
        #
        #     Input: Julian Centuries
        #
        #     Output: Mean Sideral Time Greenwich
        #             Apparent Sideral Time Greenwich
        #
        fMeanSideralTimeGreenwich = ((( 280.46061837 + 360.98564736629 * (fJulianDay - 2451545) + 0.000387933*fJulianCenturies**2 - fJulianCenturies**3 / 38710000) % 360 ) + 360 ) % 360
        fApparentSideralTimeGreenwich = fMeanSideralTimeGreenwich + (fEarthNutationInLongitude * math.cos( math.radians(fEarthMeanObliquityEcliptic * 3600)) / 15)
        return fMeanSideralTimeGreenwich, fApparentSideralTimeGreenwich

    @staticmethod
    def TransformationCoordinates_12_03(fEarthMeanObliquityEcliptic, fMoonGeocentricLongitude, fMoonGeocentricLatitude):     # return fRightAscension
        # Chapter 12 - Transformation of Coordinates - Formula 12.3
        #
        #     Input: Mean Obliquity Ecliptic
        #            Moon Geocentric Longitude
        #            Moon Geocentric Latitude
        #
        #     Output: Right Ascension in deg
        #
        fRightAscension = math.degrees(math.atan2( ( math.sin(math.radians(fMoonGeocentricLongitude)) * math.cos(math.radians(fEarthMeanObliquityEcliptic)) - math.tan(math.radians(fMoonGeocentricLatitude)) * math.sin(math.radians(fEarthMeanObliquityEcliptic)) ) , math.cos(math.radians(fMoonGeocentricLongitude)) ))
        fRightAscension = (fRightAscension + 360.0) % 360.0
        return CommonAstroFormulaes.FormatDegreesTo360(fRightAscension)

    @staticmethod
    def TransformationCoordinates_12_04(fEarthMeanObliquityEcliptic, fMoonGeocentricLongitude, fMoonGeocentricLatitude):     # return fDeclination
        # Chapter 12 - Transformation of Coordinates - Formula 12.4
        #
        #     Input: Mean Obliquity Ecliptic
        #            Moon Geocentric Longitude
        #            Moon Geocentric Latitude
        #
        #     Output: Declination in deg
        #
        fDeclination = math.degrees(math.asin( math.sin(math.radians(fMoonGeocentricLatitude)) * math.cos(math.radians(fEarthMeanObliquityEcliptic)) + math.cos(math.radians(fMoonGeocentricLatitude)) * math.sin(math.radians(fEarthMeanObliquityEcliptic)) * math.sin(math.radians(fMoonGeocentricLongitude)) ))
        return fDeclination

    @staticmethod
    def TransformationCoordinates_12_05(fRightAscension, fDeclination, fObserverLongitude, fObserverLatitude, fGreenwichSideralTime):     # return fAzimut
        # Chapter 12 - Transformation of Coordinates - Formula 12.5
        #
        #     Input: Right Ascension
        #            Declination
        #            Observer Longitude
        #            Observer Latitude
        #            Greenwich Sideral Time
        #
        #     Output: Azimut
        #
        fLocalHourAngle = (((fGreenwichSideralTime - ( fObserverLongitude) - fRightAscension) % 360.0) + 360.0) % 360.0
        fP1 = math.sin(math.radians(fLocalHourAngle))
        fP2 = math.cos(math.radians(fLocalHourAngle)) * math.sin(math.radians(fObserverLatitude)) - math.tan(math.radians(fDeclination)) * math.cos(math.radians(fObserverLatitude))
        fAzimut = math.degrees( math.atan2( fP1 , fP2) ) + 180.0
        return (fAzimut + 360.0) % 360.0

    @staticmethod
    def TransformationCoordinates_12_06(fRightAscension, fDeclination, fObserverLongitude, fObserverLatitude, fGreenwichSideralTime):     # return fElevation
        # Chapter 12 - Transformation of Coordinates - Formula 12.6
        #
        #     Input: Right Ascension
        #            Declination
        #            Observer Longitude
        #            Observer Latitude
        #            Greenwich Sideral Time
        #
        #     Output: Elevation
        #
        fLocalHourAngle = (((fGreenwichSideralTime - ( fObserverLongitude) - fRightAscension) % 360.0) + 360.0) % 360.0
        fElevation = math.degrees(math.asin( math.sin(math.radians(fObserverLatitude)) * math.sin(math.radians(fDeclination)) + math.cos(math.radians(fObserverLatitude)) * math.cos(math.radians(fDeclination)) * math.cos(math.radians(fLocalHourAngle)) ))
        return fElevation

    @staticmethod
    def AngularSeparation_16_01(fRightAscensionA, fDeclinationA, fRightAscensionB, fDeclinationB):     # return fAngularSeparationDeg
        # Chapter 16 - Angular Separation - Formula 16.1
        #
        #     Input: Right Ascension for object A
        #            Declination for Object A
        #            Right Ascension for object B
        #            Declination for Object B
        #
        #     Output: Angular Separation in Deg
        #
        fAngularSeparationDeg = math.acos( math.sin(math.radians(fDeclinationA)) * math.sin(math.radians(fDeclinationB))  +  math.cos(math.radians(fDeclinationA)) * math.cos(math.radians(fDeclinationB)) * math.cos(math.radians(fRightAscensionA - fRightAscensionB)) )
        return CommonAstroFormulaes.FormatDegreesTo360(math.degrees(fAngularSeparationDeg))

    @staticmethod
    def NutationObliquity_21_00(fJulianDay):     # return fJuliandEphemerisDay, fJulianCenturies, fJulianEphemerisCenturies
        # Chapter 21 - Nutation And Obliquity - Formula 21.0
        #
        #     Input: Julian Date
        #
        #     Output: Julian Ephemeris Day (JDE)
        #             Julian Centuries from Epoch 2000.0 (2000 January 1.5 TD)
        #             Julian Ephemeris Centuries from Epoch 2000.0 (2000 January 1 TD)
        #
        fJuliandEphemerisDay = fJulianDay + MeeusAlgorithmsFormulas.DynamicalTime_09_01(fJulianDay) / 86400.0
        fJulianCenturies = (fJulianDay - 2451545.0) / 36525.0
        fJulianEphemerisCenturies = (fJuliandEphemerisDay - 2451545.0) / 36525.0
        return fJuliandEphemerisDay, fJulianCenturies, fJulianEphemerisCenturies

    @staticmethod
    def NutationObliquity_21_01(fJulianCenturies, fSunGeometricMeanLongitude, fMoonMeanLongitude):     # return fMoonLongitudeAscendNode, fEarthNutationInLongitude
        # Chapter 21 - Nutation And Obliquity - Formula 21.1
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #            Sun Geometric Mean Longitude
        #            Moon Mean Longitude
        #
        #     Output: Moon Longitude AscendNode
        #             Moon Nutation In Longitude
        #

        fMoonLongitudeAscendNode = CommonAstroFormulaes.FormatDegreesTo360(125.04452 - 1934.136261 * fJulianCenturies + 0.0020708 * fJulianCenturies**2 + fJulianCenturies**3 / 450000.0)
        fEarthNutationInLongitude = (-17.2 * math.sin(math.radians(fMoonLongitudeAscendNode)) - 1.32 * math.sin(math.radians(2.0 * fSunGeometricMeanLongitude)) - 0.23 * math.sin(math.radians(2.0 * fMoonMeanLongitude)) + 0.21 * math.sin( math.radians(2.0 * fMoonLongitudeAscendNode))) / 3600.0
        return fMoonLongitudeAscendNode, fEarthNutationInLongitude
        
    @staticmethod
    def NutationObliquity_21_02(fJulianCenturies):     # return fEarthMeanObliquityEcliptic
        # Chapter 21 - Nutation And Obliquity - Formula 21.2
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Mean Obliquity of the Ecliptic
        #
        fEarthMeanObliquityEcliptic = (23.0 * 3600.0) + (26.0 * 60.0) + 21.448
        fEarthMeanObliquityEcliptic += - 4680.93  * (fJulianCenturies / 100.0)
        fEarthMeanObliquityEcliptic += - 1.55  * (fJulianCenturies / 100.0)**2
        fEarthMeanObliquityEcliptic +=   1999.25  * (fJulianCenturies / 100.0)**3
        fEarthMeanObliquityEcliptic += - 51.38  * (fJulianCenturies / 100.0)**4
        fEarthMeanObliquityEcliptic += - 249.67  * (fJulianCenturies / 100.0)**5
        fEarthMeanObliquityEcliptic += - 39.05  * (fJulianCenturies / 100.0)**6
        fEarthMeanObliquityEcliptic +=   7.12  * (fJulianCenturies / 100.0)**7
        fEarthMeanObliquityEcliptic +=   27.87  * (fJulianCenturies / 100.0)**8
        fEarthMeanObliquityEcliptic +=   5.79  * (fJulianCenturies / 100.0)**9
        fEarthMeanObliquityEcliptic +=   2.45  * (fJulianCenturies / 100.0)**10
        fEarthMeanObliquityEcliptic2 = (23.0 * 3600.0)  + (26.0 * 60.0) + 21.448  - (46.8150 * fJulianCenturies - 0.00059 * fJulianCenturies**2 + 0.001813 * fJulianCenturies**3)
        return CommonAstroFormulaes.FormatDegreesTo360(float((fEarthMeanObliquityEcliptic + fEarthMeanObliquityEcliptic2) / 2.0 / 3600.0))

    @staticmethod
    def SunCoordinates_24_02(fJulianCenturies):     # return fSunGeometricMeanLongitude
        # Chapter 24 - Sun Coordinates - Formula 24.2
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Geometric Mean Longitude of the Sun (degrees)
        #
        fSunGeometricMeanLongitude =  CommonAstroFormulaes.FormatDegreesTo360(280.46645 + 36000.76983 * fJulianCenturies + 0.0003032 * fJulianCenturies**2)
        return CommonAstroFormulaes.FormatDegreesTo360(fSunGeometricMeanLongitude)

    @staticmethod
    def SunCoordinates_24_03(fJulianCenturies):     # return fSunMeanAnomaly
        # Chapter 24 - Sun Coordinates - Formula 24.3
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Mean Anomaly of the Sun (degrees)
        #
        fSunMeanAnomaly = CommonAstroFormulaes.FormatDegreesTo360(357.5291 + 35999.0503 * fJulianCenturies - 0.0001559 * fJulianCenturies**2 - 0.00000048 * fJulianCenturies**3)
        return CommonAstroFormulaes.FormatDegreesTo360(fSunMeanAnomaly)

    @staticmethod
    def SunCoordinates_24_04(fJulianCenturies):     # return fEarthOrbitEccentricity
        # Chapter 24 - Sun Coordinates - Formula 24.4
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Eccentricity of the Earth Orbit 
        #
        fEarthOrbitEccentricity = 0.016708617 - 0.000042037 * fJulianCenturies - 0.0000001236 * fJulianCenturies**2
        return fEarthOrbitEccentricity

    @staticmethod
    def SunCoordinates_24_05(fJulianCenturies, fSunMeanAnomaly, fSunGeometricMeanLongitude, fEarthOrbitEccentricity):     # return fSunEquationCenter, fSunTrueGeometricLongitude, fSunTrueAnomaly, fDistanceFromEarthToSunInUA, fDistanceFromEarthToSunInKm, fSunApparentGeometricLongitude
        # Chapter 24 - Sun Coordinates - Formula 24.5
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #            Mean Anomaly of the Sun (degrees)
        #            Geometric Mean Longitude of the Sun (degrees)
        #            Eccentricity of Earth Orbit
        #
        #     Output: Sun Equation of Center
        #             Sun True Geometric Longitude (degrees)
        #             Distance From Earth To Sun In UA
        #             Distance From Earth To Sun In Km
        #             Sun Apparent Geometric Longitude (degrees)
        #
        fSunEquationCenter = (1.9146 - 0.004817 * fJulianCenturies - 0.000014 * fJulianCenturies**2) * math.sin(math.radians(fSunMeanAnomaly)) + (0.019993 - 0.000101 * fJulianCenturies) * math.sin(math.radians(2.0 * fSunMeanAnomaly)) + 0.00029 * math.sin(math.radians(3.0 * fSunMeanAnomaly))
        fSunTrueGeometricLongitude = fSunGeometricMeanLongitude + fSunEquationCenter
        fSunTrueAnomaly = fSunMeanAnomaly + fSunEquationCenter
        fDistanceFromEarthToSunInUA = (1.000001018 * (1.0 - fEarthOrbitEccentricity**2)) / (1.0 + fEarthOrbitEccentricity * math.cos(math.radians(fSunMeanAnomaly + fSunEquationCenter)))
        fDistanceFromEarthToSunInKm = CommonAstroFormulaes.ConvertUAToKM(fDistanceFromEarthToSunInUA)
        fSunApparentGeometricLongitude = fSunTrueGeometricLongitude - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * fJulianCenturies))
        return fSunEquationCenter, CommonAstroFormulaes.FormatDegreesTo360(fSunTrueGeometricLongitude), CommonAstroFormulaes.FormatDegreesTo360(fSunTrueAnomaly), fDistanceFromEarthToSunInUA, fDistanceFromEarthToSunInKm, CommonAstroFormulaes.FormatDegreesTo360(fSunApparentGeometricLongitude)

    @staticmethod
    def SunCoordinates_24_06(fSunTrueGeometricLongitude, fEarthMeanObliquityEcliptic, fJulianCenturies):     # return fSunApparentRightAscension
        # Chapter 24 - Sun Coordinates - Formula 24.6
        #
        #     Input: Sun True Geometric Longitude (degrees)
        #            Obliquity of Ecliptic
        #
        #     Output: Sun Apparent Right Ascension (degrees)
        #
        fOmega = 125.04 - 1934.136 * fJulianCenturies
        fLambda = fSunTrueGeometricLongitude - 0.00569 - 0.00478 * math.sin(math.radians(fOmega))
        fEarthMeanObliquityEclipticCorrected = fEarthMeanObliquityEcliptic + 0.00256 *  math.cos(math.radians(fOmega))
        fSunApparentRightAscension = math.degrees(math.atan2(math.cos(math.radians(fEarthMeanObliquityEclipticCorrected)) * math.sin(math.radians(fLambda)), math.cos(math.radians(fLambda))))
        return fSunApparentRightAscension

    @staticmethod
    def SunCoordinates_24_06a(fSunTrueGeometricLongitude, fEarthMeanObliquityEcliptic, fJulianCenturies):     # return fSunRightAscension
        # Chapter 24 - Sun Coordinates - Formula 24.6
        #
        #     Input: Sun True Geometric Longitude (degrees)
        #            Obliquity of Ecliptic
        #
        #     Output: Sun Right Ascension (degrees)
        #
        fSunRightAscension = math.degrees(math.atan2(math.cos(math.radians(fEarthMeanObliquityEcliptic)) * math.sin(math.radians(fSunTrueGeometricLongitude)), math.cos(math.radians(fSunTrueGeometricLongitude))))
        return fSunRightAscension

    @staticmethod
    def SunCoordinates_24_07(fSunTrueGeometricLongitude, fEarthMeanObliquityEcliptic, fJulianCenturies):     # return fSunApparentDeclination
        # Chapter 24 - Sun Coordinates - Formula 24.7
        #
        #     Input: Sun True Geometric Longitude (degrees)
        #            Obliquity of Ecliptic
        #
        #     Output: Sun Apparent Declination (degrees)
        #
        fOmega = 125.04 - 1934.136 * fJulianCenturies
        fLambda = fSunTrueGeometricLongitude - 0.00569 - 0.00478 * math.sin(math.radians(fOmega))
        fEarthMeanObliquityEclipticCorrected = fEarthMeanObliquityEcliptic + 0.00256 *  math.cos(math.radians(fOmega))
        fSunApparentDeclination = math.degrees( math.asin( math.sin(math.radians(fEarthMeanObliquityEclipticCorrected)) *  math.sin(math.radians(fLambda))))
        return fSunApparentDeclination

    @staticmethod
    def SunCoordinates_24_07a(fSunTrueGeometricLongitude, fEarthMeanObliquityEcliptic):     # return fSunDeclination
        # Chapter 24 - Sun Coordinates - Formula 24.7
        #
        #     Input: Sun True Geometric Longitude (degrees)
        #            Obliquity of Ecliptic
        #
        #     Output: Sun Declination (degrees)
        #
        fSunDeclination = math.degrees( math.asin( math.sin(math.radians(fEarthMeanObliquityEcliptic)) *  math.sin(math.radians(fSunTrueGeometricLongitude))))
        return fSunDeclination

    @staticmethod
    def SunCoordinates_24_09(fSunTrueGeometricLongitude, fSunTrueGeometricLatitude):     # return fSunGeocentricLongitude, fSunGeocentricLatitude
        # Chapter 24 - Sun Coordinates - Formula 24.09 (page 154)
        #
        #     Input: Sun True Geometric Longitude (degrees)
        #            Sun True Geometric Latitude (degrees)
        #
        #     Output: Sun Geocentric Longitude (degrees)
        #             Sun Geocentric Latitude (degrees)
        #
        fSunGeocentricLongitude = fSunTrueGeometricLongitude + 180.0
        fSunGeocentricLatitude = - fSunTrueGeometricLatitude
        return CommonAstroFormulaes.FormatDegreesTo360(fSunGeocentricLongitude), CommonAstroFormulaes.FormatDegreesTo360(fSunGeocentricLatitude)
       
    @staticmethod
    def PositionMoon_45_01(fJulianCenturies):     # return fMoonMeanLongitude
        # Chapter 24 - position Of The Moon - Formula 45.1
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Moon Mean Longitude (degrees)
        #
        fMoonMeanLongitude = CommonAstroFormulaes.FormatDegreesTo360(218.3164591 + (481267.88134236 * fJulianCenturies) - (0.0013268 * fJulianCenturies**2) + (fJulianCenturies**3 / 538841) - (fJulianCenturies**4 / 65194000))
        return fMoonMeanLongitude

    @staticmethod
    def PositionMoon_45_02(fJulianCenturies):     # return fMoonMeanElongation
        # Chapter 24 - position Of The Moon - Formula 45.2
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Moon Mean Elongation (degrees)
        #
        fMoonMeanElongation = CommonAstroFormulaes.FormatDegreesTo360( 297.8502042 + ( 445267.1115168 * fJulianCenturies ) - ( 0.0016300 * fJulianCenturies**2 ) + ( fJulianCenturies**3 / 545868 ) - (fJulianCenturies**4 / 113065000 ) )
        return fMoonMeanElongation

    @staticmethod
    def PositionMoon_45_03(fJulianCenturies):     # return fSunMeanAnomaly
        # Chapter 24 - position Of The Moon - Formula 45.2
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Mean Anomaly of the Sun (degrees)
        #
        fSunMeanAnomaly = CommonAstroFormulaes.FormatDegreesTo360(357.5291092 + (35999.0502909 * fJulianCenturies) - (0.0001536 * fJulianCenturies**2) + (fJulianCenturies**3 / 24490000))
        return fSunMeanAnomaly

    @staticmethod
    def PositionMoon_45_04(fJulianCenturies):     # return fMoonMeanAnomaly
        # Chapter 24 - position Of The Moon - Formula 45.4
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Moon Anomaly of the Sun (degrees)
        #
        fMoonMeanAnomaly = CommonAstroFormulaes.FormatDegreesTo360( 134.9634114 + ( 477198.8676313 * fJulianCenturies ) + ( 0.0089970 * fJulianCenturies**2 ) + ( fJulianCenturies**3 / 69699 ) - (  fJulianCenturies**4 / 14712000 ) )
        return fMoonMeanAnomaly

    @staticmethod
    def PositionMoon_45_05(fJulianCenturies):     # return fMoonArgumentOfLatitude
        # Chapter 24 - position Of The Moon - Formula 45.5
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Moon Argument of latitude (degrees)    - i.e.  Mean distance of the moon from its ascending node
        #
        fMoonArgumentOfLatitude = CommonAstroFormulaes.FormatDegreesTo360( 93.2720993 + ( 483202.0175273 * fJulianCenturies ) - ( 0.0034029 * fJulianCenturies**2 ) - ( fJulianCenturies**3 / 3526000 ) + ( fJulianCenturies**4 / 863310000 ) )
        return fMoonArgumentOfLatitude

    @staticmethod
    def PositionMoon_45_06(fJulianCenturies, fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fMoonMeanLongitude):     # return fMoonGeocentricLongitude, fMoonGeocentricLatitude, fMoonDistanceInKm
        # Chapter 24 - position Of The Moon - Formula 45.6
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #            MoonMeanElongation
        #            Sun Mean Anomaly
        #            Moon Mean Anomaly
        #            Moon Argument Of Latitude
        #            Eccentricity of Earth orbit around the sun
        #
        #     Output: Moon Geocentric Longitude (degrees)
        #             Moon Geocentric Latitude (degrees)
        #             Moon Distance In Km (degrees)
        #
        fA1 = 119.75 + 131.849 * fJulianCenturies
        fA2 = CommonAstroFormulaes.FormatDegreesTo360(53.09 + 479264.29 * fJulianCenturies)
        fA3 = CommonAstroFormulaes.FormatDegreesTo360(313.45 + 481266.484 * fJulianCenturies)
        fEarthEccentricity = 1.0 - 0.002516 * fJulianCenturies - 0.0000074 * fJulianCenturies**2
        fSumEpsilon1 = MeeusAlgorithmsFormulas._Table45A_getSumEpsilon1(fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEarthEccentricity)
        fSumEpsilonR = MeeusAlgorithmsFormulas._Table45A_getSumEpsilonR(fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEarthEccentricity)
        fSumEpsilonB = MeeusAlgorithmsFormulas._Table45B_getSumEpsilonB(fMoonMeanElongation, fSunMeanAnomaly, fMoonMeanAnomaly, fMoonArgumentOfLatitude, fEarthEccentricity)
        fSumEpsilon1AdditiveTerm = 3958.0 * math.sin(math.radians(fA1)) + 1962.0 * math.sin(math.radians(fMoonMeanLongitude - fMoonArgumentOfLatitude)) + 318.0 * math.sin(math.radians(fA2))
        fSumEpsilonBAdditiveTerm = -2235.0 * math.sin(math.radians(fMoonMeanLongitude)) + 382.0 * math.sin(math.radians(fA3)) + 175.0 * math.sin(math.radians(fA1 - fMoonArgumentOfLatitude)) + 175.0 * math.sin(math.radians(fA1 + fMoonArgumentOfLatitude)) + 127.0 * math.sin(math.radians(fMoonMeanLongitude - fMoonMeanAnomaly)) - 115.0 * math.sin(math.radians(fMoonMeanLongitude + fMoonMeanAnomaly))
        fSumEpsilon1 += fSumEpsilon1AdditiveTerm
        fSumEpsilonB += fSumEpsilonBAdditiveTerm
        fMoonGeocentricLongitude = fMoonMeanLongitude  + fSumEpsilon1 / 1000000.0
        fMoonGeocentricLatitude = fSumEpsilonB / 1000000.0
        fMoonDistanceInKm = 385000.56 + fSumEpsilonR / 1000.0
        return fMoonGeocentricLongitude, fMoonGeocentricLatitude, fMoonDistanceInKm

    @staticmethod
    def PositionMoon_45_07(fJulianCenturies):     # return fMoonMeanAscendingNodeLongitude
        # Chapter 24 - position Of The Moon - Formula 45.7
        #
        #     Input: Julian Centuries from Epoch 2000.0
        #
        #     Output: Moon Mean Ascending Node Longitude (degrees)
        #
        fMoonMeanAscendingNodeLongitude = 125.0445550 - 1934.1361849 * fJulianCenturies + (0.0020762 * fJulianCenturies**2) + (fJulianCenturies**3 / 467410) - (fJulianCenturies**4 / 60616000)
        return CommonAstroFormulaes.FormatDegreesTo360(fMoonMeanAscendingNodeLongitude)
        
    @staticmethod
    def IlluminatedFractionMoon_46_04(fMoonMeanElongation, fMoonMeanAnomaly, fSunMeanAnomaly):     # return fMoonPhaseAngle
        # Chapter 46 - Illuminated Fraction Of Moon - Formula 46.4
        #
        #     Input: Moon Mean Elongation
        #            Moon Mean Anomaly
        #            Sun Mean Anomaly
        #
        #     Output: Moon Phase Angle
        #
        fMoonPhaseAngle = 180.0 - fMoonMeanElongation - 6.289 * math.sin(math.radians(fMoonMeanAnomaly)) + 2.1 * math.sin(math.radians(fSunMeanAnomaly)) - 1.274 * math.sin(math.radians(2.0 * fMoonMeanElongation - fMoonMeanAnomaly)) - 0.658 * math.sin(math.radians(2.0 * fMoonMeanElongation)) - 0.214 * math.sin(math.radians(2.0 * fMoonMeanAnomaly)) - 0.11 * math.sin(math.radians(fMoonMeanElongation))
        return fMoonPhaseAngle

    @staticmethod
    def IlluminatedFractionMoon_46_01(fMoonPhaseAngle):     # return fMoonIlluminatedFraction
        # Chapter 46 - Illuminated Fraction Of Moon - Formula 46.1
        #
        #     Input: Moon Phase Angle
        #
        #     Output: Illuminated Fraction of the Moon
        #
        fMoonIlluminatedFraction = (1.0 + math.cos(math.radians(fMoonPhaseAngle))) / 2.0
        return fMoonIlluminatedFraction

    @staticmethod
    def PhysicalEphemerisMoon_51(fJulianCenturies, fSunApparentGeocentricLongitude, fMoonDistanceFromEarthInKm, fSunDistanceFromEarthInKm, fMoonMeanAnomaly, fSunMeanAnomaly, fMoonMeanElongation, fMoonGeocentricLongitude, fMoonGeocentricLatitude, fEarthNutationInLongitude, fMoonMeanAscendingNodeLongitude, fMoonArgumentOfLatitude):     # return fMoonOpticalLibrationInLongitude, fMoonOpticalLibrationInLatitude, fARad
        #51.01
        fW = fMoonGeocentricLongitude - fEarthNutationInLongitude - fMoonMeanAscendingNodeLongitude
        fW = CommonAstroFormulaes.FormatDegreesTo360(fW)
        fARad = math.atan2(((math.sin(math.radians(fW)) * math.cos(math.radians(fMoonGeocentricLatitude)) * math.cos(math.radians(1.54242))) - (math.sin(math.radians(fMoonGeocentricLatitude)) * math.sin(math.radians(1.54242)))) , (math.cos(math.radians(fW)) * math.cos(math.radians(fMoonGeocentricLatitude))))
        fARad = CommonAstroFormulaes.FormatRadiansTo2Pi(fARad)

        fA = math.degrees(fARad)
        fMoonOpticalLibrationInLongitude = fA - fMoonArgumentOfLatitude
        fMoonOpticalLibrationInLatitudeRad = math.asin(-1.0 * math.sin(math.radians(fW)) * math.cos(math.radians(fMoonGeocentricLatitude)) * math.sin(math.radians(1.54242)) - math.sin(math.radians(fMoonGeocentricLatitude)) * math.cos(math.radians(1.54242)))
        fMoonOpticalLibrationInLatitudeRad = (fMoonOpticalLibrationInLatitudeRad + (2.0 * math.pi) ) % (2.0 * math.pi)
        fMoonOpticalLibrationInLatitude = math.degrees(fMoonOpticalLibrationInLatitudeRad)
        
        #51.02
        fRadMoonMeanAnomaly = math.radians(fMoonMeanAnomaly)
        fRadMoonArgumentOfLatitude = math.radians(fMoonArgumentOfLatitude)
        fRadMoonMeanElongation = math.radians(fMoonMeanElongation)
        fRadMoonMeanAnomalyX2 = 2.0 * fRadMoonMeanAnomaly
        fRadMoonArgumentOfLatitudeX2 = 2.0 * fRadMoonArgumentOfLatitude
        fRadMoonMeanElongationX2 = 2.0 * fRadMoonMeanElongation
        fRadMoonArgumentOfLatitudeX3 = 3.0 * fRadMoonArgumentOfLatitude
        
        fRadK1 = math.radians(119.75 + 131.849 * fJulianCenturies)
        fRadK2 = math.radians(72.56 + 20.186 * fJulianCenturies)

        fRadMoonMeanAscendingNodeLongitude = math.radians(fMoonMeanAscendingNodeLongitude)
        fRadSunMeanAnomaly = math.radians(fSunMeanAnomaly)
        fRadSunMeanAnomalyX2 = fRadSunMeanAnomaly * 2.0
        fT_p = -0.02752 * math.cos(fRadMoonMeanAnomaly) 
        fT_p -= 0.02245 * math.sin(fRadMoonArgumentOfLatitude) 
        fT_p += 0.00684 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX2) 
        fT_p -= 0.00293 * math.cos(fRadMoonArgumentOfLatitudeX2) 
        fT_p -= 0.00085 * math.cos(fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) 
        fT_p -= 0.00054 * math.cos(fRadMoonMeanAnomaly - fRadMoonMeanElongationX2) 
        fT_p -= 0.0002  * math.sin(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitude) 
        fT_p -= 0.0002  * math.cos(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2) 
        fT_p -= 0.0002  * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) 
        fT_p += 0.00014 * math.cos(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2)
        
        fT_o = -0.02816 * math.sin(fRadMoonMeanAnomaly) 
        fT_o += 0.02244 * math.cos(fRadMoonArgumentOfLatitude) 
        fT_o -= 0.00682 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX2)
        fT_o -= 0.00279 * math.sin(fRadMoonArgumentOfLatitudeX2) 
        fT_o -= 0.00083 * math.sin(fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) 
        fT_o += 0.00069 * math.sin(fRadMoonMeanAnomaly - fRadMoonMeanElongationX2) 
        fT_o += 0.0004  * math.cos(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitude) 
        fT_o -= 0.00025 * math.sin(fRadMoonMeanAnomalyX2) 
        fT_o -= 0.00023 * math.sin(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2) 
        fT_o += 0.0002  * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) 
        fT_o += 0.00019 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) 
        fT_o += 0.00013 * math.sin(fRadMoonMeanAnomaly + fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) 
        fT_o -= 0.0001  * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX3)
        
        fE = (1.0 - 0.002516 * fJulianCenturies - 0.0000074 * fJulianCenturies ** 2.0)
        
        fT_t = 0.0252 * fE * math.sin(fRadSunMeanAnomaly) 
        fT_t += 0.00473 * math.sin(fRadMoonMeanAnomalyX2 - fRadMoonArgumentOfLatitudeX2) 
        fT_t -= 0.00467 * math.sin(fRadMoonMeanAnomaly) 
        fT_t += 0.00396 * math.sin(fRadK1) 
        fT_t += 0.00276 * math.sin(fRadMoonMeanAnomalyX2 - fRadMoonMeanElongationX2) 
        fT_t += 0.00196 * math.sin(fRadMoonMeanAscendingNodeLongitude) 
        fT_t -= 0.00183 * math.cos(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) 
        fT_t += 0.00115 * math.sin(fRadMoonMeanAnomaly - fRadMoonMeanElongationX2) 
        fT_t -= 0.00096 * math.sin(fRadMoonMeanAnomaly - fRadMoonMeanElongation) 
        fT_t += 0.00046 * math.sin(fRadMoonArgumentOfLatitudeX2 - fRadMoonMeanElongationX2) 
        fT_t -= 0.00039 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitude) 
        fT_t -= 0.00032 * math.sin(fRadMoonMeanAnomaly - fRadSunMeanAnomaly - fRadMoonMeanElongation) 
        fT_t += 0.00027 * math.sin(fRadMoonMeanAnomalyX2 - fRadSunMeanAnomaly - fRadMoonMeanElongationX2) 
        fT_t += 0.00023 * math.sin(fRadK2) 
        fT_t -= 0.00014 * math.sin(fRadMoonMeanElongationX2) 
        fT_t += 0.00014 * math.cos(fRadMoonMeanAnomalyX2 - fRadMoonArgumentOfLatitudeX2) 
        fT_t -= 0.00012 * math.sin(fRadMoonMeanAnomaly - fRadMoonArgumentOfLatitudeX2) 
        fT_t -= 0.00012 * math.sin(fRadMoonMeanAnomalyX2) 
        fT_t += 0.00011 * math.sin(fRadMoonMeanAnomalyX2 - fRadSunMeanAnomalyX2 - fRadMoonMeanElongationX2)
        
        fLambdaSecondO = -fT_t + (fT_p * math.cos(fARad) + fT_o * math.sin(fARad)) * math.tan(fMoonOpticalLibrationInLatitudeRad)
        fBetaSecondO = fT_o * math.cos(fARad) - fT_p * math.sin(fARad)

        #51.01 for Selenographic longitude (page 346)
        fLambdaH = fSunApparentGeocentricLongitude + 180.0 + (float(fMoonDistanceFromEarthInKm) / float(fSunDistanceFromEarthInKm) * 57.296) * math.cos(math.radians(fMoonGeocentricLatitude)) * math.sin(math.radians(fSunApparentGeocentricLongitude - fMoonGeocentricLongitude))
        fBetaH = (float(fMoonDistanceFromEarthInKm) / float(fSunDistanceFromEarthInKm)) * fMoonGeocentricLatitude

        fW_H = fLambdaH - fEarthNutationInLongitude - fMoonMeanAscendingNodeLongitude
        fW_H = (fW_H + 360.0) % 360.0
        fARad_H = math.atan2( ( (  math.sin(math.radians(fW_H)) * math.cos(math.radians(fBetaH)) * math.cos(math.radians(1.54242))) - ( math.sin(math.radians(fBetaH)) * math.sin(math.radians(1.54242)) ) )  , ( math.cos(math.radians(fW_H)) * math.cos(math.radians(fBetaH)) ))
        
        fARad_H = (fARad_H + (2.0 * math.pi)) % (2.0 * math.pi)
        fA_H = math.degrees(fARad_H)

        fLPrime_H = fA_H - fMoonArgumentOfLatitude
        fBPrime_HRad = math.asin(-1.0 * math.sin(math.radians(fW_H)) * math.cos(math.radians(fBetaH)) * math.sin(math.radians(1.54242)) - math.sin(math.radians(fBetaH)) * math.cos(math.radians(1.54242)))
        fBPrime_HRad = (fBPrime_HRad + (2.0 * math.pi)) % (2.0 * math.pi)
        fBPrime_H = math.degrees(fBPrime_HRad)
        
        fLSecond_H = -fT_t + (fT_p * math.cos(fARad_H) + fT_o * math.sin(fARad_H)) * math.tan(fBPrime_HRad)
        fBSecond_H = fT_o * math.cos(fARad_H) - fT_p * math.sin(fARad_H)

        # Longitude on the Moon is measured both east and west from its prime meridian. When no direction is specified, east is positive and west is negative.
        fMoonSubSolarSelenographicLongitude = (fLPrime_H + fLSecond_H) % 360.0
        fMoonSubSolarSelenographicLatitude = (fBPrime_H + fBSecond_H) % 360.0
        
        # The selenographic colongitude is the longitude of the morning terminator on the Moon, as measured in degrees westward from the prime meridian. 
        fMoonSelenographicColongitude = (360 - (fMoonSubSolarSelenographicLongitude - 90)) % 360.0
#        fMoonSelenographicColongitude = (fMoonSelenographicLongitude - 90.0 + 360.0) % 360.0 #(450.0 - self._fMoonSelenographicLongitude) - int((450.0 - self._fMoonSelenographicLongitude) / 360.0) * 360.0
#        if fMoonSelenographicColongitude > 180.0: fMoonSelenographicColongitude = fMoonSelenographicColongitude - 360.0
        
        return fMoonOpticalLibrationInLongitude, fMoonOpticalLibrationInLatitude, fMoonSubSolarSelenographicLongitude, fMoonSubSolarSelenographicLatitude, fMoonSelenographicColongitude

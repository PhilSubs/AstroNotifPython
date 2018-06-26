#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class MeeusAlgorithms
# 
from toolObjectSerializable import toolObjectSerializable
import math
from MeeusTable45A import MeeusTable45A
from MeeusTable45B import MeeusTable45B
#from toolTrace import toolTrace
from MeeusAlgorithmsFormulas import MeeusAlgorithmsFormulas


class MeeusAlgorithmsFormulasTests(toolObjectSerializable):
    # Internal Methods
    @staticmethod
    def _CompareFloat(fValue, fExpectedValue, iPrecision):
        fRoundedValue = round(fValue, iPrecision)
        fRoundedExpectedValue = round(fExpectedValue, iPrecision)
        return (fRoundedValue == fRoundedExpectedValue)
    @staticmethod
    def _ExpandWithChars(sString, sChar, iNbChars):
        return (sString + (sChar * iNbChars))[:iNbChars]
    @staticmethod
    def _ExpandWithBlanks(sString, iNbChars):
        return MeeusAlgorithmsFormulasTests._ExpandWithChars(sString, " ", iNbChars)
    @staticmethod
    def _LeftExpandWithBlanks(sString, iNbChars):
        return ((" " * iNbChars) + sString)[-iNbChars:]
    @staticmethod
    def _FormatResultAsText(fValue, fExpectedValue, iPrecision, sFormulaName, sParameters, sComment):
        bStatus = MeeusAlgorithmsFormulasTests._CompareFloat(fValue, fExpectedValue, iPrecision)
        if bStatus:
            sFormattedText =  "       "
        else:
            sFormattedText =  ">>> KO "
        return (sFormattedText + "  " + MeeusAlgorithmsFormulasTests._ExpandWithBlanks(sComment, 32) + "  " + MeeusAlgorithmsFormulasTests._ExpandWithBlanks(sFormulaName + " (" + sParameters + ")", 70) + " = " + MeeusAlgorithmsFormulasTests._ExpandWithBlanks(str(fValue), 15) + " Expected: " + MeeusAlgorithmsFormulasTests._ExpandWithBlanks(str(fExpectedValue), 16)) + "   " + str(float('{:0.8f}'.format(round(fValue, iPrecision) - round(fExpectedValue, iPrecision)).rstrip('0'))) + "  (" + str(iPrecision) + ")"
    @staticmethod
    def displayValue(fValue, iPrecision, fName, fFormulaName):
        print MeeusAlgorithmsFormulasTests._ExpandWithChars(fName, ".", 40) + "  " + MeeusAlgorithmsFormulasTests._LeftExpandWithBlanks(str(round(fValue, iPrecision)), 15) + "  " + MeeusAlgorithmsFormulasTests._ExpandWithBlanks(fFormulaName,70)
    
    
    # Class Methods
    @staticmethod
    def TestAll():
        print ""
        print MeeusAlgorithmsFormulasTests.Test_07_JulianDay_07_01()
        print MeeusAlgorithmsFormulasTests.Test_09_DynamicalTime_09_01()
        print MeeusAlgorithmsFormulasTests.Test_TransformationCoordinates_12_03()
        print MeeusAlgorithmsFormulasTests.Test_TransformationCoordinates_12_04()
        print MeeusAlgorithmsFormulasTests.Test_11_SideralTimeGreenwich_11_01()
        print MeeusAlgorithmsFormulasTests.Test_NutationObliquity_21_00()
        print MeeusAlgorithmsFormulasTests.Test_NutationObliquity_21_01()
        print MeeusAlgorithmsFormulasTests.Test_NutationObliquity_21_02()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_02()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_03()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_04()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_05()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_06()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_07()
        print MeeusAlgorithmsFormulasTests.Test_SunCoordinates_24_09()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_01()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_02()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_03()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_04()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_05()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_06()
        print MeeusAlgorithmsFormulasTests.Test_PositionMoon_45_07()
        print MeeusAlgorithmsFormulasTests.Test_IlluminatedFractionMoon_46_04()
        print MeeusAlgorithmsFormulasTests.Test_IlluminatedFractionMoon_46_01()
        print MeeusAlgorithmsFormulasTests.Test_PhysicalEphemerisMoon_51()
        print ""
    @staticmethod
    def DisplayValues(fNowYear, fNowMonth, fNowDay, fNowHours, fNowMinutes, fNowSeconds):
        print ""
        print "Values for " + str(fNowHours) + ":" + str(fNowMinutes) + ":" + str(fNowSeconds) + " on " + str(fNowDay) + "-" + str(fNowMonth) + "-" + str(fNowYear)
        print ""
        print ""

        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(fNowYear, fNowMonth, fNowDay, fNowHours, fNowMinutes, fNowSeconds)
        fDeltaT = MeeusAlgorithmsFormulas.DynamicalTime_09_01(fJulianDay)
        fJuliandEphemerisDay, fJulianCenturies, fJulianEphemerisCenturies = MeeusAlgorithmsFormulas.NutationObliquity_21_00(fJulianDay)
        fMeanObliquityEcliptic_Earth = MeeusAlgorithmsFormulas.NutationObliquity_21_02(fJulianCenturies)
        fEccentricity_Earth = MeeusAlgorithmsFormulas.SunCoordinates_24_04(fJulianCenturies)
        fGeometricMeanLongitude_Sun = MeeusAlgorithmsFormulas.SunCoordinates_24_02(fJulianCenturies)
        fMeanLongitude_Moon = MeeusAlgorithmsFormulas.PositionMoon_45_01(fJulianCenturies)
        fAscendNodeLongitude_Moon, fNutationInLongitude_Earth = MeeusAlgorithmsFormulas.NutationObliquity_21_01(fJulianCenturies, fGeometricMeanLongitude_Sun, fMeanLongitude_Moon)
        fMeanSideralTimeGreenwich, fApparentSideralTimeGreenwich = MeeusAlgorithmsFormulas.SideralTimeGreenwich_11_01(fJulianDay, fJulianCenturies, fNutationInLongitude_Earth, fMeanObliquityEcliptic_Earth)
        fMeanAnomaly_Sun = MeeusAlgorithmsFormulas.PositionMoon_45_03(fJulianCenturies)
        fEquationCenter_Sun, fTrueGeometricLongitude_Sun, fTrueAnomaly_Sun, fDistanceInUA_Sun, fDistanceInKm_Sun, fApparentGeometricLongitude_Sun = MeeusAlgorithmsFormulas.SunCoordinates_24_05(fJulianCenturies, fMeanAnomaly_Sun, fGeometricMeanLongitude_Sun, fEccentricity_Earth)
        fRightAscension_Sun = MeeusAlgorithmsFormulas.SunCoordinates_24_06(fTrueGeometricLongitude_Sun, fMeanObliquityEcliptic_Earth, fJulianCenturies)
        fDeclination_Sun = MeeusAlgorithmsFormulas.SunCoordinates_24_07(fTrueGeometricLongitude_Sun, fMeanObliquityEcliptic_Earth, fJulianCenturies)
        fApparentGeocentricLongitude_Sun, fApparentGeocentricLatitude_Sun = MeeusAlgorithmsFormulas.SunCoordinates_24_09(fGeometricMeanLongitude_Sun, 0.0)
        fMeanElongation_Moon =  MeeusAlgorithmsFormulas.PositionMoon_45_02(fJulianCenturies)
        fMeanAnomaly_Moon = MeeusAlgorithmsFormulas.PositionMoon_45_04(fJulianCenturies)
        fMeanAscendingNodeLongitude_Moon = MeeusAlgorithmsFormulas.PositionMoon_45_07(fJulianCenturies)
        fArgumentOfLatitude_Moon = MeeusAlgorithmsFormulas.PositionMoon_45_05(fJulianCenturies)
        fGeocentricLongitude_Moon, fGeocentricLatitude_Moon, fDistanceInKm_Moon = MeeusAlgorithmsFormulas.PositionMoon_45_06(fJulianCenturies, fMeanElongation_Moon, fMeanAnomaly_Sun, fMeanAnomaly_Moon, fArgumentOfLatitude_Moon, fMeanLongitude_Moon)
        fPhaseAngle_Moon = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_04(fMeanElongation_Moon, fMeanAnomaly_Moon, fMeanAnomaly_Sun)
        fIllumination_Moon = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_01(fPhaseAngle_Moon)
        fRightAscension_Moon = MeeusAlgorithmsFormulas.TransformationCoordinates_12_03(fMeanObliquityEcliptic_Earth, fGeocentricLongitude_Moon, fGeocentricLatitude_Moon)
        fDeclination_Moon = MeeusAlgorithmsFormulas.TransformationCoordinates_12_04(fMeanObliquityEcliptic_Earth, fGeocentricLongitude_Moon, fGeocentricLatitude_Moon)

        fOpticalLibrationInLongitude_Moon, fOpticalLibrationInLatitude_Moon, fSubSolarSelenographicLongitude_Moon, fSubSolarSelenographicLatitude_Moon, fSelenographicColongitude_Moon = MeeusAlgorithmsFormulas.PhysicalEphemerisMoon_51(fJulianCenturies, fApparentGeocentricLongitude_Sun, fDistanceInKm_Moon, fDistanceInKm_Sun, fMeanAnomaly_Moon, fMeanAnomaly_Sun, fMeanElongation_Moon, fGeocentricLongitude_Moon, fGeocentricLatitude_Moon, fNutationInLongitude_Earth, fMeanAscendingNodeLongitude_Moon, fArgumentOfLatitude_Moon)

        # Date
        print ""
        print "Date"
        print ""
        MeeusAlgorithmsFormulasTests.displayValue(fJulianDay, 2, "Julian Date", "JulianDay_07_01")
        MeeusAlgorithmsFormulasTests.displayValue(fDeltaT, 2, "Delta T", "DynamicalTime_09_01")
        MeeusAlgorithmsFormulasTests.displayValue(fJuliandEphemerisDay, 2, "Julian Ephemeris Day", "NutationObliquity_21_00")
        MeeusAlgorithmsFormulasTests.displayValue(fJulianCenturies, 2, "Julian Centuries", "NutationObliquity_21_00")
        MeeusAlgorithmsFormulasTests.displayValue(fJulianEphemerisCenturies, 2, "Julian Ephemeris Centuries", "NutationObliquity_21_00")
        # Time
        print ""
        print "Time"
        print ""
        MeeusAlgorithmsFormulasTests.displayValue(fMeanSideralTimeGreenwich, 2, "MeanSideral Time Greenwich", "SideralTimeGreenwich_11_01")
        MeeusAlgorithmsFormulasTests.displayValue(fApparentSideralTimeGreenwich, 2, "Apparent Sideral Time Greenwich", "SideralTimeGreenwich_11_01")
        # Sun
        print ""
        print "Sun"
        print ""
        MeeusAlgorithmsFormulasTests.displayValue(fGeometricMeanLongitude_Sun, 2, "Geometric MeanLongitude (Sun)", "SunCoordinates_24_02")
        MeeusAlgorithmsFormulasTests.displayValue(fMeanAnomaly_Sun, 2, "Mean Anomaly (Sun)", "PositionMoon_45_03")
        MeeusAlgorithmsFormulasTests.displayValue(fEquationCenter_Sun, 2, "Equation Center (Sun)", "SunCoordinates_24_05")
        MeeusAlgorithmsFormulasTests.displayValue(fTrueGeometricLongitude_Sun, 2, "True Geometric Longitude (Sun)", "SunCoordinates_24_05")
        MeeusAlgorithmsFormulasTests.displayValue(fTrueAnomaly_Sun, 2, "True Anomaly (Sun)", "SunCoordinates_24_05")
        MeeusAlgorithmsFormulasTests.displayValue(fDistanceInUA_Sun, 2, "Distance In UA (Sun)", "SunCoordinates_24_05")
        MeeusAlgorithmsFormulasTests.displayValue(fDistanceInKm_Sun, 2, "Distance In Km (Sun)", "SunCoordinates_24_05")
        MeeusAlgorithmsFormulasTests.displayValue(fApparentGeometricLongitude_Sun, 2, "Apparent Geometric Longitude (Sun)", "SunCoordinates_24_05")
        MeeusAlgorithmsFormulasTests.displayValue(fRightAscension_Sun, 2, "Right Ascension (Sun)", "SunCoordinates_24_06")
        MeeusAlgorithmsFormulasTests.displayValue(fDeclination_Sun, 2, "Declination (Sun)", "SunCoordinates_24_07")
        MeeusAlgorithmsFormulasTests.displayValue(fApparentGeocentricLongitude_Sun, 2, "Apparent Geocentric Longitude (Sun)", "SunCoordinates_24_09")
        MeeusAlgorithmsFormulasTests.displayValue(fApparentGeocentricLatitude_Sun, 2, "Apparent Geocentric Latitude (Sun)", "SunCoordinates_24_09")
        # Earth
        print ""
        print "Earth"
        print ""
        MeeusAlgorithmsFormulasTests.displayValue(fMeanObliquityEcliptic_Earth, 2, "Mean Obliquity Ecliptic (Earth)", "NutationObliquity_21_02")
        MeeusAlgorithmsFormulasTests.displayValue(fEccentricity_Earth, 2, "Eccentricity (Earth)", "SunCoordinates_24_04")
        MeeusAlgorithmsFormulasTests.displayValue(fNutationInLongitude_Earth, 2, "Nutation In Longitude (Earth)", "NutationObliquity_21_01")
        # Moon
        print ""
        print "Moon"
        print ""
        MeeusAlgorithmsFormulasTests.displayValue(fMeanLongitude_Moon, 2, "Mean Longitude (Moon)", "PositionMoon_45_01")
        MeeusAlgorithmsFormulasTests.displayValue(fAscendNodeLongitude_Moon, 2, "Ascend Node Longitude (Moon)", "NutationObliquity_21_01")
        MeeusAlgorithmsFormulasTests.displayValue(fMeanElongation_Moon, 2, "Mean Elongation (Moon)", "PositionMoon_45_02")
        MeeusAlgorithmsFormulasTests.displayValue(fMeanAnomaly_Moon, 2, "Mean Anomaly (Moon)", "PositionMoon_45_04")
        MeeusAlgorithmsFormulasTests.displayValue(fMeanAscendingNodeLongitude_Moon, 2, "Mean Ascending Node Longitude (Moon)", "PositionMoon_45_07")
        MeeusAlgorithmsFormulasTests.displayValue(fArgumentOfLatitude_Moon, 2, "Argument Of Latitude (Moon)", "PositionMoon_45_05")
        MeeusAlgorithmsFormulasTests.displayValue(fGeocentricLongitude_Moon, 2, "Geocentric Longitude (Moon)", "PositionMoon_45_06")
        MeeusAlgorithmsFormulasTests.displayValue(fGeocentricLatitude_Moon, 2, "Geocentric Latitude (Moon)", "PositionMoon_45_06")
        MeeusAlgorithmsFormulasTests.displayValue(fDistanceInKm_Moon, 2, "Distance In Km (Moon)", "PositionMoon_45_06")
        MeeusAlgorithmsFormulasTests.displayValue(fPhaseAngle_Moon, 2, "Phase Angle (Moon)", "IlluminatedFractionMoon_46_04")
        MeeusAlgorithmsFormulasTests.displayValue(fIllumination_Moon, 2, "Illumination (Moon)", "IlluminatedFractionMoon_46_01")
        MeeusAlgorithmsFormulasTests.displayValue(fRightAscension_Moon, 2, "Right Ascension (Moon)", "TransformationCoordinates_12_03")
        MeeusAlgorithmsFormulasTests.displayValue(fDeclination_Moon, 2, "Declination (Moon)", "TransformationCoordinates_12_04")
        MeeusAlgorithmsFormulasTests.displayValue(fOpticalLibrationInLongitude_Moon, 2, "Optical Libration In Longitude (Moon)", "PhysicalEphemerisMoon_51")
        MeeusAlgorithmsFormulasTests.displayValue(fOpticalLibrationInLatitude_Moon, 2, "Optical Libration In Latitude (Moon)", "PhysicalEphemerisMoon_51")
        MeeusAlgorithmsFormulasTests.displayValue(fSubSolarSelenographicLongitude_Moon, 2, "SubSolar Selenographic Longitude (Moon)", "PhysicalEphemerisMoon_51")
        MeeusAlgorithmsFormulasTests.displayValue(fSubSolarSelenographicLatitude_Moon, 2, "SubSolar Selenographic Latitude (Moon)", "PhysicalEphemerisMoon_51")
        MeeusAlgorithmsFormulasTests.displayValue(fSelenographicColongitude_Moon, 2, "Selenographic Colongitude (Moon)", "PhysicalEphemerisMoon_51")
        
        print ""

    @staticmethod
    def Test_07_JulianDay_07_01():
        # Test 07.a in Meeus book
        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(1957, 10, 4, 19, 26, 24)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fJulianDay, 2436116.31, 2, "JulianDay_07_01","1957, 10, 04, 19, 26, 24","Julian Day")
        # Test with current date (result value taken from online converter)
        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(2018, 2, 7, 15, 15, 0)
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fJulianDay, 2458157.135417, 5, "JulianDay_07_01","2018, 2, 7, 15, 15, 0","Julian Day")
        # Return result
        return sComment

    @staticmethod
    def Test_09_DynamicalTime_09_01():
        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(2018, 2, 7, 15, 15, 0)
        fDeltaT = MeeusAlgorithmsFormulas.DynamicalTime_09_01(fJulianDay)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fDeltaT, 125.7455, 4, "DynamicalTime_09_01",str(fJulianDay),"Delta T")
        # Return result
        return sComment

    @staticmethod
    def Test_11_SideralTimeGreenwich_11_01():
        fMeanSideralTimeGreenwich, fApparentSideralTimeGreenwich = MeeusAlgorithmsFormulas.SideralTimeGreenwich_11_01(2446896.30625, -0.12727430, -0.00105222222222222222222222222222, 23.443569444444444444444444444444)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMeanSideralTimeGreenwich, 128.7378734, 6, "DynamicalTime_09_01","2446895.5, -0.127296372348, -0.00105222222222222222222222222222, 23.443569444444444444444444444444","Mean Sideral Time Greenwich")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fApparentSideralTimeGreenwich, 128.7379377, 6, "DynamicalTime_09_01","2446895.5, -0.127296372348, -0.00105222222222222222222222222222, 23.443569444444444444444444444444","Apparent Sideral Time Greenwich")
        # Return result
        return sComment

    @staticmethod
    def Test_TransformationCoordinates_12_03():        
        fRightAscension = MeeusAlgorithmsFormulas.TransformationCoordinates_12_03(23.4392911, 113.205630, 6.684170)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fRightAscension, 116.317869823, 4, "TransformationCoordinates_12_03","23.4392911, 113.205630, 6.684170","Right Ascension")
        # Return result
        return sComment

    @staticmethod
    def Test_TransformationCoordinates_12_04():        
        fDeclination = MeeusAlgorithmsFormulas.TransformationCoordinates_12_04(23.4392911, 113.205630, 6.684170)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fDeclination, 28.0279470188, 4, "TransformationCoordinates_12_04","23.4392911, 113.205630, 6.684170","Declination")
        # Return result
        return sComment

    @staticmethod
    def Test_NutationObliquity_21_00():        
        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(1987, 4, 10, 0, 0, 0)
        fJuliandEphemerisDay, fJulianCenturies, fJulianEphemerisCenturies = MeeusAlgorithmsFormulas.NutationObliquity_21_00(fJulianDay)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fJuliandEphemerisDay, 2446895.5, 1, "NutationObliquity_21_00",str(fJulianDay),"Juliand Ephemeris Day")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fJulianCenturies, -0.127296372348, 11, "NutationObliquity_21_00","JulianDay_07_01(1987, 4, 10, 0, 0, 0)","Julian Centuries")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fJulianEphemerisCenturies, -0.127296344738, 11, "NutationObliquity_21_00","JulianDay_07_01(1987, 4, 10, 0, 0, 0)","Julian Centuries from Ephemeris Day")
        # Return result
        return sComment

    @staticmethod
    def Test_NutationObliquity_21_01():
        fSunGeometricMeanLongitude = MeeusAlgorithmsFormulas.SunCoordinates_24_02(-0.127296372348)
        fMoonMeanLongitude = MeeusAlgorithmsFormulas.PositionMoon_45_01(-0.127296372348)
        fMoonLongitudeAscendNode, fMoonNutationInLongitude = MeeusAlgorithmsFormulas.NutationObliquity_21_01(-0.127296372348, fSunGeometricMeanLongitude, fMoonMeanLongitude)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonLongitudeAscendNode, 11.2531, 4, "NutationObliquity_21_01","-0.127296372348, " + str(fSunGeometricMeanLongitude) + ", " + str(fMoonMeanLongitude),"Moon Longitude Ascend Node")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonNutationInLongitude, -3.788 / 3600, 4, "NutationObliquity_21_01","-0.127296372348, " + str(fSunGeometricMeanLongitude) + ", " + str(fMoonMeanLongitude),"Moon Nutation In Longitude")
        # Return result
        return sComment

    @staticmethod
    def Test_NutationObliquity_21_02():        
        fMeanObliquityEcliptic = MeeusAlgorithmsFormulas.NutationObliquity_21_02(-0.127296372348)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMeanObliquityEcliptic, 23.44094639, 5, "NutationObliquity_21_02","-0.127296372348","Mean Obliquity Ecliptic")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_02():        
        fSunGeometricMeanLongitude = MeeusAlgorithmsFormulas.SunCoordinates_24_02(-0.072183436)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunGeometricMeanLongitude, 201.80719, 5, "SunCoordinates_24_02","-0.072183436","Sun Geometric Mean Longitude")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_03():        
        fSunMeanAnomaly = MeeusAlgorithmsFormulas.SunCoordinates_24_03(-0.072183436)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunMeanAnomaly, 278.99396, 5, "SunCoordinates_24_03","-0.072183436","Sun Mean Anomaly")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_04():        
        fEarthEccentricity = MeeusAlgorithmsFormulas.SunCoordinates_24_04(-0.072183436)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fEarthEccentricity, 0.016711651, 9, "SunCoordinates_24_04","-0.072183436","Eccentricity of Earth orbit")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_05():        
        fSunEquationCenter, fSunTrueGeometricLongitude, fSunTrueAnomaly, fDistanceFromEarthToSunInUA, fDistanceFromEarthToSunInKm, fSunApparentGeometricLongitude = MeeusAlgorithmsFormulas.SunCoordinates_24_05(-0.072183436, 278.99396, 201.80719, 0.016711651)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunEquationCenter, -1.89732, 5, "SunCoordinates_24_05","-0.072183436, 278.99396, 201.80719, 0.016711651","Sun Equation of Center")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunTrueGeometricLongitude, 199.90987, 5, "SunCoordinates_24_05","-0.072183436, 278.99396, 201.80719, 0.016711651","Sun True Geometric Longitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunTrueAnomaly, (278.99396 - 1.89732), 5, "SunCoordinates_24_05","-0.072183436, 278.99396, 201.80719, 0.016711651","Sun True Anomaly")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fDistanceFromEarthToSunInUA, 0.99766, 5, "SunCoordinates_24_05","-0.072183436, 278.99396, 201.80719, 0.016711651","Distance From Earth To Sun In UA")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunApparentGeometricLongitude, 199.90894, 5, "SunCoordinates_24_05","-0.072183436, 278.99396, 201.80719, 0.016711651","Sun Apparent Geometric Longitude")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_06():        
        fSunApparentRightAscension = MeeusAlgorithmsFormulas.SunCoordinates_24_06(199.90987, 23.44023, -0.072183436)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunApparentRightAscension, -161.61918, 5, "SunCoordinates_24_06","199.90987, 23.44023, -0.072183436","Sun Apparent Right Ascension")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_07():        
        fSunApparentDeclination = MeeusAlgorithmsFormulas.SunCoordinates_24_07(199.90987, 23.44023, -0.072183436)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunApparentDeclination, -7.78507, 5, "SunCoordinates_24_07","199.90987, 23.44023, -0.072183436","Sun Apparent Declination")
        # Return result
        return sComment

    @staticmethod
    def Test_SunCoordinates_24_09():        
        fSunGeocentricLongitude, fSunGeocentricLatitude = MeeusAlgorithmsFormulas.SunCoordinates_24_09(19.907372, -0.000179)  # longitude = 22.33978 on 12APR1992 0h
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunGeocentricLongitude, 199.907372, 6, "SunCoordinates_24_09","19.907372, -0.000179","Sun Geocentric Longitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunGeocentricLatitude, 0.000179, 6, "SunCoordinates_24_09","19.907372, -0.000179","Sun Geocentric Latitude")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_01():        
        fMoonMeanLongitude = MeeusAlgorithmsFormulas.PositionMoon_45_01(-0.077221081451)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonMeanLongitude, 134.290186, 6, "PositionMoon_45_01","-0.077221081451","Moon Mean Longitude")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_02():        
        fMoonMeanElongation = MeeusAlgorithmsFormulas.PositionMoon_45_02(-0.077221081451)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonMeanElongation, 113.842309, 6, "PositionMoon_45_02","-0.077221081451","Moon Mean Elongation")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_03():        
        fSunMeanAnomaly = MeeusAlgorithmsFormulas.PositionMoon_45_03(-0.077221081451)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fSunMeanAnomaly, 97.643514, 6, "PositionMoon_45_03","-0.077221081451","Sun Mean Anomaly")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_04():        
        fMoonMeanAnomaly = MeeusAlgorithmsFormulas.PositionMoon_45_04(-0.077221081451)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonMeanAnomaly, 5.150839, 6, "PositionMoon_45_04","-0.077221081451","Moon Mean Anomaly")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_05():        
        fMoonArgumentOfLatitude = MeeusAlgorithmsFormulas.PositionMoon_45_05(-0.077221081451)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonArgumentOfLatitude, 219.889726, 6, "PositionMoon_45_05","-0.077221081451","Moon Argument Of Latitude")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_06():        
        fMoonGeocentricLongitude, fMoonGeocentricLatitude, fMoonDistanceInKm = MeeusAlgorithmsFormulas.PositionMoon_45_06(-0.077221081451, 113.842309, 97.643514, 5.150839, 219.889726, 134.290186)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonGeocentricLongitude, 133.162659, 5, "PositionMoon_45_06","-0.077221081451, 113.842309, 97.643514, 5.150839, 219.889726, 134.290186","Moon Geocentric Longitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonGeocentricLatitude, -3.229127, 6, "PositionMoon_45_06","-0.077221081451, 113.842309, 97.643514, 5.150839, 219.889726, 134.290186","Moon Geocentric Latitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonDistanceInKm, 368409.7, 1, "PositionMoon_45_06","-0.077221081451, 113.842309, 97.643514, 5.150839, 219.889726, 134.290186","Moon Distance In Km")
        # Return result
        return sComment

    @staticmethod
    def Test_PositionMoon_45_07():        
        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(1992, 4, 12, 0, 0, 0)
        fJuliandEphemerisDay, fJulianCenturies, fJulianEphemerisCenturies = MeeusAlgorithmsFormulas.NutationObliquity_21_00(fJulianDay)
        fMoonMeanAscendingNodeLongitude = MeeusAlgorithmsFormulas.PositionMoon_45_07(fJulianCenturies)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonMeanAscendingNodeLongitude, 274.400655, 6, "PositionMoon_45_07",str(fJulianCenturies),"Moon Mean Ascending Node Longitude")
        # Return result
        return sComment

    @staticmethod
    def Test_IlluminatedFractionMoon_46_01():        
        fMoonIlluminatedFraction = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_01(68.88)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonIlluminatedFraction, 0.6802, 4, "IlluminatedFractionMoon_46_01","68.88","Moon Illuminated Fraction")
        # Return result
        return sComment

    @staticmethod
    def Test_IlluminatedFractionMoon_46_04():        
        fMoonPhaseAngle = MeeusAlgorithmsFormulas.IlluminatedFractionMoon_46_04(113.8483, 5.1508, 97.6437)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonPhaseAngle, 68.88, 2, "IlluminatedFractionMoon_46_04","113.8483, 5.1508, 97.6437","Moon Phase Angle")
        # Return result
        return sComment

    @staticmethod
    def Test_PhysicalEphemerisMoon_51():  
        fJulianDay = MeeusAlgorithmsFormulas.JulianDay_07_01(1992, 4, 12, 0, 0, 0)
        fJuliandEphemerisDay, fJulianCenturies, fJulianEphemerisCenturies = MeeusAlgorithmsFormulas.NutationObliquity_21_00(fJulianDay)
        fMoonOpticalLibrationInLongitude, fMoonOpticalLibrationInLatitude, fMoonSubSolarSelenographicLongitude, fMoonSubSolarSelenographicLatitude, fMoonSelenographicColongitude = MeeusAlgorithmsFormulas.PhysicalEphemerisMoon_51(fJulianCenturies, 22.33978, 368406, 149971500, 5.150839, 97.643514, 113.842309, 133.167269, -3.229127, 0.004610, 274.400655, 219.889726)
        sComment = MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonOpticalLibrationInLongitude, -1.206, 3, "PhysicalEphemerisMoon_51",str(fJulianCenturies) + ", 22.33978, 368406, 149971500, 5.150839, 97.643514, 113.842309, 133.167269, -3.229127, 0.004610, 274.400655, 219.889726","Moon Optical Libration In Longitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonOpticalLibrationInLatitude, 4.194, 3, "PhysicalEphemerisMoon_51",str(fJulianCenturies) + ", 22.33978, 368406, 149971500, 5.150839, 97.643514, 113.842309, 133.167269, -3.229127, 0.004610, 274.400655, 219.889726","Moon Optical Libration In Latitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonSubSolarSelenographicLongitude, 67.89, 2, "PhysicalEphemerisMoon_51",str(fJulianCenturies) + ", 22.33978, 368406, 149971500, 5.150839, 97.643514, 113.842309, 133.167269, -3.229127, 0.004610, 274.400655, 219.889726","Moon Sub Solar Selenographic Longitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonSubSolarSelenographicLatitude, 1.46, 2, "PhysicalEphemerisMoon_51",str(fJulianCenturies) + ", 22.33978, 368406, 149971500, 5.150839, 97.643514, 113.842309, 133.167269, -3.229127, 0.004610, 274.400655, 219.889726","Moon Sub Solar Selenographic Latitude")
        sComment += "\n" + MeeusAlgorithmsFormulasTests._FormatResultAsText(fMoonSelenographicColongitude, 22.11, 2, "PhysicalEphemerisMoon_51",str(fJulianCenturies) + ", 22.33978, 368406, 149971500, 5.150839, 97.643514, 113.842309, 133.167269, -3.229127, 0.004610, 274.400655, 219.889726","Moon Selenographic Colongitude")
        # Return result
        return sComment
     
#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class CommonAstroFormulaes.py
# 
import math

class CommonAstroFormulaes():
    @staticmethod
    def getObliqEclipInDegForDateValue(fDateValue):
        return 23.4393 - 3.563 * math.pow(10, -7) * fDateValue
    @staticmethod
    def getSideralTimeForTime(sTime, fSunTrueAnoInDeg, fArgPerihelInDeg, fLongitude):
        # sTime qs HHMMSS
        iHour = int(sTime[0:2])
        iMinutes = int(sTime[2:4])
        iSeconds = int(sTime[2:4])
        # Sideral Time
        fLocalSideralTimeInHour = (fSunTrueAnoInDeg + fArgPerihelInDeg + 180.0 + (float(iHour) + float(iMinutes) / 60.0 + float(iSeconds) / 3600.0) * 15.0 + fLongitude) / 15.0
        fLocalSideralTimeInHour = fLocalSideralTimeInHour % 24.0
        return fLocalSideralTimeInHour
    @staticmethod
    def getSideralTimeForSlot(iTimeSlot, fSunTrueAnoInDeg, fArgPerihelInDeg, fLongitude):
        # Sideral Time
        return ((fSunTrueAnoInDeg + fArgPerihelInDeg + 180.0 + (float(iTimeSlot % 24)) * 15.0 + fLongitude) / 15.0) % 24
    @staticmethod
    def getAzimutFromEquatCoord(fRAInDeg, fDecInDeg, fLatitudeInDeg, fLocalSideralTimeInHour):
        fHA = fLocalSideralTimeInHour*15.0 - fRAInDeg
        while fHA > 180.0:
            fHA = fHA - 360.0
        while fHA < 180.0:
            fHA = fHA + 360.0

        fx = math.cos(math.radians(fHA)) * math.cos(math.radians(fDecInDeg))
        fy = math.sin(math.radians(fHA)) * math.cos(math.radians(fDecInDeg))
        fz = math.sin(math.radians(fDecInDeg))

        fxhor = fx * math.sin(math.radians(fLatitudeInDeg)) - fz * math.cos(math.radians(fLatitudeInDeg))
        fyhor = fy
        fzhor = fx * math.cos(math.radians(fLatitudeInDeg)) + fz * math.sin(math.radians(fLatitudeInDeg))

        return math.degrees(math.atan2( fyhor, fxhor )) + 180.0

    @staticmethod
    def getAltitudeFromEquatCoord(fRAInDeg, fDecInDeg, fLatitudeInDeg, fLocalSideralTimeInHour):
        fHA = fLocalSideralTimeInHour*15.0 - fRAInDeg
        while fHA > 180.0:
            fHA = fHA - 360.0
        while fHA < 180.0:
            fHA = fHA + 360.0

        fx = math.cos(math.radians(fHA)) * math.cos(math.radians(fDecInDeg))
        fy = math.sin(math.radians(fHA)) * math.cos(math.radians(fDecInDeg))
        fz = math.sin(math.radians(fDecInDeg))

        fxhor = fx * math.sin(math.radians(fLatitudeInDeg)) - fz * math.cos(math.radians(fLatitudeInDeg))
        fyhor = fy
        fzhor = fx * math.cos(math.radians(fLatitudeInDeg)) + fz * math.sin(math.radians(fLatitudeInDeg))

        return math.degrees(math.atan2( fzhor, math.sqrt(fxhor*fxhor+fyhor*fyhor) ))
    

    
    @staticmethod
    def getHMSFromDeg(fDeg):
        fValue = ((fDeg + 360.0) % 360.0) / 360.0 * 86400.0
        fHour = math.floor(fValue / 3600.0)
        fValue = fValue - ( 3600.0 * fHour )
        fMinutes = math.floor(fValue / 60.0)
        fValue = fValue - ( 60.0 * fMinutes )
        fSeconds = round(fValue)
        return str(int(fHour)) + "h " + ("00" + str(int(fMinutes)))[-2:] + "' " + ("00" + str(int(fSeconds)))[-2:] + '"'

    
    @staticmethod
    def getDMSFromDeg(fDeg):
        if fDeg >= 0:
            fSign = 1
            fUnsignedValue = fDeg
        else:
            fSign = -1
            fUnsignedValue = - fDeg
        fValue = ((fUnsignedValue + 360.0) % 360.0) / 360.0 * 360 * 60 * 60
        fDegrees = math.floor(fValue / 3600.0)
        fValue = fValue - ( 3600.0 * fDegrees )
        fMinutes = math.floor(fValue / 60.0)
        fValue = fValue - ( 60.0 * fMinutes )
        fSeconds = round(fValue)
        if fSeconds == 60:
            fSeconds = 0
            fMinutes = fMinutes + 1
            if fMinutes == 60:
                fMinutes =0
                fDegrees = fDegrees + 1
        if fSign == 1:
            return str(int(fDegrees)) + "d " + ("00" + str(int(fMinutes)))[-2:] + "' " + ("00" + str(int(fSeconds)))[-2:] + '"'
        else:
            return "-" + str(int(fDegrees)) + "d " + ("00" + str(int(fMinutes)))[-2:] + "' " + ("00" + str(int(fSeconds)))[-2:] + '"'

    @staticmethod
    def getDegFromHMS(sHHMMSS):
        if len(sHHMMSS) == 0.0:
            return ""
        else:
            iHour = int(sHHMMSS[0:2])
            iMinutes = int(sHHMMSS[2:4])
            iSeconds = int(sHHMMSS[4:6])
            fValue = float(iHour * 3600 + iMinutes * 60 + iSeconds) / 86400.0 * 360.0
            return fValue
        
    @staticmethod
    def FormatDegreesTo360(fValueInDeg):     # return degrees between 0 and 360
        return math.fmod(math.fmod(fValueInDeg, 360.0) + 360.0, 360.0)
        
    @staticmethod
    def FormatRadiansTo2Pi(fValueInRad):     # return degrees between 0 and 2xpi
        return math.fmod(math.fmod(fValueInRad, ( 2.0 * math.pi)) + ( 2.0 * math.pi), ( 2.0 * math.pi))
        
    @staticmethod
    def ConvertUAToKM(fDistanceInUA):        # return distance in Km
        return 149597871.0 * fDistanceInUA

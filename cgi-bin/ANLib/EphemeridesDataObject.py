#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class EphemeridesDataObject
# 
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace


class EphemeridesDataObject(toolObjectSerializable):
    def __init__(self, sID, sType, sCategory, sName):
        toolObjectSerializable.__init__(self)
        self._sID = sID
        self._sType = sType
        self._sCategory = sCategory
        self._sName = sName
        self._Azimut = {}        #
        self._Altitude = {}      #
        self._RightAscension = {}        #
        self._Declination = {}      #
        self._Distance = {}      #
        self._MeanLong = {} #
        self._Colongitude = {}   #
        self._SelenographicLongitude = {}   #
        self._SelenographicLatitude = {}   #
        self._Phase = {}
        self._Illumination = {}
    def setDataForSlot(self, iSlot, fAzimut, fAltitude, fRightAscension, fDeclination, fDistance, fMeanLong, fColongitude = 0.0, fSelenographicLongitude = 0.0, fSelenographicLatitude = 0.0, fPhase = 0.0, fIllumination = 0.0):
        self._Azimut[str(iSlot)] = fAzimut
        self._Altitude[str(iSlot)] = fAltitude
        self._RightAscension[str(iSlot)] = fRightAscension
        self._Declination[str(iSlot)] = fDeclination
        self._Distance[str(iSlot)] = fDistance
        self._MeanLong[str(iSlot)] = fMeanLong
        self._Colongitude[str(iSlot)] = fColongitude
        self._SelenographicLongitude[str(iSlot)] = fSelenographicLongitude
        self._SelenographicLatitude[str(iSlot)] = fSelenographicLatitude
        self._Phase[str(iSlot)] = fPhase
        self._Illumination[str(iSlot)] = fIllumination
    def getID(self): return self._sID
    def getType(self): return self._sType
    def getCategory(self): return self._sCategory
    def getName(self): return self._sName
    def getMinAzimut(self, iStartSlot, iEndSlot):
        iMinAzimut = -1      # rise azimut
        for iSlot in range(iStartSlot, iEndSlot):
            if self._Altitude[str(iSlot)] > 0.0 and iMinAzimut < 0: iMinAzimut = int(round(self._Azimut[str(iSlot)]))
        return iMinAzimut
    def getCulminAzimut(self, iStartSlot, iEndSlot): 
        iCulminAzimut = -1   # culmination azimut
        iCulminAltitude = -1 # culmination altitude
        for iSlot in range(iStartSlot, iEndSlot):
            if int(round(self._Altitude[str(iSlot)])) > iCulminAltitude and self._Altitude[str(iSlot)] > 0.0: 
                iCulminAltitude = int(round(self._Altitude[str(iSlot)])) 
                iCulminAzimut = int(round(self._Azimut[str(iSlot)]))
        return iCulminAzimut
    def getCulminAltitude(self, iStartSlot, iEndSlot): 
        iCulminAzimut = -1   # culmination azimut
        iCulminAltitude = -1 # culmination altitude
        for iSlot in range(iStartSlot, iEndSlot):
            if int(round(self._Altitude[str(iSlot)])) > iCulminAltitude and self._Altitude[str(iSlot)] > 0.0: 
                iCulminAltitude = int(round(self._Altitude[str(iSlot)])) 
                iCulminAzimut = int(round(self._Azimut[str(iSlot)]))
        return iCulminAltitude
    def getMaxAzimut(self, iStartSlot, iEndSlot): 
        iMaxAzimut = -1      # set azimut
        iCulminAzimut = -1   # culmination azimut
        iCulminAltitude = -1 # culmination altitude
        for iSlot in range(iStartSlot, iEndSlot):
            if int(round(self._Altitude[str(iSlot)])) > iCulminAltitude and self._Altitude[str(iSlot)] > 0.0: 
                iCulminAltitude = int(round(self._Altitude[str(iSlot)])) 
                iCulminAzimut = int(round(self._Azimut[str(iSlot)]))
            if self._Altitude[str(iSlot)] < 0.0 and iCulminAltitude > 0 and iMaxAzimut < 0: iMaxAzimut = int(round(self._Azimut[str(iSlot)]))
        return iMaxAzimut
    def getAzimutForSlot(self, iSlot): return self._Azimut[str(iSlot)]
    def getAltitudeForSlot(self, iSlot): return self._Altitude[str(iSlot)]
    def getRightAscensionForSlot(self, iSlot): return self._RightAscension[str(iSlot)]
    def getDeclinationForSlot(self, iSlot): return self._Declination[str(iSlot)]
    def getDistanceForSlot(self, iSlot): return self._Distance[str(iSlot)]
    def getApparentDiameterInArcSecForSlot(self, iSlot): 
        if self._sID == "Mercury":
            return 6.74 / self._Distance[str(iSlot)]
        elif self._sID == "Venus":
            return 16.92 / self._Distance[str(iSlot)]
        elif self._sID == "Mars":
            return 9.36 / self._Distance[str(iSlot)]
        elif self._sID == "Jupiter":
            return 196.94 / self._Distance[str(iSlot)]
        elif self._sID == "Saturn":
            return 165.6 / self._Distance[str(iSlot)]
        elif self._sID == "Uranus":
            return 65.8 / self._Distance[str(iSlot)]
        elif self._sID == "Neptune":
            return 62.2 / self._Distance[str(iSlot)]
        elif self._sID == "Moon":
            return 1873.7 * 60.0 / self._Distance[str(iSlot)]
        else:
            return 0.0
    def getMeanLongForSlot(self, iSlot): return self._MeanLong[str(iSlot)] % 360
    def getColongitudeForSlot(self, iSlot): return self._Colongitude[str(iSlot)]
    def getSelenographicLongitudeForSlot(self, iSlot): return self._SelenographicLongitude[str(iSlot)]
    def getSelenographicLatitudeForSlot(self, iSlot): return self._SelenographicLatitude[str(iSlot)]
    def getPhaseForSlot(self, iSlot): return self._Phase[str(iSlot)]
    def getIlluminationForSlot(self, iSlot): return self._Illumination[str(iSlot)]
    
        
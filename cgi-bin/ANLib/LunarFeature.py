#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class LunarFeature
# 
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace


class LunarFeature(toolObjectSerializable):
    def __init__(self, iIndex, sID, sName, fLongitude, fLongitudeMin, fLongitudeMax, fLatitude, sIsFavourite, sType, fHeight, fDiameter, fDepth, fLength, fBreadth, sRukl):
        toolObjectSerializable.__init__(self)
        self._sID = sID
        self._sName = sName
        self._fLongitude = fLongitude
        self._fLongitudeMin = fLongitudeMin
        self._fLongitudeMax = fLongitudeMax
        self._fLatitude = fLatitude
        self._iIndex = iIndex
        self._bIsFavourite = (sIsFavourite == "Yes")
        self._sType = sType
        self._fHeight = fHeight
        self._fDiameter = fDiameter
        self._fDepth = fDepth
        self._fLength = fLength
        self._fBreadth = fBreadth 
        self._sRukl = sRukl
    def getID(self): return self._sID
    def setID(self, sID): self._sID = sID
    def getName(self): return self._sName
    def setName(self, sName): self._sName = sName
    def getIndex(self): return self._iIndex
    def getLongitude(self): return self._fLongitude
    def setLongitude(self, fLongitude): self._fLongitude = fLongitude
    def getLongitudeMin(self): return self._fLongitudeMin
    def setLongitudeMin(self, fLongitudeMin): self._fLongitudeMin = fLongitudeMin
    def getLongitudeMax(self): return self._fLongitudeMax
    def setLongitudeMax(self, fLongitudeMax): self._fLongitudeMax = fLongitudeMax
    def getLatitude(self): return self._fLatitude
    def setLatitude(self, fLatitude): self._fLatitude = fLatitude
    def getIsFavourite(self): return self._bIsFavourite
    def setIsFavourite(self, bIsFavourite): self._bIsFavourite = bIsFavourite
    def getType(self): return self._sType
    def setType(self, sType): self._sType = sType
    def getHeight(self): return self._fHeight
    def setHeight(self, fHeigh): self._fHeight = fHeight
    def getDiameter(self): return self._fDiameter
    def setDiameter(self, fDiameter): self._fDiameter = fDiameter
    def getDepth(self): return self._fDepth
    def setDepth(self, fDepth): self._fDepth = fDepth
    def getLength(self): return self._fLength
    def setLength(self, fLength): self._fLength = fLength
    def getBreadth(self): return self._fBreadth
    def setBreadth(self, fBreadth): self._fBreadth = fBreadth
    def getRukl(self): return self._sRukl
    def setRukl(self, sRukl): self._sRukl = sRukl

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class SkyObject
# 
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes
#from toolTrace import toolTrace


class SkyObject(toolObjectSerializable):
    def __init__(self, iIndex, sCategory, sID, sType, sName, sRA, fDec, sPictureName, sComment1, sComment2, sIsFavourite):
        toolObjectSerializable.__init__(self)
        self._sCategory = sCategory
        self._iIndex = iIndex
        self._sID = sID
        self._sType = sType
        self._sName = sName
        self._fRA = CommonAstroFormulaes.getDegFromHMS(sRA)
        self._fDec = fDec
        self._sPictureName = sPictureName
        self._sComment1 = sComment1
        self._sComment2 = sComment2
        self._bIsFavourite = (sIsFavourite == "Yes")
    def getCategory(self): return self._sCategory
    def setCategory(self, sCategory): self._sCategory = sCategory
    def getIndex(self): return self._iIndex
    def getID(self): return self._sID
    def setID(self, sID): self._sID = sID
    def getType(self): return self._sType
    def setType(self, sType): self._sType = sType
    def getName(self): return self._sName
    def setName(self, sName): self._sName = sName
    def getRA(self): return self._fRA
    def setRA(self, fRA): self._fRA = fRA
    def getDec(self): return self._fDec
    def setDec(self, fDec): self._fDec = fDec
    def getPictureName(self): return self._sPictureName
    def setPictureName(self, sPictureName): self._sPictureName = sPictureName
    def getComment1(self): return self._sComment1
    def setComment1(self, sComment): self._sComment1 = sComment
    def getComment2(self): return self._sComment2
    def setComment2(self, sComment): self._sComment2 = sComment
    def getIsFavourite(self): return self._bIsFavourite
    def setIsFavourite(self, bIsFavourite): self._bIsFavourite = bIsFavourite

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ObstructedSkyArea
# 
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace


class ParametersObstructedSkyArea(toolObjectSerializable):
    def __init__(self, sComment, tColor, fAzimutMinInDeg, fAzimutMaxInDeg, fAltitudeMinInDeg, fAltitudeMaxInDeg):
        toolObjectSerializable.__init__(self)
        self._sComment = sComment
        self._tColor = tColor
        self._fAzimutMinInDeg = fAzimutMinInDeg
        self._fAzimutMaxInDeg = fAzimutMaxInDeg
        self._fAltitudeMinInDeg = fAltitudeMinInDeg
        self._fAltitudeMaxInDeg = fAltitudeMaxInDeg
    def getComment(self): return self._sComment
    def setComment(self, sComment): self._sComment = sComment
    def getColor(self): return self._tColor
    def setColor(self, tColor): self._tColor = tColor
    def getAzimutMinInDeg(self): return self._fAzimutMinInDeg
    def setAzimutMinInDeg(self, fAzimutMinInDeg): self._fAzimutMinInDeg = fAzimutMinInDeg
    def getAzimutMaxInDeg(self): return self._fAzimutMaxInDeg
    def setAzimutMaxInDeg(self, fAzimutMaxInDeg): self._fAzimutMaxInDeg = fAzimutMaxInDeg
    def getAltitudeMinInDeg(self): return self._fAltitudeMinInDeg
    def setAltitudeMinInDeg(self, fAltitudeMinInDeg): self._fAltitudeMinInDeg = fAltitudeMinInDeg
    def getAltitudeMaxInDeg(self): return self._fAltitudeMaxInDeg
    def setAltitudeMaxInDeg(self, fAltitudeMaxInDeg): self._fAltitudeMaxInDeg = fAltitudeMaxInDeg

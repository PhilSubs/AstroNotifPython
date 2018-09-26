#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersLocalization
# 
from toolObjectSerializable import toolObjectSerializable
from Tools import Tools
from toolJSON import toolJSON
#from toolTrace import toolTrace


class ParametersLocalization(toolObjectSerializable):
    def __init__(self, dicJSONData, sLanguageCode):
        toolObjectSerializable.__init__(self)
        self._sActiveLanguageCode = sLanguageCode
        self._tLabels = None
        self.__initWithData(dicJSONData)
        
    def setActiveLanguage(self, sLanguageCode): self._sActiveLanguageCode = sLanguageCode
    def getActiveLanguage(self): return self._sActiveLanguageCode

    def _convertForPrint (self, sText): 
        try:
            sReturn = sText.decode("utf-8")
        except:
            sReturn = sText
        return sReturn

    def getLabel(self, sCode): 
        if sCode[0:7] == "[label]":
            if sCode[7:] in self._tLabels:
                return self._tLabels[sCode[7:]]
            else:
                return sCode
        elif sCode in self._tLabels:
            return self._tLabels[sCode]
        else:
            return sCode
        
    def __initWithData(self, dicJSONData):
        # init properties
        self._tLabels = {}
        for iId in range (0, len(dicJSONData[self._sActiveLanguageCode])):
            sKeyLabel = list(dicJSONData[self._sActiveLanguageCode].keys())[iId]
            self._tLabels[sKeyLabel] = dicJSONData[self._sActiveLanguageCode][sKeyLabel]
            

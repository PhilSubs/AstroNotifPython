#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersLocalization
# 
from ParametersJsonGeneric import ParametersJsonGeneric

class ParametersLocalization(ParametersJsonGeneric):
    def __init__(self, sJsonFileName, sLanguageCode):
        ParametersJsonGeneric.__init__(self, sJsonFileName)
        self._sActiveLanguageCode = sLanguageCode

    def setActiveLanguage(self, sLanguageCode): self._sActiveLanguageCode = sLanguageCode
    def getActiveLanguage(self): return self._sActiveLanguageCode
        
    def getLabel(self, sCode, bNotifyMissing = True): 
        # Remove the indicator [Label] from the code requested if any
        if sCode[0:7] == "[label]":
            sCodeSearched = sCode[7:]
        else:
            sCodeSearched = sCode
        # Add language code in the key to find the value with the generic parameter class
        sCodeSearched = self._sActiveLanguageCode + "." + sCodeSearched
        # Find the value fomr the JSON file... if missing, the reauested code will be returned
        try:
            sReturn = ParametersJsonGeneric.get(self, sCodeSearched, bNotifyMissing)
        except:
            sReturn = sCode
        # returns result
        return sReturn

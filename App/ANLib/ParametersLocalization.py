#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersLocalization
# 
import json
from toolObjectSerializable import toolObjectSerializable
from Tools import Tools
#from toolTrace import toolTrace


class ParametersLocalization(toolObjectSerializable):
    def __init__(self, sLanguageCode):
        toolObjectSerializable.__init__(self)
        self._sLanguageCode = sLanguageCode
        self._tLabels = {}
        
        self.__loadFromFile()
        
    def getActiveLanguage(self): return self._sLanguageCode
    def getLabel(self, sCode): 
        sReturn = sCode
        if sCode[0:7] == "[label]":
            if sCode[7:] in self._tLabels:
                sReturn = self._tLabels[sCode[7:]]
#                print "Label   " + sCode + "   --> " + sReturn + "  (" + self._sLanguageCode + ")"
            else:
                print "Label # " + sCode + "   missing !  (" + self._sLanguageCode + ")"
        elif sCode in self._tLabels:
            sReturn = self._tLabels[sCode]
#            print "Label   " + sCode + "   --> " + sReturn + "  (" + self._sLanguageCode + ")"
        else:
            print "Label ! " + sCode + "   not translated !  (" + self._sLanguageCode + ")"

        if type(sReturn) is unicode:
                sReturn.encode("iso-8859-1" )

        return sReturn
    
    def __loadFromFile(self):
        # load parameters file
        with open('parameters_Localization.json', 'r') as f:
             data = json.load(f)
        # init properties
        for iId in range (0, len(data[self._sLanguageCode])):
            sKeyLabel = list(data[self._sLanguageCode].keys())[iId]
            self._tLabels[sKeyLabel] = data[self._sLanguageCode][sKeyLabel]
            

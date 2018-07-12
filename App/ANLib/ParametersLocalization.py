#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersLocalization
# 
import json
from toolObjectSerializable import toolObjectSerializable
from Tools import Tools
from toolJSON import toolJSON
#from toolTrace import toolTrace


class ParametersLocalization(toolObjectSerializable):
    def __init__(self, sLanguageCode):
        toolObjectSerializable.__init__(self)
        self._sLanguageCode = sLanguageCode
        self._tLabels = {}
        
        self.__loadFromFile()
    def _convertForPrint (self, sText): 
#        if isinstance(sText, unicode):
        try:
#            print ">>>try>>>>>> "+ sText[0:4]
            sReturn = str(sText.encode("iso-8859-1" ))#.encode("utf-8" )
        except:
#            print ">>>except>>> "+ sText[0:4]
            sReturn = sText
#        else:
#            print ">>>>>>>>>>>> "+ sText[0:3]
#            sReturn = sText
        return sReturn
    def getActiveLanguage(self): return self._sLanguageCode
    def getLabel(self, sCode): 
        sReturn = sCode
        if sCode[0:7] == "[label]":
            if sCode[7:] in self._tLabels:
                sReturn = self._tLabels[sCode[7:]]
            else:
                print "Label # " + self._convertForPrint(sCode) + "   missing !  (" + self._sLanguageCode + ")"
        elif sCode in self._tLabels:
            sReturn = self._tLabels[sCode]
#        else:
#            print "Label ! " + self._convertForPrint(sCode) + "   not translated !  (" + self._sLanguageCode + ")"

        if type(sReturn) is unicode:
            sReturn = self._convertForPrint(sReturn)

        return sReturn
    
    def __loadFromFile(self):
        # load parameters file
        data = toolJSON.getContent('parameters_Localization.json')
        
#        with open('parameters_Localization.json', 'r') as f:
#             data = json.load(f)
        # init properties
        for iId in range (0, len(data[self._sLanguageCode])):
            sKeyLabel = list(data[self._sLanguageCode].keys())[iId]
            self._tLabels[sKeyLabel] = data[self._sLanguageCode][sKeyLabel]
            

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersJsonGenericObjects
# 
from toolJSON import toolJSON
from ParametersJsonGenericObject import ParametersJsonGenericObject

class ParametersJsonGenericObjects:
    def __init__(self, sJsonFileName):
        self._jsonFileName = sJsonFileName
        self._dicObjects = {}
        self._buffer = {}
        self._dicAttributes = {}
        self._dicIDToIndex = {}
        dicJSONData = toolJSON.getContent(self._jsonFileName)
            
        for iId in range (0, len(dicJSONData)):
            sObjectKey = list(dicJSONData.keys())[iId]
            aNewObject = ParametersJsonGenericObject(dicJSONData[sObjectKey])
            self._dicObjects[sObjectKey] = aNewObject
            self._dicIDToIndex[dicJSONData[sObjectKey]["ID"]] = sObjectKey

            
    def getCount(self): return len(self._dicObjects)

    def getObjectByID(self, sID): return self._dicObjects[self._dicIDToIndex[sID]]

    def getObjectByIndex(self, iIndex): 
        sId = str(iIndex)
        if sId in self._dicObjects:
            return self._dicObjects[sId]
        else:
            raise NameError('Error in getObjectByIndex: nothing found while searching key ' + sId + '/' + str(len(self._dicObjects)) + '.')
    
    def set(self, sCode, aValue, sType):
        sDic = {}
        sDic["value"] = aValue
        sDic["type"] = sType
        self._dicAttributes[sCode] = sDic
    
    def get(self, sCode): 
        if not self._buffer.get(sCode) is None :
            aReturnValue = self._buffer[sCode]
        else:
            try:
                sDic = self._dicAttributes[sCode]
                sType = sDic["type"]
            except:
                sDic = None
                sType = None
                print "   >>>> ERROR >>>>  attribute " + sCode + " not found !!!"
            if not sDic is None:
               if sType == "tuple":
                   aReturnValue = eval(sDic["value"])
               else:
                   aReturnValue = sDic["value"]
               self._buffer[sCode] = aReturnValue
        return aReturnValue

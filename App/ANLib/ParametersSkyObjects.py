#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class SkyObjects
# 
from ParametersSkyObject import ParametersSkyObject
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace

class ParametersSkyObjects(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._dicSkyObjects = {}
        self._dicLinkIDWithIndex = {}
        self._iCountDeepSky = 0
        self.__initWithData(dicJSONData)

    def getCount(self): return len(self._dicSkyObjects)
    def getCountDeepSky(self): return self._iCountDeepSky
    def getSkyObjectByID(self, sID): return self._dicSkyObjects[self._dicLinkIDWithIndex[sID]]
    def getSkyObjectByID1(self, sID): return self._dicSkyObjects.get(sID)
    def getSkyObjectByIndex(self, iIndex): 
        sId = str(iIndex+1)
        if sId in self._dicSkyObjects:
            return self._dicSkyObjects[sId]
        else:
            raise NameError('Error in getSkyObjectByIndex: nothing found while searching key ' + sId + '/' + str(len(self._dicSkyObjects)) + '.')
    def getSkyObjectByIndex1(self, iIndex): 
        x = 0
        while (x < len(self._dicSkyObjects) and  self._dicSkyObjects.values()[x].getIndex() != iIndex):
            x = x + 1
        if x < len(self._dicSkyObjects):
            return self._dicSkyObjects.values()[x]
        else:
            raise NameError('Error in getSkyObjectByIndex: ' + str(x) + ' value reached while searching index ' + str(iIndex) + '/' + str(len(self._dicSkyObjects)) + '.')
            
    def __initWithData(self, dicJSONData):
        # init Sky Objects array of SkyObject objects
        for iId in range (0, len(dicJSONData)):
            sObjectKey = list(dicJSONData.keys())[iId]
            newSkyObject = ParametersSkyObject(iId, dicJSONData[sObjectKey]["Category"], dicJSONData[sObjectKey]["ID"], dicJSONData[sObjectKey]["Type"], dicJSONData[sObjectKey]["Name"], dicJSONData[sObjectKey]["RA"], dicJSONData[sObjectKey]["Dec"], dicJSONData[sObjectKey]["PictureName"], dicJSONData[sObjectKey]["Comment1"], dicJSONData[sObjectKey]["Comment2"], dicJSONData[sObjectKey]["Distance"], dicJSONData[sObjectKey]["DistanceUnit"], dicJSONData[sObjectKey]["DimensionX"], dicJSONData[sObjectKey]["DimensionXUnit"], dicJSONData[sObjectKey]["DimensionY"], dicJSONData[sObjectKey]["DimensionYUnit"], dicJSONData[sObjectKey]["ApparentMagnitude"], dicJSONData[sObjectKey]["IsFavourite"], dicJSONData[sObjectKey]["NotifyWhenObservable"] )
#            self._dicSkyObjects[dicJSONData[sObjectKey]["ID"]] = newSkyObject
            self._dicSkyObjects[sObjectKey] = newSkyObject
            self._dicLinkIDWithIndex[dicJSONData[sObjectKey]["ID"]] = sObjectKey
            if dicJSONData[sObjectKey]["Category"] == "DeepSky": self._iCountDeepSky = self._iCountDeepSky + 1
            

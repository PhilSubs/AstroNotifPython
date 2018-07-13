#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class SkyObjects
# 
from SkyObject import SkyObject
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace

class SkyObjects(toolObjectSerializable):
    def __init__(self, dataSkyObjects):
        toolObjectSerializable.__init__(self)
        self._dicSkyObjects = {}
        self._dicLinkIDWithIndex = {}
        self._iCountDeepSky = 0
        self.__initSkyObjects(dataSkyObjects)
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
    def __initSkyObjects(self, dataSkyObjects):
        # init Sky Objects array of SkyObject objects
        for iId in range (0, len(dataSkyObjects)):
            sObjectKey = list(dataSkyObjects.keys())[iId]
            newSkyObject = SkyObject(iId, dataSkyObjects[sObjectKey]["Category"], dataSkyObjects[sObjectKey]["ID"], dataSkyObjects[sObjectKey]["Type"], dataSkyObjects[sObjectKey]["Name"], dataSkyObjects[sObjectKey]["RA"], dataSkyObjects[sObjectKey]["Dec"], dataSkyObjects[sObjectKey]["PictureName"], dataSkyObjects[sObjectKey]["Comment1"], dataSkyObjects[sObjectKey]["Comment2"], dataSkyObjects[sObjectKey]["Distance"], dataSkyObjects[sObjectKey]["DistanceUnit"], dataSkyObjects[sObjectKey]["DimensionX"], dataSkyObjects[sObjectKey]["DimensionXUnit"], dataSkyObjects[sObjectKey]["DimensionY"], dataSkyObjects[sObjectKey]["DimensionYUnit"], dataSkyObjects[sObjectKey]["ApparentMagnitude"], dataSkyObjects[sObjectKey]["IsFavourite"] )
#            self._dicSkyObjects[dataSkyObjects[sObjectKey]["ID"]] = newSkyObject
            self._dicSkyObjects[sObjectKey] = newSkyObject
            self._dicLinkIDWithIndex[dataSkyObjects[sObjectKey]["ID"]] = sObjectKey
            if dataSkyObjects[sObjectKey]["Category"] == "DeepSky": self._iCountDeepSky = self._iCountDeepSky + 1
            

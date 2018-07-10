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
        self._iCountDeepSky = 0
        self.__initSkyObjects(dataSkyObjects)
    def getCount(self): return len(self._dicSkyObjects)
    def getCountDeepSky(self): return self._iCountDeepSky
    def getSkyObjectByID(self, sID): return self._dicSkyObjects.get(sID)
    def getSkyObjectByIndex(self, iIndex): 
        x = 0
        while (x < len(self._dicSkyObjects) and  self._dicSkyObjects.values()[x].getIndex() != iIndex):
            x = x + 1
        if x < len(self._dicSkyObjects):
            return self._dicSkyObjects.values()[x]
        else:
            raise NameError('Error in getSkyObjectByIndex: ' + str(x) + ' value reached while searching index ' + str(iIndex) + '/' + str(len(self._dicSkyObjects)) + '.')
    def __initSkyObjects(self, dataSkyObjects):
        # init Sky Objects array of SkyObject objects
        for x in range(0,  len(dataSkyObjects)):
            newSkyObject = SkyObject(x, dataSkyObjects[x]["Category"], dataSkyObjects[x]["ID"], dataSkyObjects[x]["Type"], dataSkyObjects[x]["Name"], dataSkyObjects[x]["RA"], dataSkyObjects[x]["Dec"], dataSkyObjects[x]["PictureName"], dataSkyObjects[x]["Comment1"], dataSkyObjects[x]["Comment2"], dataSkyObjects[x]["Distance"], dataSkyObjects[x]["DistanceUnit"], dataSkyObjects[x]["DimensionX"], dataSkyObjects[x]["DimensionXUnit"], dataSkyObjects[x]["DimensionY"], dataSkyObjects[x]["DimensionYUnit"], dataSkyObjects[x]["ApparentMagnitude"], dataSkyObjects[x]["IsFavourite"] )
            self._dicSkyObjects[dataSkyObjects[x]["ID"]] = newSkyObject
            if dataSkyObjects[x]["Category"] == "DeepSky": self._iCountDeepSky = self._iCountDeepSky + 1
            

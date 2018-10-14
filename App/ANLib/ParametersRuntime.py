#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Parameters
# 
from ParametersJsonGeneric import ParametersJsonGeneric

class ParametersRuntime(ParametersJsonGeneric):
    def __init__(self, sJsonFileName):
        ParametersJsonGeneric.__init__(self, sJsonFileName)
        self._Place = None

    def getPlace(self): return self._Place
    def setPlace(self, aPlace): self._Place = aPlace
    

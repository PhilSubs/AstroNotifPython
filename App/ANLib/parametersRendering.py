#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersRendering
# 
import json
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace


class ParametersRendering(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._tcolorVisibilityFlagsNotObservable = (0,0,0)
        self._tcolorVisibilityFlagsAtLEastOneDayObservable = (0,0,0)
        self._tcolorVisibilityFlagsObservable = (0,0,0)
        self._tcolorHeliocentricGraphBackground = (0,0,0,0)
        self._tcolorHeliocentricGraphLines = (0,0,0,0)
        self._tcolorHeliocentricGraphSun = (0,0,0,0)
        self._tcolorHeliocentricGraphEarth = (0,0,0,0)
        self._tcolorHeliocentricGraphPlanet = (0,0,0,0)
        self._tcolorMoonMiniMapBackground = (0,0,0,0)
        self._tcolorMoonMiniMapBorder = (0,0,0,0)
        self._tcolorMoonMiniMapLight = (0,0,0,0)
        self._tcolorMoonMiniMapDark = (0,0,0,0)
        self.__loadFromFile()
    def getGlobalParam(self): return self._sGlobalParam
    def __loadFromFile(self):
        # load parameters file
        with open('parameters_Rendering.json', 'r') as f:
             data = json.load(f)
        # init properties
        self._tcolorVisibilityFlagsNotObservable = data["colorVisibilityFlagsNotObservable"]
        self._tcolorVisibilityFlagsAtLEastOneDayObservable = data["colorVisibilityFlagsAtLEastOneDayObservable"]
        self._tcolorVisibilityFlagsObservable = data["colorVisibilityFlagsObservable"]
        self._tcolorHeliocentricGraphBackground = data["colorHeliocentricGraphBackground"]
        self._tcolorHeliocentricGraphLines = data["colorHeliocentricGraphLines"]
        self._tcolorHeliocentricGraphSun = data["colorHeliocentricGraphSun"]
        self._tcolorHeliocentricGraphEarth = data["colorHeliocentricGraphEarth"]
        self._tcolorHeliocentricGraphPlanet = data["colorHeliocentricGraphPlanet"]
        self._tcolorMoonMiniMapBackground = data["colorMoonMiniMapBackground"]
        self._tcolorMoonMiniMapBorder = data["colorMoonMiniMapBorder"]
        self._tcolorMoonMiniMapLight = data["colorMoonMiniMapLight"]
        self._tcolorMoonMiniMapDark = data["colorMoonMiniMapDark"]

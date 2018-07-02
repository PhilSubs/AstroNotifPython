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
        self._tcolorVisibilityFlagsNotObservable = eval(data["colorVisibilityFlagsNotObservable"])
        self._tcolorVisibilityFlagsAtLEastOneDayObservable = eval(data["colorVisibilityFlagsAtLEastOneDayObservable"])
        self._tcolorVisibilityFlagsObservable = eval(data["colorVisibilityFlagsObservable"])
        self._tcolorHeliocentricGraphBackground = eval(data["colorHeliocentricGraphBackground"])
        self._tcolorHeliocentricGraphLines = eval(data["colorHeliocentricGraphLines"])
        self._tcolorHeliocentricGraphSun = eval(data["colorHeliocentricGraphSun"])
        self._tcolorHeliocentricGraphEarth = eval(data["colorHeliocentricGraphEarth"])
        self._tcolorHeliocentricGraphPlanet = eval(data["colorHeliocentricGraphPlanet"])
        self._tcolorMoonMiniMapBackground = eval(data["colorMoonMiniMapBackground"])
        self._tcolorMoonMiniMapBorder = eval(data["colorMoonMiniMapBorder"])
        self._tcolorMoonMiniMapLight = eval(data["colorMoonMiniMapLight"])
        self._tcolorMoonMiniMapDark = eval(data["colorMoonMiniMapDark"])

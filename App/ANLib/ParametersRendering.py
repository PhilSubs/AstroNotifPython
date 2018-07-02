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
        self._tcolorSunAltitudeMoreThan18DegBelow = (0,0,0)
        self._tcolorSunAltitude12To18DegBelow = (0,0,0)
        self._tcolorSunAltitude06To12DegBelow = (0,0,0)
        self._tcolorSunAltitude00To06DegBelow = (0,0,0)
        self._tcolorSunAltitude00To06DegAbove = (0,0,0)
        self._tcolorSunAltitude06To12DegAbove = (0,0,0)
        self._tcolorSunAltitudeMoreThan12DegAbove = (0,0,0)
        self._tcolorObjectVisibilityStatusBelow = (0,0,0)
        self._tcolorObjectVisibilityStatusHidden = (0,0,0)
        self._tcolorObjectVisibilityStatusVeryLow = (0,0,0)
        self._tcolorObjectVisibilityStatusLow = (0,0,0)
        self._tcolorObjectVisibilityStatusDifficult = (0,0,0)
        self._tcolorObjectVisibilityStatusImpossible = (0,0,0)
        self._tcolorObjectVisibilityStatusGood = (0,0,0)
        self._tcolorObjectVisibilityStatusOther = (0,0,0)
        
        self.__loadFromFile()
        
        
    def getColorVisibilityFlagsNotObservable(self): return self._tcolorVisibilityFlagsNotObservable
    def getColorVisibilityFlagsAtLEastOneDayObservable(self): return self._tcolorVisibilityFlagsAtLEastOneDayObservable
    def getColorVisibilityFlagsObservable(self): return self._tcolorVisibilityFlagsObservable
    def getColorHeliocentricGraphBackground(self): return self._tcolorHeliocentricGraphBackground
    def getColorHeliocentricGraphLines(self): return self._tcolorHeliocentricGraphLines
    def getColorHeliocentricGraphSun(self): return self._tcolorHeliocentricGraphSun
    def getColorHeliocentricGraphEarth(self): return self._tcolorHeliocentricGraphEarth
    def getColorHeliocentricGraphPlanet(self): return self._tcolorHeliocentricGraphPlanet
    def getColorMoonMiniMapBackground(self): return self._tcolorMoonMiniMapBackground
    def getColorMoonMiniMapBorder(self): return self._tcolorMoonMiniMapBorder
    def getColorMoonMiniMapLight(self): return self._tcolorMoonMiniMapLight
    def getColorMoonMiniMapDark(self): return self._tcolorMoonMiniMapDark
    def getColorSunAltitudeMoreThan18DegBelow(self): return self._tcolorSunAltitudeMoreThan18DegBelow
    def getColorSunAltitude12To18DegBelow(self): return self._tcolorSunAltitude12To18DegBelow
    def getColorSunAltitude06To12DegBelow(self): return self._tcolorSunAltitude06To12DegBelow
    def getColorSunAltitude00To06DegBelow(self): return self._tcolorSunAltitude00To06DegBelow
    def getColorSunAltitude00To06DegAbove(self): return self._tcolorSunAltitude00To06DegAbove
    def getColorSunAltitude06To12DegAbove(self): return self._tcolorSunAltitude06To12DegAbove
    def getColorSunAltitudeMoreThan12DegAbove(self): return self._tcolorSunAltitudeMoreThan12DegAbove
    def getColorObjectVisibilityStatusBelow(self): return self._tcolorObjectVisibilityStatusBelow
    def getColorObjectVisibilityStatusHidden(self): return self._tcolorObjectVisibilityStatusHidden
    def getColorObjectVisibilityStatusVeryLow(self): return self._tcolorObjectVisibilityStatusVeryLow
    def getColorObjectVisibilityStatusLow(self): return self._tcolorObjectVisibilityStatusLow
    def getColorObjectVisibilityStatusDifficult(self): return self._tcolorObjectVisibilityStatusDifficult
    def getColorObjectVisibilityStatusImpossible(self): return self._tcolorObjectVisibilityStatusImpossible
    def getColorObjectVisibilityStatusGood(self): return self._tcolorObjectVisibilityStatusGood
    def getColorObjectVisibilityStatusOther(self): return self._tcolorObjectVisibilityStatusOther
    
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
        self._tcolorSunAltitudeMoreThan18DegBelow = eval(data["colorSunAltitudeMoreThan18DegBelow"])
        self._tcolorSunAltitude12To18DegBelow = eval(data["colorSunAltitude12To18DegBelow"])
        self._tcolorSunAltitude06To12DegBelow = eval(data["colorSunAltitude06To12DegBelow"])
        self._tcolorSunAltitude00To06DegBelow = eval(data["colorSunAltitude00To06DegBelow"])
        self._tcolorSunAltitude00To06DegAbove = eval(data["colorSunAltitude00To06DegAbove"])
        self._tcolorSunAltitude06To12DegAbove = eval(data["colorSunAltitude06To12DegAbove"])
        self._tcolorSunAltitudeMoreThan12DegAbove = eval(data["colorSunAltitudeMoreThan12DegAbove"])
        self._tcolorObjectVisibilityStatusBelow = eval(data["colorObjectVisibilityStatusBelow"])
        self._tcolorObjectVisibilityStatusHidden = eval(data["colorObjectVisibilityStatusHidden"])
        self._tcolorObjectVisibilityStatusVeryLow = eval(data["colorObjectVisibilityStatusVeryLow"])
        self._tcolorObjectVisibilityStatusLow = eval(data["colorObjectVisibilityStatusLow"])
        self._tcolorObjectVisibilityStatusDifficult = eval(data["colorObjectVisibilityStatusDifficult"])
        self._tcolorObjectVisibilityStatusImpossible = eval(data["colorObjectVisibilityStatusImpossible"])
        self._tcolorObjectVisibilityStatusGood = eval(data["colorObjectVisibilityStatusGood"])
        self._tcolorObjectVisibilityStatusOther = eval(data["colorObjectVisibilityStatusOther"])

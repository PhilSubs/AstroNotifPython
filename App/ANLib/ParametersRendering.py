#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersRendering
# 
import json
from toolObjectSerializable import toolObjectSerializable
from Tools import Tools
#from toolTrace import toolTrace


class ParametersRendering(toolObjectSerializable):
    def __init__(self):
        toolObjectSerializable.__init__(self)
        self._tcolorVisibilityFlags = {}
        self._tcolorHeliocentricGraph = {}
        self._tcolorMoonMiniMap = {}
        self._tcolorSunAltitude = {}
        self._tcolorObjectVisibilityStatus = {}
        self._tcolorLunarFeatureVisibility = {}
        self._tStyles = {}
        
        self.__loadFromFile()
        
        
    def getColorVisibilityFlags(self, sCode): return self._tcolorVisibilityFlags[sCode]
    def getColorHeliocentricGraph(self, sCode): return self._tcolorHeliocentricGraph[sCode]
    def getColorMoonMiniMap(self, sCode): return self._tcolorMoonMiniMap[sCode]
    def getColorSunAltitude(self, sCode): return self._tcolorSunAltitude[sCode]
    def getColorObjectVisibilityStatus(self, sCode): return self._tcolorObjectVisibilityStatus[sCode]
    def getColorLunarFeatureVisibility(self, sCode): return self._tcolorLunarFeatureVisibility[sCode]
    def getStyles(self, sCode): return self._tStyles[sCode]
    
    def __loadFromFile(self):
        # load parameters file
        with open('parameters_Rendering.json', 'r') as f:
             data = json.load(f)
        # init properties
        self._tcolorVisibilityFlags['NotObservable'] = eval(data["colorVisibilityFlagsNotObservable"])
        self._tcolorVisibilityFlags['AtLEastOneDayObservable'] = eval(data["colorVisibilityFlagsAtLEastOneDayObservable"])
        self._tcolorVisibilityFlags['Observable'] = eval(data["colorVisibilityFlagsObservable"])
        self._tcolorHeliocentricGraph['Background'] = eval(data["colorHeliocentricGraphBackground"])
        self._tcolorHeliocentricGraph['Lines'] = eval(data["colorHeliocentricGraphLines"])
        self._tcolorHeliocentricGraph['Sun'] = eval(data["colorHeliocentricGraphSun"])
        self._tcolorHeliocentricGraph['Earth'] = eval(data["colorHeliocentricGraphEarth"])
        self._tcolorHeliocentricGraph['Planet'] = eval(data["colorHeliocentricGraphPlanet"])
        self._tcolorMoonMiniMap['Background'] = eval(data["colorMoonMiniMapBackground"])
        self._tcolorMoonMiniMap['Border'] = eval(data["colorMoonMiniMapBorder"])
        self._tcolorMoonMiniMap['Light'] = eval(data["colorMoonMiniMapLight"])
        self._tcolorMoonMiniMap['Dark'] = eval(data["colorMoonMiniMapDark"])
        self._tcolorSunAltitude['MoreThan18DegBelow'] = eval(data["colorSunAltitudeMoreThan18DegBelow"])
        self._tcolorSunAltitude['12To18DegBelow'] = eval(data["colorSunAltitude12To18DegBelow"])
        self._tcolorSunAltitude['06To12DegBelow'] = eval(data["colorSunAltitude06To12DegBelow"])
        self._tcolorSunAltitude['00To06DegBelow'] = eval(data["colorSunAltitude00To06DegBelow"])
        self._tcolorSunAltitude['00To06DegAbove'] = eval(data["colorSunAltitude00To06DegAbove"])
        self._tcolorSunAltitude['06To12DegAbove'] = eval(data["colorSunAltitude06To12DegAbove"])
        self._tcolorSunAltitude['MoreThan12DegAbove'] = eval(data["colorSunAltitudeMoreThan12DegAbove"])
        self._tcolorObjectVisibilityStatus['Below'] = eval(data["colorObjectVisibilityStatusBelow"])
        self._tcolorObjectVisibilityStatus['Hidden'] = eval(data["colorObjectVisibilityStatusHidden"])
        self._tcolorObjectVisibilityStatus['VeryLow'] = eval(data["colorObjectVisibilityStatusVeryLow"])
        self._tcolorObjectVisibilityStatus['Low'] = eval(data["colorObjectVisibilityStatusLow"])
        self._tcolorObjectVisibilityStatus['Difficult'] = eval(data["colorObjectVisibilityStatusDifficult"])
        self._tcolorObjectVisibilityStatus['Impossible'] = eval(data["colorObjectVisibilityStatusImpossible"])
        self._tcolorObjectVisibilityStatus['Good'] = eval(data["colorObjectVisibilityStatusGood"])
        self._tcolorObjectVisibilityStatus['Unknown'] = eval(data["colorObjectVisibilityStatusUnknown"])
        self._tcolorLunarFeatureVisibility['colorLunarFeatureVisibilityNotObservable'] = eval(data["colorLunarFeatureVisibilityNotObservable"])
        self._tcolorLunarFeatureVisibility['colorLunarFeatureVisibilityGood'] = eval(data["colorLunarFeatureVisibilityGood"])
        self._tStyles['DefaultFontSize'] = data["styleDefaultFontSize"]
        self._tStyles['DefaultFontDirectory'] = data["styleDefaultFontDirectory"]
        self._tStyles['DefaultFont'] = Tools.get_ResourceSubfolder_path("Fonts") + data["styleDefaultFont"]
        self._tStyles['DefaultFontColor'] = eval(data["styleDefaultFontColor"])
        self._tStyles['DefaultBackColor'] = eval(data["styleDefaultBackColor"])
        self._tStyles['DefaultTopMargin'] = data["styleDefaultTopMargin"]
        self._tStyles['DefaultBottomMargin'] = data["styleDefaultBottomMargin"]
        self._tStyles['DefaultPaddingTopBottom'] = data["styleDefaultPaddingTopBottom"]
        self._tStyles['RowHeaderDateFontSize'] = data["styleRowHeaderDateFontSize"]
        self._tStyles['RowHeaderTimeFontSize'] = data["styleRowHeaderTimeFontSize"]
        self._tStyles['ObjectNameFontSize'] = data["styleObjectNameFontSize"]
        self._tStyles['ObjectDataFontSize'] = data["styleObjectDataFontSize"]
        self._tStyles['ObjectAdditionalDailyDataFontSize'] = data["styleObjectAdditionalDailyDataFontSize"]
        self._tStyles['SectionTitleH0FontSize'] = data["styleSectionTitleH0FontSize"]
        self._tStyles['SectionTitleH0BackColor'] = eval(data["styleSectionTitleH0BackColor"])
        self._tStyles['SectionTitleH0FontColor'] = eval(data["styleSectionTitleH0FontColor"])
        self._tStyles['SectionTitleH0TopMargin'] = data["styleSectionTitleH0TopMargin"]
        self._tStyles['SectionTitleH0BottomMargin'] = data["styleSectionTitleH0BottomMargin"]
        self._tStyles['SectionTitleH0PaddingTopBottom'] = data["styleSectionTitleH0PaddingTopBottom"]
        self._tStyles['SectionTitleH1FontSize'] = data["styleSectionTitleH1FontSize"]
        self._tStyles['SectionTitleH1BackColor'] = eval(data["styleSectionTitleH1BackColor"])
        self._tStyles['SectionTitleH1FontColor'] = eval(data["styleSectionTitleH1FontColor"])
        self._tStyles['SectionTitleH1TopMargin'] = data["styleSectionTitleH1TopMargin"]
        self._tStyles['SectionTitleH1BottomMargin'] = data["styleSectionTitleH1BottomMargin"]
        self._tStyles['SectionTitleH1PaddingTopBottom'] = data["styleSectionTitleH1PaddingTopBottom"]
        self._tStyles['SectionTitleH2FontSize'] = data["styleSectionTitleH2FontSize"]
        self._tStyles['SectionTitleH2FontColor'] = eval(data["styleSectionTitleH2FontColor"])
        self._tStyles['SectionTitleH2TopMargin'] = data["styleSectionTitleH2TopMargin"]
        self._tStyles['SectionTitleH2BottomMargin'] = data["styleSectionTitleH2BottomMargin"]
        self._tStyles['SectionTitleH2PaddingTopBottom'] = data["styleSectionTitleH2PaddingTopBottom"]
        self._tStyles['LunarFeatureNameFontSize'] = data["styleLunarFeatureNameFontSize"]
        self._tStyles['LunarFeatureDataFontSize'] = data["styleLunarFeatureDataFontSize"]
        self._tStyles['LunarFeatureDataFont'] = Tools.get_ResourceSubfolder_path("Fonts") + data["styleLunarFeatureDataFont"]

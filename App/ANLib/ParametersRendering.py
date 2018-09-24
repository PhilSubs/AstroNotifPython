#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersRendering
# 
from toolObjectSerializable import toolObjectSerializable
from Tools import Tools
from toolJSON import toolJSON
#from toolTrace import toolTrace


class ParametersRendering(toolObjectSerializable):
    def __init__(self, dicJSONData):
        toolObjectSerializable.__init__(self)
        self._tcolorVisibilityFlags = None
        self._tcolorHeliocentricGraph = None
        self._tcolorMoonMiniMap = None
        self._tcolorSunAltitude = None
        self._tcolorObjectVisibilityStatus = None
        self._tcolorLunarFeatureVisibility = None
        self._tDisplay = None
        self._tStyles = None
        self.__initWithData(dicJSONData)
        
    def getColorVisibilityFlags(self, sCode): return self._tcolorVisibilityFlags[sCode]
    def getColorHeliocentricGraph(self, sCode): return self._tcolorHeliocentricGraph[sCode]
    def getColorMoonMiniMap(self, sCode): return self._tcolorMoonMiniMap[sCode]
    def getColorSunAltitude(self, sCode): return self._tcolorSunAltitude[sCode]
    def getColorObjectVisibilityStatus(self, sCode): return self._tcolorObjectVisibilityStatus[sCode]
    def getColorLunarFeatureVisibility(self, sCode): return self._tcolorLunarFeatureVisibility[sCode]
    def getStyles(self, sCode): return self._tStyles[sCode]
    def getDisplay(self, sCode): return self._tDisplay[sCode]
    
    def __initWithData(self, dicJSONData):
        # Color Visibility
        self._tcolorVisibilityFlags = {}
        self._tcolorVisibilityFlags['NotObservable'] = eval(dicJSONData["colorVisibilityFlagsNotObservable"])
        self._tcolorVisibilityFlags['AtLEastOneDayObservable'] = eval(dicJSONData["colorVisibilityFlagsAtLEastOneDayObservable"])
        self._tcolorVisibilityFlags['Observable'] = eval(dicJSONData["colorVisibilityFlagsObservable"])
        # Color Heliocentric Graph
        self._tcolorHeliocentricGraph = {}
        self._tcolorHeliocentricGraph['Background'] = eval(dicJSONData["colorHeliocentricGraphBackground"])
        self._tcolorHeliocentricGraph['Lines'] = eval(dicJSONData["colorHeliocentricGraphLines"])
        self._tcolorHeliocentricGraph['Sun'] = eval(dicJSONData["colorHeliocentricGraphSun"])
        self._tcolorHeliocentricGraph['Earth'] = eval(dicJSONData["colorHeliocentricGraphEarth"])
        self._tcolorHeliocentricGraph['Planet'] = eval(dicJSONData["colorHeliocentricGraphPlanet"])
        # Color Moon minimap
        self._tcolorMoonMiniMap = {}
        self._tcolorMoonMiniMap['Background'] = eval(dicJSONData["colorMoonMiniMapBackground"])
        self._tcolorMoonMiniMap['Border'] = eval(dicJSONData["colorMoonMiniMapBorder"])
        self._tcolorMoonMiniMap['Light'] = eval(dicJSONData["colorMoonMiniMapLight"])
        self._tcolorMoonMiniMap['Dark'] = eval(dicJSONData["colorMoonMiniMapDark"])
        # Color Sun Altitude
        self._tcolorSunAltitude = {}
        self._tcolorSunAltitude['MoreThan18DegBelow'] = eval(dicJSONData["colorSunAltitudeMoreThan18DegBelow"])
        self._tcolorSunAltitude['12To18DegBelow'] = eval(dicJSONData["colorSunAltitude12To18DegBelow"])
        self._tcolorSunAltitude['06To12DegBelow'] = eval(dicJSONData["colorSunAltitude06To12DegBelow"])
        self._tcolorSunAltitude['00To06DegBelow'] = eval(dicJSONData["colorSunAltitude00To06DegBelow"])
        self._tcolorSunAltitude['00To06DegAbove'] = eval(dicJSONData["colorSunAltitude00To06DegAbove"])
        self._tcolorSunAltitude['06To12DegAbove'] = eval(dicJSONData["colorSunAltitude06To12DegAbove"])
        self._tcolorSunAltitude['MoreThan12DegAbove'] = eval(dicJSONData["colorSunAltitudeMoreThan12DegAbove"])
        # Color Object Visibility
        self._tcolorObjectVisibilityStatus = {}
        self._tcolorObjectVisibilityStatus['Below'] = eval(dicJSONData["colorObjectVisibilityStatusBelow"])
        self._tcolorObjectVisibilityStatus['Hidden'] = eval(dicJSONData["colorObjectVisibilityStatusHidden"])
        self._tcolorObjectVisibilityStatus['VeryLow'] = eval(dicJSONData["colorObjectVisibilityStatusVeryLow"])
        self._tcolorObjectVisibilityStatus['Low'] = eval(dicJSONData["colorObjectVisibilityStatusLow"])
        self._tcolorObjectVisibilityStatus['Difficult'] = eval(dicJSONData["colorObjectVisibilityStatusDifficult"])
        self._tcolorObjectVisibilityStatus['DifficultMoonlight'] = eval(dicJSONData["colorObjectVisibilityStatusDifficultMoonlight"])
        self._tcolorObjectVisibilityStatus['Impossible'] = eval(dicJSONData["colorObjectVisibilityStatusImpossible"])
        self._tcolorObjectVisibilityStatus['Good'] = eval(dicJSONData["colorObjectVisibilityStatusGood"])
        self._tcolorObjectVisibilityStatus['Unknown'] = eval(dicJSONData["colorObjectVisibilityStatusUnknown"])
        # Color Lunar Feature Visibility
        self._tcolorLunarFeatureVisibility = {}
        self._tcolorLunarFeatureVisibility['TerminatorNearButNotObservable'] = eval(dicJSONData["colorLunarFeatureVisibilityTerminatorNearButNotObservable"])
        self._tcolorLunarFeatureVisibility['Good'] = eval(dicJSONData["colorLunarFeatureVisibilityGood"])
        self._tcolorLunarFeatureVisibility['SunBelowHorizon'] = eval(dicJSONData["colorLunarFeatureVisibilitySunBelowHorizon"])
        self._tcolorLunarFeatureVisibility['SunTooHigh'] = eval(dicJSONData["colorLunarFeatureVisibilitySunTooHigh"])
        self._tcolorLunarFeatureVisibility['MoonBelowHorizon'] = eval(dicJSONData["colorLunarFeatureVisibilityMoonBelowHorizon"])
        self._tcolorLunarFeatureVisibility['MoonHidden'] = eval(dicJSONData["colorLunarFeatureVisibilityMoonHidden"])
        self._tcolorLunarFeatureVisibility['MoonImpossible'] = eval(dicJSONData["colorLunarFeatureVisibilityMoonImpossible"])
        # Display
        self._tDisplay = {}
        self._tDisplay['Language'] = dicJSONData["displayLanguage"]
        self._tDisplay['BitmapType'] = dicJSONData["displayBitmapType"]
        self._tDisplay['BitmapExtension'] = dicJSONData["displayBitmapExtension"]
        self._tDisplay['VisibilityTableAsBitmap'] = dicJSONData["displayVisibilityTableAsBitmap"]
        self._tDisplay['NumberOfSlotsForMoon'] = dicJSONData["displayNumberOfSlotsForMoon"]
        self._tDisplay['NumberOfSlotsForMoonFeatures'] = dicJSONData["displayNumberOfSlotsForMoonFeatures"]
        self._tDisplay['NumberOfSlotsForPlanets'] = dicJSONData["displayNumberOfSlotsForPlanets"]
        self._tDisplay['NumberOfSlotsForDeepSky'] = dicJSONData["displayNumberOfSlotsForDeepSky"]
        self._tDisplay['NumberOfMinutesPerSlot'] = dicJSONData["displayNumberOfMinutesPerSlot"]
        self._tDisplay['DaySlotForDataInfo'] = dicJSONData["displayDaySlotForDataInfo"]
        self._tDisplay['MaxAltitudeForObjectLow'] = dicJSONData["displayMaxAltitudeForObjectLow"]
        self._tDisplay['MaxAltitudeForObjectVeryLow'] = dicJSONData["displayMaxAltitudeForObjectVeryLow"]
        self._tDisplay['MaxSunAltitudeForObservableDeepSky'] = dicJSONData["displayMaxSunAltitudeForObservableDeepSky"]
        self._tDisplay['MaxSunAltitudeForObservableBrightObjects'] = dicJSONData["displayMaxSunAltitudeForObservableBrightObjects"]
        self._tDisplay['MaxSunAltitudeForDifficultBrightObjects'] = dicJSONData["displayMaxSunAltitudeForDifficultBrightObjects"]
        self._tDisplay['MaxSunAltitudeFoImpossibleBrightObjects'] = dicJSONData["displayMaxSunAltitudeFoImpossibleBrightObjects"]
        self._tDisplay['MaxSunAltitudeForObservableMediumObjects'] = dicJSONData["displayMaxSunAltitudeForObservableMediumObjects"]
        self._tDisplay['MaxSunAltitudeForDifficultMediumObjects'] = dicJSONData["displayMaxSunAltitudeForDifficultMediumObjects"]
        # Text Styles
        self._tStyles = {}
        self._tStyles['DefaultFontSize'] = dicJSONData["styleDefaultFontSize"]
        self._tStyles['DefaultFontDirectory'] = dicJSONData["styleDefaultFontDirectory"]
        self._tStyles['DefaultFont'] = dicJSONData["styleDefaultFont"]
        self._tStyles['DefaultFontColor'] = eval(dicJSONData["styleDefaultFontColor"])
        self._tStyles['DefaultBackColor'] = eval(dicJSONData["styleDefaultBackColor"])
        self._tStyles['DefaultTopMargin'] = dicJSONData["styleDefaultTopMargin"]
        self._tStyles['DefaultBottomMargin'] = dicJSONData["styleDefaultBottomMargin"]
        self._tStyles['DefaultPaddingTopBottom'] = dicJSONData["styleDefaultPaddingTopBottom"]
        self._tStyles['GMTWarningFontSize'] = dicJSONData["styleGMTWarningFontSize"]
        self._tStyles['GMTWarningFont'] = dicJSONData["styleGMTWarningFont"]
        self._tStyles['LegendFontSize'] = dicJSONData["styleLegendFontSize"]
        self._tStyles['LegendFont'] = dicJSONData["styleLegendFont"]
        self._tStyles['RowHeaderDateFontSize'] = dicJSONData["styleRowHeaderDateFontSize"]
        self._tStyles['RowHeaderDateFont'] = dicJSONData["styleRowHeaderDateFont"]
        self._tStyles['RowHeaderTimeFontSize'] = dicJSONData["styleRowHeaderTimeFontSize"]
        self._tStyles['ObjectNameFontSize'] = dicJSONData["styleObjectNameFontSize"]
        self._tStyles['ObjectNameFontColor'] = eval(dicJSONData["styleObjectNameFontColor"])
        self._tStyles['ObjectNameNotifiedFontSize'] = dicJSONData["styleObjectNameNotifiedFontSize"]
        self._tStyles['ObjectNameNotifiedFontColor'] = eval(dicJSONData["styleObjectNameNotifiedFontColor"])
        self._tStyles['ObjectDataFontSize'] = dicJSONData["styleObjectDataFontSize"]
        self._tStyles['ObjectAdditionalDailyDataFontSize'] = dicJSONData["styleObjectAdditionalDailyDataFontSize"]
        self._tStyles['SectionTitleH0FontSize'] = dicJSONData["styleSectionTitleH0FontSize"]
        self._tStyles['SectionTitleH0BackColor'] = eval(dicJSONData["styleSectionTitleH0BackColor"])
        self._tStyles['SectionTitleH0FontColor'] = eval(dicJSONData["styleSectionTitleH0FontColor"])
        self._tStyles['SectionTitleH0TopMargin'] = dicJSONData["styleSectionTitleH0TopMargin"]
        self._tStyles['SectionTitleH0BottomMargin'] = dicJSONData["styleSectionTitleH0BottomMargin"]
        self._tStyles['SectionTitleH0PaddingTopBottom'] = dicJSONData["styleSectionTitleH0PaddingTopBottom"]
        self._tStyles['SectionTitleH1FontSize'] = dicJSONData["styleSectionTitleH1FontSize"]
        self._tStyles['SectionTitleH1BackColor'] = eval(dicJSONData["styleSectionTitleH1BackColor"])
        self._tStyles['SectionTitleH1FontColor'] = eval(dicJSONData["styleSectionTitleH1FontColor"])
        self._tStyles['SectionTitleH1TopMargin'] = dicJSONData["styleSectionTitleH1TopMargin"]
        self._tStyles['SectionTitleH1BottomMargin'] = dicJSONData["styleSectionTitleH1BottomMargin"]
        self._tStyles['SectionTitleH1PaddingTopBottom'] = dicJSONData["styleSectionTitleH1PaddingTopBottom"]
        self._tStyles['SectionTitleH2FontSize'] = dicJSONData["styleSectionTitleH2FontSize"]
        self._tStyles['SectionTitleH2FontColor'] = eval(dicJSONData["styleSectionTitleH2FontColor"])
        self._tStyles['SectionTitleH2TopMargin'] = dicJSONData["styleSectionTitleH2TopMargin"]
        self._tStyles['SectionTitleH2BottomMargin'] = dicJSONData["styleSectionTitleH2BottomMargin"]
        self._tStyles['SectionTitleH2PaddingTopBottom'] = dicJSONData["styleSectionTitleH2PaddingTopBottom"]
        self._tStyles['LunarFeatureNameFontSize'] = dicJSONData["styleLunarFeatureNameFontSize"]
        self._tStyles['LunarFeatureNameFontColor'] = eval(dicJSONData["styleLunarFeatureNameFontColor"])
        self._tStyles['LunarFeatureNameNotifiedFontSize'] = dicJSONData["styleLunarFeatureNameNotifiedFontSize"]
        self._tStyles['LunarFeatureNameNotifiedFontColor'] = eval(dicJSONData["styleLunarFeatureNameNotifiedFontColor"])
        self._tStyles['LunarFeatureDataFontSize'] = dicJSONData["styleLunarFeatureDataFontSize"]
        self._tStyles['LunarFeatureDataFont'] = dicJSONData["styleLunarFeatureDataFont"]
        self._tStyles['BitmapHeaderH0FontSize'] = dicJSONData["styleBitmapHeaderH0FontSize"]
        self._tStyles['BitmapHeaderH0BackColor'] = eval(dicJSONData["styleBitmapHeaderH0BackColor"])
        self._tStyles['BitmapHeaderH0FontColor'] = eval(dicJSONData["styleBitmapHeaderH0FontColor"])
        self._tStyles['BitmapHeaderH0TopMargin'] = dicJSONData["styleBitmapHeaderH0TopMargin"]
        self._tStyles['BitmapHeaderH0BottomMargin'] = dicJSONData["styleBitmapHeaderH0BottomMargin"]
        self._tStyles['BitmapHeaderH0PaddingTopBottom'] = dicJSONData["styleBitmapHeaderH0PaddingTopBottom"]
        self._tStyles['BitmapHeaderH1FontSize'] = dicJSONData["styleBitmapHeaderH1FontSize"]
        self._tStyles['BitmapHeaderH1BackColor'] = eval(dicJSONData["styleBitmapHeaderH1BackColor"])
        self._tStyles['BitmapHeaderH1FontColor'] = eval(dicJSONData["styleBitmapHeaderH1FontColor"])
        self._tStyles['BitmapHeaderH1TopMargin'] = dicJSONData["styleBitmapHeaderH1TopMargin"]
        self._tStyles['BitmapHeaderH1BottomMargin'] = dicJSONData["styleBitmapHeaderH1BottomMargin"]
        self._tStyles['BitmapHeaderH1PaddingTopBottom'] = dicJSONData["styleBitmapHeaderH1PaddingTopBottom"]
        self._tStyles['BitmapHeaderH2FontSize'] = dicJSONData["styleBitmapHeaderH2FontSize"]
        self._tStyles['BitmapHeaderH2BackColor'] = eval(dicJSONData["styleBitmapHeaderH2BackColor"])
        self._tStyles['BitmapHeaderH2FontColor'] = eval(dicJSONData["styleBitmapHeaderH2FontColor"])
        self._tStyles['BitmapHeaderH2TopMargin'] = dicJSONData["styleBitmapHeaderH2TopMargin"]
        self._tStyles['BitmapHeaderH2BottomMargin'] = dicJSONData["styleBitmapHeaderH2BottomMargin"]
        self._tStyles['BitmapHeaderH2PaddingTopBottom'] = dicJSONData["styleBitmapHeaderH2PaddingTopBottom"]

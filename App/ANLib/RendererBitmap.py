#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class RendererBitmap
# 
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes
from MeeusAlgorithms import MeeusAlgorithms
from Tools import Tools
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime
import platform


class RendererBitmap(toolObjectSerializable):
    iLeftLabelWidthInPx = 100
    iHourSlotWidthInPx = 16
    iAltitudeRowHeight = 3
    #sFontDefaultName = "arial.ttf"
    iFontDefaultSize = 16
    iTableMarginLeft = 0
    iTableWidthObjectLabel = 300
    iTableVisibilityFlagWidth = 10
    iTableSpaceBetweenLabelAndGraph = 5
    iTableSpaceBetweenDays = 1
    iTableMarginTop = 20
    iTableHeaderRowHeight = 16
    iTableHeaderRowInterline = 5
    iTableObjectRowGraphAdditionalDataHeight = 16
    iSectionTitleHeightH1 = 40
    iSectionTitleHeightH2 = 24


    def __init__(self, oParameters, sRelativeFolderForBitmaps, sURLFolderForBitmaps, bForFavouriteOnly = False):
        toolObjectSerializable.__init__(self)
        self._bForFavouriteOnly = bForFavouriteOnly
        self._sRelativeFolderForBitmaps = sRelativeFolderForBitmaps
        self._sURLFolderForBitmaps = sURLFolderForBitmaps
        self._oParameters = oParameters
        self._oParametersRuntime = self._oParameters.Runtime()
        self._oParametersRendering = self._oParameters.Rendering()
        self._dicMemBuffer = {}
        self._dicRuntimeParamMemBuffer = {}
        self._dicRenderingParamMemBuffer = {}
        self._dicLocalizationMemBuffer = {}
        self.initBuffers()

    def initBuffers(self):
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.MoreThan18DegBelow"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.MoreThan18DegBelow')
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.12To18DegBelow"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.12To18DegBelow')
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.06To12DegBelow"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.06To12DegBelow')
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.00To06DegBelow"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.00To06DegBelow')
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.00To06DegAbove"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.00To06DegAbove')
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.06To12DegAbove"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.06To12DegAbove')
        self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.MoreThan12DegAbove"] = self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.MoreThan12DegAbove')
        self._dicRenderingParamMemBuffer["LineColorForStatusBelow"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Below")
        self._dicRenderingParamMemBuffer["LineColorForStatusHidden"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Hidden")
        self._dicRenderingParamMemBuffer["LineColorForStatusVeryLow"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.VeryLow")
        self._dicRenderingParamMemBuffer["LineColorForStatusLow"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Low")
        self._dicRenderingParamMemBuffer["LineColorForStatusDifficult"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Difficult")
        self._dicRenderingParamMemBuffer["LineColorForStatusDifficultMoonlight"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.DifficultMoonlight")
        self._dicRenderingParamMemBuffer["LineColorForStatusImpossible"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Impossible")
        self._dicRenderingParamMemBuffer["LineColorForStatusGood"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Good")
        self._dicRenderingParamMemBuffer["LineColorForStatusUnknown"] = self._oParametersRendering.get("ObjectVisibilityGraph.LineColorForStatus.Unknown")
        self._dicRenderingParamMemBuffer["Styles.Default.FontSize"] = self._oParametersRendering.get('Styles.Default.FontSize')
        self._dicRenderingParamMemBuffer["Styles.Default.FontDirectory"] = self._oParametersRendering.get('Styles.Default.FontDirectory')
        self._dicRenderingParamMemBuffer["Styles.Default.FontColor"] = self._oParametersRendering.get('Styles.Default.FontColor')
        self._dicRenderingParamMemBuffer["Styles.Default.BackColor"] = self._oParametersRendering.get('Styles.Default.BackColor')
        self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"] = self._oParametersRendering.get('RenderingOptions.NumberOfMinutesPerSlot')
        self._dicRenderingParamMemBuffer["NumberOfSlotsForMoon"] = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForMoon')
        self._dicRenderingParamMemBuffer["NumberOfSlotsForMoonFeatures"] = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForMoonFeatures')
        self._dicRenderingParamMemBuffer["NumberOfSlotsForPlanets"] = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForPlanets')
        self._dicRenderingParamMemBuffer["NumberOfSlotsForDeepSky"] = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForDeepSky')
        self._dicRenderingParamMemBuffer["PathToLogFileName"] = self._oParameters.Runtime().get("Global.PathToLogFileName")
        self._dicRenderingParamMemBuffer["MaximumLunarFeatureSunAltitude"] = self._oParametersRendering.get('RenderingOptions.MaximumLunarFeatureSunAltitude')
        self._dicRuntimeParamMemBuffer["MinDurationForMoonObservableInMinutes"] = self._oParametersRuntime.get('Observation.MinDurationForMoonObservableInMinutes')
        self._dicRuntimeParamMemBuffer["MinDurationForPlanetObservableInMinutes"] = self._oParametersRuntime.get('Observation.MinDurationForPlanetObservableInMinutes')
        self._dicRuntimeParamMemBuffer["MinDurationForDeepSkyObservableInMinutes"] = self._oParametersRuntime.get('Observation.MinDurationForDeepSkyObservableInMinutes')
        self._dicLocalizationMemBuffer["At"] = self._oParameters.Localization().getWithDefault("At")
        self._dicLocalizationMemBuffer["CulminationAbrev"] = self._oParameters.Localization().getWithDefault("CulminationAbrev")
        self._dicLocalizationMemBuffer["Azimut"] = self._oParameters.Localization().getWithDefault("Azimut")
        self._dicLocalizationMemBuffer["AzimutAbrev"] = self._oParameters.Localization().getWithDefault("AzimutAbrev")
        self._dicLocalizationMemBuffer["DistanceAbrev"] = self._oParameters.Localization().getWithDefault("DistanceAbrev")
        self._dicLocalizationMemBuffer["KilometerAbrev"] = self._oParameters.Localization().getWithDefault("KilometerAbrev")
        self._dicLocalizationMemBuffer["Phase"] = self._oParameters.Localization().getWithDefault("Phase")
        self._dicLocalizationMemBuffer["IlluminationAbrev"] = self._oParameters.Localization().getWithDefault("IlluminationAbrev")
        self._dicLocalizationMemBuffer["ColongitudeAbrev"] = self._oParameters.Localization().getWithDefault("ColongitudeAbrev")
        self._dicLocalizationMemBuffer["ObservableTime"] = self._oParameters.Localization().getWithDefault("ObservableTime")
        self._dicLocalizationMemBuffer["DegreesAbev"] = self._oParameters.Localization().getWithDefault("DegreesAbev")
        self._dicLocalizationMemBuffer["MinAngularDistanceWithMoon"] = self._oParameters.Localization().getWithDefault("MinAngularDistanceWithMoon")
        fDiffGMT = self._oParameters.Runtime().get("Place").get("CurrentLocalTimeDifferenceWithGMT")
        if fDiffGMT < 0.0:
            self._dicRenderingParamMemBuffer["GMTWarningLabel"] = self._oParameters.Localization().getWithDefault("GMTWarning") + " " + str(fDiffGMT)
        else:
            self._dicRenderingParamMemBuffer["GMTWarningLabel"] = self._oParameters.Localization().getWithDefault("GMTWarning") + " +" + str(fDiffGMT)

    def initBuffersFromEphemirides(self, oEphemeridesData): 
        iMaxSlotMoon = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForMoon')
        iMaxSlotPlanets = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForPlanets')
        iMaxSlotDeepSky = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForDeepSky')
        iMaxSlot = iMaxSlotMoon
        if iMaxSlotPlanets > iMaxSlot: iMaxSlot = iMaxSlotPlanets
        if iMaxSlotDeepSky > iMaxSlot: iMaxSlot = iMaxSlotDeepSky
        self._dicMemBuffer["BitmapColorforSunAltitudeOnSlot"] = {}
        for iSlot in range (0,iMaxSlot):
            self._dicMemBuffer["BitmapColorforSunAltitudeOnSlot"][str(iSlot)] = self._getBitmapColorforSunAltitude(oEphemeridesData.getSunAltitudeForSlot(iSlot))
        
        
    def _getBitmapColorForObjectAltitudeDependingOnSunAltitude(self, sObjectVisibilityStatus):
        tColor = self._dicRenderingParamMemBuffer["LineColorForStatus" + sObjectVisibilityStatus]
        return tColor

    def _getBitmapColorforSunAltitude(self, fSunAltitude):
        if fSunAltitude < -18.0:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.MoreThan18DegBelow"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.MoreThan18DegBelow')
        elif fSunAltitude < -12.0:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.12To18DegBelow"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.12To18DegBelow')
        elif fSunAltitude < -6.0:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.06To12DegBelow"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.06To12DegBelow')
        elif fSunAltitude < -0.0:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.00To06DegBelow"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.00To06DegBelow')
        elif fSunAltitude < 6.0:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.00To06DegAbove"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.00To06DegAbove')
        elif fSunAltitude < 12.0:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.06To12DegAbove"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.06To12DegAbove')
        else:
            tColor = self._dicRenderingParamMemBuffer["SkyColorForSunAltitude.MoreThan12DegAbove"]#self._oParametersRendering.get('ObjectVisibilityGraph.SkyColorForSunAltitude.MoreThan12DegAbove')
        return tColor

    def _getFont(self, sStyle = ""):
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle(sStyle)
        return theStyleFont

    def _getFontSize(self, sStyle = ""):
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle(sStyle)
        return iStyleFontSize
        
    def _getImageCopy(self, oImg):
        iImgWidth, iImgHeight = oImg.size
        return oImg.crop((0, 0, iImgWidth, iImgHeight))
        
    def _changeImageSize(self, oImg, iNewWidth, iNewHeight):
        theInitialImg = Image.new( 'RGBA', (iNewWidth, iNewHeight), (0, 0, 0, 255))
        theInitialImg.paste(oImg, (0,0), oImg)
        return theInitialImg
            
    def _getStyle(self, sStyle = ""):
        # Default values
        iStyleFontSize = self._dicRenderingParamMemBuffer["Styles.Default.FontSize"]
        sFontDirectory = self._dicRenderingParamMemBuffer["Styles.Default.FontDirectory"]
        if sFontDirectory == "": sFontDirectory = Tools.get_ResourceSubfolder_path("Fonts")
        sFont = sFontDirectory + self._oParametersRendering.get('Styles.Default.Font')
        tStyleFontColor = self._dicRenderingParamMemBuffer["Styles.Default.FontColor"]
        tStyleBackColor = self._dicRenderingParamMemBuffer["Styles.Default.BackColor"]
        
        # Style overlap
        if sStyle == "GMTWarning":
            iStyleFontSize = self._oParametersRendering.get('Styles.GMTWarning.FontSize')
            sFont = sFontDirectory + self._oParametersRendering.get('Styles.GMTWarning.Font')
        elif sStyle == "Legend":
            iStyleFontSize = self._oParametersRendering.get('Styles.Legend.FontSize')
            sFont = sFontDirectory + self._oParametersRendering.get('Styles.Legend.Font')
        elif sStyle == "RowHeaderDate":
            iStyleFontSize = self._oParametersRendering.get('Styles.RowHeader.Date.FontSize')
            sFont = sFontDirectory + self._oParametersRendering.get('Styles.RowHeader.Date.Font')
        elif sStyle == "RowHeaderTime":
            iStyleFontSize = self._oParametersRendering.get('Styles.RowHeader.Time.FontSize')
        elif sStyle == "ObjectName":
            iStyleFontSize = self._oParametersRendering.get('Styles.Object.Name.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.Object.Name.FontColor')
        elif sStyle == "ObjectNameNotified":
            iStyleFontSize = self._oParametersRendering.get('Styles.Object.NameNotified.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.Object.NameNotified.FontColor')
        elif sStyle == "ObjectData":
            iStyleFontSize = self._oParametersRendering.get('Styles.Object.Data.FontSize')
        elif sStyle == "ObjectAdditionalDailyData":
            iStyleFontSize = self._oParametersRendering.get('Styles.Object.AdditionalDailyData.FontSize')
        elif sStyle == "SectionTitleH0":
            iStyleFontSize = self._oParametersRendering.get('Styles.SectionTitle.H0.FontSize')
            tStyleBackColor = self._oParametersRendering.get('Styles.SectionTitle.H0.BackColor')
            tStyleFontColor = self._oParametersRendering.get('Styles.SectionTitle.H0.FontColor')
        elif sStyle == "SectionTitleH1":
            iStyleFontSize = self._oParametersRendering.get('Styles.SectionTitle.H1.FontSize')
            tStyleBackColor = self._oParametersRendering.get('Styles.SectionTitle.H1.BackColor')
            tStyleFontColor = self._oParametersRendering.get('Styles.SectionTitle.H1.FontColor')
        elif sStyle == "SectionTitleH2":
            iStyleFontSize = self._oParametersRendering.get('Styles.SectionTitle.H2.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.SectionTitle.H2.FontColor')
        elif sStyle == "LunarFeatureName":
            iStyleFontSize = self._oParametersRendering.get('Styles.LunarFeature.Name.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.LunarFeature.Name.FontColor')
        elif sStyle == "LunarFeatureNameNotified":
            iStyleFontSize = self._oParametersRendering.get('Styles.LunarFeature.NameNotified.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.LunarFeature.NameNotified.FontColor')
        elif sStyle == "LunarFeatureData":
            iStyleFontSize = self._oParametersRendering.get('Styles.LunarFeature.Data.FontSize')
            sFont = sFontDirectory + self._oParametersRendering.get('Styles.LunarFeature.Data.Font')
        elif sStyle == "BitmapHeaderH0":
            iStyleFontSize = self._oParametersRendering.get('Styles.BitmapHeader.H0.FontSize')
            tStyleBackColor = self._oParametersRendering.get('Styles.BitmapHeader.H0.BackColor')
            tStyleFontColor = self._oParametersRendering.get('Styles.BitmapHeader.H0.FontColor')
        elif sStyle == "BitmapHeaderH1":
            iStyleFontSize = self._oParametersRendering.get('Styles.BitmapHeader.H1.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.BitmapHeader.H1.FontColor')
        elif sStyle == "BitmapHeaderH2":
            iStyleFontSize = self._oParametersRendering.get('Styles.BitmapHeader.H2.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.BitmapHeader.H2.FontColor')
        elif sStyle == "AzimutInformation":
            iStyleFontSize = self._oParametersRendering.get('Styles.VisiblityGraphAzimutInformation.FontSize')
            tStyleFontColor = self._oParametersRendering.get('Styles.VisiblityGraphAzimutInformation.FontColor')
        
        # return all values for style
        try:
            theStyleFont = ImageFont.truetype(sFont, iStyleFontSize)
        except:
            theStyleFont = ImageFont.truetype(sFont + ".ttf", iStyleFontSize)
        return (iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor)

    def _getRectangularCoordXYFromLunarLongLat(self, fLongitude, fLatitude, iBitmapSize): 
        fLongitude = fLongitude - 90
        x = iBitmapSize/2 + (iBitmapSize/2 * math.cos(math.radians(fLongitude)) * math.cos(math.radians(fLatitude)))
        y = iBitmapSize/2 - (iBitmapSize/2 * math.sin(math.radians(fLatitude)))

        return x,y

    def _getRectangularCoordXY(self,fAngle, iRadius): 
        x = iRadius * math.cos(math.radians(fAngle))
        y = iRadius * math.sin(math.radians(fAngle))

        return x,y
        
    def _addLunarFeatureRow(self, oLunarFeatureObject, oCalendar, oEphemeridesData, oImg):
        iNbSlotsPerDay = (1440 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])

        sComment1 = self._oParameters.Localization().getWithDefault(oLunarFeatureObject.get("Type")) + "    -    " + self._oParameters.Localization().getWithDefault("LongitudeAbrev") + ": " + str(oLunarFeatureObject.get("Longitude")) + self._dicLocalizationMemBuffer["DegreesAbev"] + "  -  "  + self._oParameters.Localization().getWithDefault("LatitudeAbrev") + ": " + str(oLunarFeatureObject.get("Latitude")) + self._dicLocalizationMemBuffer["DegreesAbev"]
        sComment2 = ""
        sComment3 = ""
        sFormatForFloatValues = "{0:.1f}"
        if oLunarFeatureObject.get("Diameter") != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getWithDefault("Diameter") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.get("Diameter")) + " " + self._oParameters.Localization().getWithDefault("KilometerAbrev")
        if oLunarFeatureObject.get("Depth") != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getWithDefault("Depth") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.get("Depth")) + " " + self._oParameters.Localization().getWithDefault("KilometerAbrev")
        if oLunarFeatureObject.get("Height") != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getWithDefault("Height") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.get("Height")) + " " + self._oParameters.Localization().getWithDefault("KilometerAbrev")
        if oLunarFeatureObject.get("Length") != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getWithDefault("Length") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.get("Length")) + " " + self._oParameters.Localization().getWithDefault("KilometerAbrev")
        if oLunarFeatureObject.get("Breadth") != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getWithDefault("Breadth") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.get("Breadth")) + " " + self._oParameters.Localization().getWithDefault("KilometerAbrev")
        if oLunarFeatureObject.get("Rukl") != "": sComment3 += ("  -  " if len(sComment3) > 0 else "") + self._oParameters.Localization().getWithDefault("Rukl") + ": " + oLunarFeatureObject.get("Rukl")
        iRowPositionY, theNewImg = self._addLunarFeatureRowHeader(oLunarFeatureObject, sComment1, sComment2, sComment3, oImg)
        iTmpX, iTmpY = theNewImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayIsObservable = False
        bAtLeastOneDayIsNotObservable = False
        iBuffDaySlotForDataInfo = (iNbSlotsPerDay + self._oParametersRendering.get('RenderingOptions.DaySlotForDataInfo') - oCalendar.getLocalStartTimeSlotBasedHour0( self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]) ) % iNbSlotsPerDay
        iBuffNumberOfSlotsForMoonFeatures = self._dicRenderingParamMemBuffer["NumberOfSlotsForMoonFeatures"]
        fBuffLongitude = oLunarFeatureObject.get("Longitude")
        fBuffLatitude = oLunarFeatureObject.get("Latitude")
        oBuffEphemerideDataObjectMoon = oEphemeridesData.getEphemerideDataObject("Moon")
        for iDaySlot in range (0,  iBuffNumberOfSlotsForMoonFeatures, iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + iBuffDaySlotForDataInfo
            iStartX = RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph + (iDay * iNbSlotsPerDay * iSlotWidthInPx) + (iDay * RendererBitmap.iTableSpaceBetweenDays)
            bToBeDisplayed, bIsObservable, theNewImg =  self._addLunarFeatureVisibilityBitmapForDay(iDaySlot, iDaySlot + iNbSlotsPerDay, iDataSlot, oLunarFeatureObject, oCalendar, oEphemeridesData, theNewImg, iStartX, iRowPositionY)
            if bToBeDisplayed:
                bAtLeastOneDayToBeDisplayed = True
            if bIsObservable:
                bAtLeastOneDayIsObservable = True
            if not bIsObservable:
                bAtLeastOneDayIsNotObservable = True
            # Draw Moon Map
            iBitmapSize = 50
            iPosXMoonMap = iStartX + 1
            iPosYMoonMap = iRowPositionY 
            theNewImg = self._addMoonMinimapBitmap( oBuffEphemerideDataObjectMoon.getPhaseForSlot(iDataSlot), fBuffLongitude, fBuffLatitude, theNewImg, iPosXMoonMap, iPosYMoonMap, iBitmapSize)

        if bAtLeastOneDayIsObservable:
            if not bAtLeastOneDayIsNotObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.get('VisibilityFlags.Color.Observable'), iRowPositionY, theNewImg)
            else:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.get('VisibilityFlags.Color.AtLeastOneDayObservable'), iRowPositionY, theNewImg)
        else:
            theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.get('VisibilityFlags.Color.NotObservable'), iRowPositionY, theNewImg)
            
        if bAtLeastOneDayToBeDisplayed:
            return True, bAtLeastOneDayIsObservable, theNewImg
        else:
            return False, bAtLeastOneDayIsObservable, oImg
                
    def _addLunarFeatureRowHeader(self, oLunarFeatureObject, sComment1,  sComment2,  sComment3, oImg):
        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        
        iNewHeight = iImgHeight + iTableObjectRowHeight + 1
        oNewImg = self._changeImageSize(oImg, iImgWidth, iNewHeight)
        iStartX = RendererBitmap.iTableMarginLeft
        iStartY = iImgHeight + 1
        theNewDraw = ImageDraw.Draw(oNewImg)

        # Draw Border
        theNewDraw.rectangle((iStartX, iStartY, iStartX + RendererBitmap.iTableWidthObjectLabel, iStartY + iTableObjectRowHeight), fill=(255, 255, 255))

        # Display name and infos
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle("LunarFeatureName")
        iStyleFontSizeNotified, theStyleFontNotified, tStyleFontColorNotified, tStyleBackColorNotified = self._getStyle("LunarFeatureNameNotified")
        
        if oLunarFeatureObject.get("NotifyWhenObservable"):
            theNewDraw.text((iStartX + 3, iStartY + 5), oLunarFeatureObject.get("Name"), tStyleFontColorNotified, font=theStyleFontNotified)
        else:
            theNewDraw.text((iStartX + 3, iStartY + 5), oLunarFeatureObject.get("Name"), tStyleFontColor, font=theStyleFont)
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), sComment1, (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), sComment2, (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 + 12), sComment3, (0,0,0), font=self._getFont("LunarFeatureData"))

        return iStartY, oNewImg

    def _addLunarFeatureVisibilityBitmapForDay(self, iStartSlot, iEndSlot, iDataSlot, oLunarFeatureObject, oCalendar, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        bToBeDisplayed = False
        bIsObservable = False
        iNbRow = 90 / 5
        
        # create image and draw objects
        iBitmapHeight = iNbRow * RendererBitmap.iAltitudeRowHeight - 1
        iBitmapWidth = iSlotWidthInPx * iNbSlotsPerDay
        oNewImg = self._getImageCopy(oImg)
        theNewDraw = ImageDraw.Draw(oNewImg)

        # draw border
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        iBorderStartX = iRowPositionX 
        iBorderEndX = iBorderStartX + iNbSlotsPerDay * iSlotWidthInPx
        iBorderStartY = iRowPositionY - 1
        iBorderEndY = iBorderStartY + iTableObjectRowHeight - 1
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127, 255), fill=(40, 40, 40, 255))
        
        # create image and draw objects
        # draw table
        fBuffLongitudeMin = oLunarFeatureObject.get("LongitudeMin")
        fBuffLongitudeMax = oLunarFeatureObject.get("LongitudeMax")
        bBuffShowWhenTerminatorIsOnLunarFeature = self._oParametersRendering.get('RenderingOptions.ShowWhenTerminatorIsOnLunarFeature')
        fBuffShowWhenTerminatorIsOnLunarFeatureWithinDeg = self._oParametersRendering.get('RenderingOptions.ShowWhenTerminatorIsOnLunarFeatureWithinDeg')
        oBuffEphemerideDataObjectMoon = oEphemeridesData.getEphemerideDataObject("Moon")
        fBuffLunarFeatureLongitude = oLunarFeatureObject.get("Longitude")
        fBuffLunarFeatureLatitude = oLunarFeatureObject.get("Latitude")
        fBuffMaximumLunarFeatureSunAltitude = self._dicRenderingParamMemBuffer["MaximumLunarFeatureSunAltitude"]
        tBuffColorForStatusGood = self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.Good')
        tBuffColorForStatusSunBelowHorizon = self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.SunBelowHorizon')
        tBuffColorForStatusSunTooHigh = self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.SunTooHigh')
        for iSlot in range(iStartSlot, iEndSlot):
            fSunAltitudeOverFeature = MeeusAlgorithms.getSunAltitudeFromMoonFeature(fBuffLunarFeatureLongitude, fBuffLunarFeatureLatitude, oBuffEphemerideDataObjectMoon.getSelenographicLongitudeForSlot(iSlot), oBuffEphemerideDataObjectMoon.getSelenographicLatitudeForSlot(iSlot))
            sMoonVisibilityStatus = oEphemeridesData.getEphemerideDataObject("Moon").getVisibilityStatus(iSlot)
            fLongitudeMin = (fBuffLongitudeMin - fBuffShowWhenTerminatorIsOnLunarFeatureWithinDeg + 360.0) % 360.0
            fLongitudeMax = (fBuffLongitudeMax + fBuffShowWhenTerminatorIsOnLunarFeatureWithinDeg + 360.0) % 360.0
            fTerminatorLongitudeRise = (oBuffEphemerideDataObjectMoon.getSelenographicLongitudeForSlot(iSlot) - 90.0) % 360.0
            fTerminatorLongitudeSet = (oBuffEphemerideDataObjectMoon.getSelenographicLongitudeForSlot(iSlot) + 90.0) % 360.0

            if fLongitudeMax < fLongitudeMin: fLongitudeMax += 360.0
            if fTerminatorLongitudeRise < fLongitudeMin: fTerminatorLongitudeRise += 360.0
            if fTerminatorLongitudeSet < fLongitudeMin: fTerminatorLongitudeSet += 360.0
            
            bIsTerminatorNearFeature = ((fTerminatorLongitudeRise >= fLongitudeMin and fTerminatorLongitudeRise <= fLongitudeMax) or (fTerminatorLongitudeSet >= fLongitudeMin and fTerminatorLongitudeSet <= fLongitudeMax))
            
            # Define condition when Lunar feature is observable:
            #    - Moon must not be Hidden, Below or Impossible
            #    - Lunar feature must be  NearTerminator or sun altitude over feature must be > 0 and <= MaximumLunarFeatureSunAltitude
            if not (sMoonVisibilityStatus == "Hidden" or sMoonVisibilityStatus == "Below" or sMoonVisibilityStatus == "Impossible") and (bIsTerminatorNearFeature or (fSunAltitudeOverFeature > 0.0 and fSunAltitudeOverFeature <= fBuffMaximumLunarFeatureSunAltitude)):
                bIsObservable = True
            
            iTransparency = 255
            if sMoonVisibilityStatus == "Hidden" or sMoonVisibilityStatus == "Impossible" :
                iTransparency = 250
            if sMoonVisibilityStatus == "Below":
                iTransparency = 0
            if bBuffShowWhenTerminatorIsOnLunarFeature and bIsTerminatorNearFeature:
                tColor = tBuffColorForStatusGood
            elif fSunAltitudeOverFeature < 0.0:  
                tColor = tBuffColorForStatusSunBelowHorizon
            elif fSunAltitudeOverFeature >= fBuffMaximumLunarFeatureSunAltitude:
                tColor = tBuffColorForStatusSunTooHigh
            else:
                tColor = (255, 127 + int(fSunAltitudeOverFeature / fBuffMaximumLunarFeatureSunAltitude * 128.0), int(fSunAltitudeOverFeature / fBuffMaximumLunarFeatureSunAltitude * 255.0))
            tColor = (tColor[0], tColor[1], tColor[2], iTransparency)

                    
            x1 = iBorderStartX + 1 + (iSlot - iStartSlot) * iSlotWidthInPx
            x2 = x1 + iSlotWidthInPx - 1
            y1 = iBorderStartY + 1
            y2 = iBorderEndY - 1 - RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
            theNewDraw.rectangle((x1, y1, x2, y2), fill=tColor)

        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127, 255))

        # Additional data
        sAdditionalText = 'At ' + oCalendar.getLocalTimeForSlotAsHHMM(iDataSlot, self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]) + ':   Sun Altitude: ' + str(int(round(MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.get("Longitude"), oLunarFeatureObject.get("Latitude"), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot))))) + self._dicLocalizationMemBuffer["DegreesAbev"] + '  Sun Azimut: ' + str(int(round(MeeusAlgorithms.getSunAzimutFromMoonFeature(oLunarFeatureObject.get("Longitude"), oLunarFeatureObject.get("Latitude"), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot))))) + self._dicLocalizationMemBuffer["DegreesAbev"]
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255, 255), font=self._getFont("ObjectAdditionalDailyData"))
        
        bToBeDisplayed = (bIsObservable or self._oParametersRendering.get('RenderingOptions.ForceObservable'))
        if bToBeDisplayed:        
            return True, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
                
    def _addMoonMinimapBitmap(self, iPhase, fLongitude, fLatitude, oImg, iPosX, iPosY, iBitmapSize):
        iIndicatorSizeInPx = 3
        
        tColorMoonMapBorder = self._oParametersRendering.get('MoonMiniMap.Color.Border')
        tColorMoonMapBackground = self._oParametersRendering.get('MoonMiniMap.Color.Background')
        tColorMoonMapLight = self._oParametersRendering.get('MoonMiniMap.Color.Light')
        tColorMoonMapDark = self._oParametersRendering.get('MoonMiniMap.Color.Dark')
        
        # Draw intermediary bitmaps
        imgFullLight = Image.new( 'RGBA', (iBitmapSize + 2, iBitmapSize + 1), tColorMoonMapBackground) # create a new black image
        drawFullLight = ImageDraw.Draw(imgFullLight)
        drawFullLight.ellipse((0, 0, iBitmapSize, iBitmapSize), fill=tColorMoonMapLight, outline=tColorMoonMapBorder)
        imgQuarterRightLight = imgFullLight.crop((iBitmapSize/2, 0, iBitmapSize, iBitmapSize))
        imgQuarterLeftLight = imgFullLight.crop((0, 0, iBitmapSize/2, iBitmapSize))
        
        imgFullDark = Image.new( 'RGBA', (iBitmapSize + 2, iBitmapSize + 1), tColorMoonMapBackground) # create a new black image
        drawFullDark = ImageDraw.Draw(imgFullDark)
        drawFullDark.ellipse((0, 0, iBitmapSize, iBitmapSize), fill=tColorMoonMapDark, outline=tColorMoonMapBorder)
        imgQuarterRightDark = imgFullDark.crop((iBitmapSize/2, 0, iBitmapSize, iBitmapSize))
        imgQuarterLeftDark = imgFullDark.crop((0, 0, iBitmapSize/2, iBitmapSize))
        
        if iPhase < 0.0: iPhase = iPhase + 360.0
        
        if iPhase >= 0 and iPhase < 90:
            iTransformedPhase = iPhase
        elif iPhase >= 90 and iPhase < 180:
            iTransformedPhase = 180 - iPhase
        elif iPhase >= 180 and iPhase < 270:
            iTransformedPhase = iPhase - 180
        else:
            iTransformedPhase = 360 - iPhase

        iSizeWidth = (iBitmapSize/2) * math.cos(math.radians(iTransformedPhase))
        
        imgToQ = Image.new( 'RGBA', (iBitmapSize + 2, iBitmapSize + 1), tColorMoonMapBackground) # create a new black image
        drawToQ = ImageDraw.Draw(imgToQ)
        drawToQ.ellipse((0, 0, iBitmapSize, iBitmapSize ), fill=tColorMoonMapLight, outline=tColorMoonMapBorder)
        drawToQ.ellipse((iBitmapSize/2 - iSizeWidth, 0, iBitmapSize/2 + iSizeWidth, iBitmapSize ), fill=tColorMoonMapDark, outline=tColorMoonMapDark)
        imgToFirstQRight = imgToQ.crop((iBitmapSize/2, 0, iBitmapSize, iBitmapSize))
        imgToLastQLeft = imgToQ.crop((0, 0, iBitmapSize/2, iBitmapSize))
        
        imgAfterQ = Image.new( 'RGBA', (iBitmapSize + 2, iBitmapSize + 1), tColorMoonMapBackground) # create a new black image
        drawAfterQ = ImageDraw.Draw(imgAfterQ)
        drawAfterQ.ellipse((0, 0, iBitmapSize , iBitmapSize ), fill=tColorMoonMapDark, outline=tColorMoonMapBorder)
        drawAfterQ.ellipse((iBitmapSize/2 - iSizeWidth, 0, iBitmapSize/2 + iSizeWidth, iBitmapSize ), fill=tColorMoonMapLight, outline=tColorMoonMapLight)
        imgAfterFirstQRight = imgAfterQ.crop((iBitmapSize/2, 0, iBitmapSize, iBitmapSize))
        imgAfterLastQLeft = imgAfterQ.crop((0, 0, iBitmapSize/2, iBitmapSize))
            
        # Create moon minimap by fusioning intermediary bitmaps
        imgMoonMinimap = Image.new( 'RGBA', (iBitmapSize + 2, iBitmapSize + 1), tColorMoonMapBackground) # create a new black image
        drawMoonMinimap = ImageDraw.Draw(imgMoonMinimap)
        
        if iPhase >= 0 and iPhase < 90:
            imgMoonMinimap.paste(imgAfterLastQLeft, (0,0))
            imgMoonMinimap.paste(imgQuarterRightLight, (iBitmapSize/2 ,0))
        elif iPhase >= 90 and iPhase < 180:
            imgMoonMinimap.paste(imgQuarterLeftDark, (0,0))
            imgMoonMinimap.paste(imgToFirstQRight, (iBitmapSize/2 ,0))
        elif iPhase >= 180 and iPhase < 270:
            imgMoonMinimap.paste(imgToLastQLeft, (0,0))
            imgMoonMinimap.paste(imgQuarterRightDark, (iBitmapSize/2 ,0))
        else:
            imgMoonMinimap.paste(imgQuarterLeftLight, (0,0))
            imgMoonMinimap.paste(imgAfterFirstQRight, (iBitmapSize/2 ,0))
            
        # Redraw moon border
        imgMoonBorder = Image.new( 'RGBA', (iBitmapSize + 2, iBitmapSize + 1), tColorMoonMapBackground) # create a new black image
        drawMoonBorder = ImageDraw.Draw(imgMoonBorder)
        drawMoonBorder.ellipse((0, 0, iBitmapSize, iBitmapSize), fill=(0, 0, 0, 0), outline=tColorMoonMapBorder)
        imgMoonMinimap.paste(imgMoonBorder, (0,0), imgMoonBorder)
            
        # Compute position of the feature in the image
        # Draw a red dot at the position of the feature
        x, y = self._getRectangularCoordXYFromLunarLongLat(fLongitude, fLatitude, iBitmapSize)
        drawMoonMinimap.ellipse((x - int(iIndicatorSizeInPx / 2) , y - int(iIndicatorSizeInPx / 2), x + int(iIndicatorSizeInPx / 2), y + int(iIndicatorSizeInPx / 2)), fill=(255,0,0), outline=(255,0,0))

        # merge moon minimap with original bitmap
        oImg.paste(imgMoonMinimap, (iPosX,iPosY), imgMoonMinimap)
        return oImg          

    def _addHeliocentricBitmap(self, sPlanetName, fEarthMeanLongInDeg, fPlanetMeanLongInDeg, iRowPositionY, oImg):
        oNewImg = self._getImageCopy(oImg)
        theNewDraw = ImageDraw.Draw(oNewImg)

        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        iBitmapSize = iTableObjectRowHeight
        iPositionX = RendererBitmap.iTableWidthObjectLabel - iBitmapSize - RendererBitmap.iTableVisibilityFlagWidth - 1
        tColorBackground = self._oParametersRendering.get('HeliocentricGraph.Color.Background')
        tColorLines = self._oParametersRendering.get('HeliocentricGraph.Color.Lines')
        tColorSun = self._oParametersRendering.get('HeliocentricGraph.Color.Sun')
        tColorEarth = self._oParametersRendering.get('HeliocentricGraph.Color.Earth')
        tColorPlanet = self._oParametersRendering.get('HeliocentricGraph.Color.Planet')

        iSunSize = 6
        iEarthSize = 4 
        iPlanetSize = 4

        if sPlanetName == "Mercury" or sPlanetName == "Venus":
            iRadiusPlanet = iBitmapSize / 4
            iRadiusEath = (iBitmapSize/2) - (iPlanetSize/2)
        else:
            iRadiusPlanet = (iBitmapSize/2) - (iPlanetSize/2)
            iRadiusEath = iBitmapSize / 4

        theNewDraw.ellipse((iPositionX + iBitmapSize/2 - iRadiusEath, iRowPositionY + iBitmapSize/2 - iRadiusEath, iPositionX + iBitmapSize/2 + iRadiusEath, iRowPositionY + iBitmapSize/2 + iRadiusEath), outline=tColorLines)
        x, y = self._getRectangularCoordXY(fEarthMeanLongInDeg, iRadiusEath)
        theNewDraw.ellipse((iPositionX + iBitmapSize/2 + x - iEarthSize/2, iRowPositionY + iBitmapSize/2 + y - iEarthSize/2, iPositionX + iBitmapSize/2 + x + iEarthSize/2, iRowPositionY + iBitmapSize/2 + y + iEarthSize/2), fill=tColorEarth, outline=tColorEarth)

        theNewDraw.ellipse((iPositionX + iBitmapSize/2 - iRadiusPlanet, iRowPositionY + iBitmapSize/2 - iRadiusPlanet, iPositionX + iBitmapSize/2 + iRadiusPlanet, iRowPositionY + iBitmapSize/2 + iRadiusPlanet), outline=tColorLines)
        x, y = self._getRectangularCoordXY(fPlanetMeanLongInDeg, iRadiusPlanet)
        theNewDraw.ellipse((iPositionX + iBitmapSize/2 + x - iPlanetSize/2, iRowPositionY + iBitmapSize/2 + y - iPlanetSize/2, iPositionX + iBitmapSize/2 + x + iPlanetSize/2, iRowPositionY + iBitmapSize/2 + y + iPlanetSize/2), fill=tColorPlanet, outline=tColorPlanet)

        theNewDraw.ellipse((iPositionX + iBitmapSize/2 - (iSunSize/2), iRowPositionY + iBitmapSize/2 - (iSunSize/2), iPositionX + iBitmapSize/2 + (iSunSize/2), iRowPositionY + iBitmapSize/2 + (iSunSize/2)), fill=tColorSun, outline=tColorSun)
        
        return oNewImg
        
    def _addObjectRow(self, oEphemeridesDataObject, oCalendar, oEphemeridesData, oImg):
        iNbSlotsPerDay = (1440 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        bIsObservable = False
        sHTMLObjectRow = ""
        if (oEphemeridesDataObject.getCategory() == "Moon"):
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, "", "", "", oImg)
            iMaxSlot = self._oParametersRendering.get('RenderingOptions.NumberOfSlotsForMoon')
        elif (oEphemeridesDataObject.getCategory() == "Planetary"):
            iMaxSlot = self._dicRenderingParamMemBuffer["NumberOfSlotsForPlanets"]
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(0)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0))) + self._dicLocalizationMemBuffer["DegreesAbev"] 
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (' + self._oParameters.Localization().getWithDefault("NearConjonction") + ')'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (' + self._oParameters.Localization().getWithDefault("NearOpposition") + ')'
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, self._oParameters.Localization().getWithDefault("Distance") + ": " +  str(int(round(oEphemeridesDataObject.getDistanceForSlot(0) * 149.600000, 1))) + ' ' + self._oParameters.Localization().getWithDefault("MillionKilometersAbrev"), self._oParameters.Localization().getWithDefault("PositionAngleAbrev") + ": " +  sMeanLongComment, self._oParameters.Localization().getWithDefault("ApparentDiameterAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getApparentDiameterInArcSecForSlot(0), 1))) + ' ' + self._oParameters.Localization().getWithDefault("SecondOfAngleAbrev"), oImg)
            # add heliocentric schema
            theNewImg = self._addHeliocentricBitmap(oEphemeridesDataObject.getName(), oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0, oEphemeridesDataObject.getMeanLongForSlot(0), iRowPositionY, theNewImg)
        else:
            iMaxSlot = self._dicRenderingParamMemBuffer["NumberOfSlotsForDeepSky"]
            aSkyObject = self._oParameters.SkyObjects().getObjectByID(oEphemeridesDataObject.getID())
            sDataRow1 = self._oParameters.Localization().getWithDefault(aSkyObject.get("Type"))
            if aSkyObject.get("DistanceUnit") != "":
                sDataRow1 += "     "  + self._oParameters.Localization().getWithDefault("DistanceAbrev") + ": " + str(aSkyObject.get("Distance")) + " "  + self._oParameters.Localization().getWithDefault(aSkyObject.get("DistanceUnit"))
            sDataRow2 = self._oParameters.Localization().getWithDefault("RightAscensionAbrev") + ": " + aSkyObject.get("RA")[0:2] + "h" + aSkyObject.get("RA")[2:4] + "'" + aSkyObject.get("RA")[4:] + '"'  + "    " + self._oParameters.Localization().getWithDefault("DeclinationAbrev") + ": " +  str(round(aSkyObject.get("Dec"),2)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            if aSkyObject.get("ApparentMagnitude") != "":
                sDataRow3 = self._oParameters.Localization().getWithDefault("ApparentMagnitudeAbrev") + ": " + str(aSkyObject.get("ApparentMagnitude"))
            if aSkyObject.get("DimensionXUnit") != "":
                if sDataRow3 != "": sDataRow3 += "     "
                sDataRow3 += self._oParameters.Localization().getWithDefault("DimensionAbrev") + ": " + str(aSkyObject.get("DimensionX")) + " "  + aSkyObject.get("DimensionXUnit")
                if aSkyObject.get("DimensionYUnit") != "":
                    sDataRow3 += " x "  + str(aSkyObject.get("DimensionY")) + " "  + aSkyObject.get("DimensionYUnit")
            if aSkyObject.get("Comment1") != "":
                if sDataRow3 != "": sDataRow3 += "     "
                sDataRow3 += aSkyObject.get("Comment1")
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, sDataRow1, sDataRow2, sDataRow3, oImg)
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayObservable = False
        bAtLeastOneDayNotObservable = False
        iBuffDaySlotForDataInfo = (iNbSlotsPerDay + self._oParametersRendering.get('RenderingOptions.DaySlotForDataInfo') - oCalendar.getLocalStartTimeSlotBasedHour0( self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]) ) % iNbSlotsPerDay
        for iDaySlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + iBuffDaySlotForDataInfo
            iStartX = RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph + (iDay * iNbSlotsPerDay * iSlotWidthInPx) + (iDay * RendererBitmap.iTableSpaceBetweenDays)
            bIsDisplayed, bIsObservable, theNewImg =  self._addObjectVisibilityInfoForDay( oEphemeridesDataObject, oCalendar, iDaySlot, iDaySlot + iNbSlotsPerDay, iDataSlot, oEphemeridesData, theNewImg, iStartX, iRowPositionY)
            if bIsDisplayed:
                bAtLeastOneDayToBeDisplayed = True
            if bIsObservable:
                bAtLeastOneDayObservable = True
            else:
                bAtLeastOneDayNotObservable = True

        if bAtLeastOneDayObservable:
            if not bAtLeastOneDayNotObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.get('VisibilityFlags.Color.Observable'), iRowPositionY, theNewImg)
            else:            
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.get('VisibilityFlags.Color.AtLeastOneDayObservable'), iRowPositionY, theNewImg)
        else:
            theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.get('VisibilityFlags.Color.NotObservable'), iRowPositionY, theNewImg)
            
        if bAtLeastOneDayToBeDisplayed:
            return bAtLeastOneDayToBeDisplayed, bAtLeastOneDayObservable, theNewImg
        else:
            return bAtLeastOneDayToBeDisplayed, bAtLeastOneDayObservable, oImg
            
    def _addObjectRowHeader(self, oEphemeridesDataObject, sObjectDataRow1, sObjectDataRow2, sObjectDataRow3, oImg):
        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight

        iNewHeight = iImgHeight + iTableObjectRowHeight + 1
        oNewImg = self._changeImageSize(oImg, iImgWidth, iNewHeight)
        iStartX = RendererBitmap.iTableMarginLeft
        iStartY = iImgHeight + 1
        theNewDraw = ImageDraw.Draw(oNewImg)

        theNewDraw.rectangle((iStartX, iStartY, iStartX + RendererBitmap.iTableWidthObjectLabel, iStartY + iTableObjectRowHeight), fill=(255, 255, 255))

        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle("ObjectName")
        iStyleFontSizeNotified, theStyleFontNotified, tStyleFontColorNotified, tStyleBackColorNotified = self._getStyle("ObjectNameNotified")
        
        if self._oParameters.SkyObjects().getObjectByID(oEphemeridesDataObject.getID()).get("NotifyWhenObservable"):
            theNewDraw.text((iStartX + 3, iStartY), self._oParameters.Localization().getWithDefault(oEphemeridesDataObject.getName()), tStyleFontColorNotified, font=theStyleFontNotified)
        else:
            theNewDraw.text((iStartX + 3, iStartY), self._oParameters.Localization().getWithDefault(oEphemeridesDataObject.getName()), tStyleFontColor, font=theStyleFont)
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), Tools.removeHTMLTags(sObjectDataRow1), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), Tools.removeHTMLTags(sObjectDataRow2), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 * 2), Tools.removeHTMLTags(sObjectDataRow3), (0,0,0), font=self._getFont("ObjectData"))
        
        if oEphemeridesDataObject.getPictureName() <> "":
            imgObjectThumbnail = Image.open(Tools.get_ResourceSubfolder_path("Bitmaps") + oEphemeridesDataObject.getPictureName())
            oNewImg.paste(imgObjectThumbnail, (iStartX + RendererBitmap.iTableWidthObjectLabel - 50 - RendererBitmap.iTableVisibilityFlagWidth - 2, iStartY + 2 ))
        
        return iStartY, oNewImg

    def _addObjectVisibilityBitmapForDay(self, oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsObservable = 0
        fMinAngularDistanceWithMoon = 360.0 
        
        iNbSlotsPerDay = (1440 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iNbRow = 90 / 5
        bIsObservable = False
        
        # create image and draw objects
        iBitmapHeight = iNbRow * RendererBitmap.iAltitudeRowHeight - 1
        iBitmapWidth = iSlotWidthInPx * iNbSlotsPerDay
        oNewImg = self._getImageCopy(oImg)
        theNewDraw = ImageDraw.Draw(oNewImg)

        # draw border
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        iBorderStartX = iRowPositionX - 3
        iBorderEndX = iBorderStartX + iNbSlotsPerDay * iSlotWidthInPx
        iBorderStartY = iRowPositionY 
        iBorderEndY = iBorderStartY + iTableObjectRowHeight - 1
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127), fill=(40, 40, 40))
        
        # draw graph
        if 1 == 1:
            iPrevX = -1
            iPrevY = -1
            for iRowAltitude in range(90, 0, -5):
                iRow = iRowAltitude / 5
                y1 = (iNbRow * RendererBitmap.iAltitudeRowHeight) - (iRow * RendererBitmap.iAltitudeRowHeight)
                y2 = y1 + RendererBitmap.iAltitudeRowHeight - 1
                for iSlot in range(iStartSlot, iEndSlot):
                    x1 = (iSlot - iStartSlot) * iSlotWidthInPx
                    x1 = (iSlot - iStartSlot) * iSlotWidthInPx
                    x2 = x1 + iSlotWidthInPx - 1
                    tColor = self._dicMemBuffer["BitmapColorforSunAltitudeOnSlot"][str(iSlot)]
                    theNewDraw.rectangle((iRowPositionX - 1 + x1, iRowPositionY + 1 + y1, iRowPositionX - 1 + x2, iRowPositionY + 1 + y2), fill=tColor)
            bBuffShowObstructionOnGraph = self._oParametersRendering.get("RenderingOptions.ShowObstructionOnGraph")
            tBuffShowObstructionOnGraphColor = self._oParametersRendering.get("RenderingOptions.ShowObstructionOnGraphColor")
            oBuffPlace = self._oParameters.Runtime().get("Place")
            for iSlot in range(iStartSlot, iEndSlot):
                x = (iSlot - iStartSlot) * iSlotWidthInPx + (iSlotWidthInPx/2) - 1
                y = iBitmapHeight - int(float( oEphemeridesDataObject.getAltitudeForSlot(iSlot) / 90.0) * float(iBitmapHeight))
                # Draw obstruction
                if bBuffShowObstructionOnGraph:
                    fObstructionMinAlt, fObstructionMaxAlt = oBuffPlace.get("MinMaxAltitudeObstructedForAzimut")[str(int(oEphemeridesDataObject.getAzimutForSlot(iSlot)))]
                    if not(fObstructionMinAlt == 0.0 and fObstructionMaxAlt == 0.0):
                        yObstructedMin = iBitmapHeight - int(float( fObstructionMinAlt / 90.0) * float(iBitmapHeight))
                        yObstructedMax = iBitmapHeight - int(float( fObstructionMaxAlt / 90.0) * float(iBitmapHeight))
                        tColorObstruction = oBuffPlace.get("ColorForAzimutAltitude")[str(Tools.getIndexFromAzimutAltitude(oEphemeridesDataObject.getAzimutForSlot(iSlot), fObstructionMinAlt))]
                        if tColorObstruction == None:
                            tColorObstruction = tBuffShowObstructionOnGraphColor
                        theNewDraw.rectangle((iRowPositionX - 1 + (iSlot - iStartSlot) * iSlotWidthInPx, iRowPositionY + 1 + yObstructedMin, iRowPositionX - 1 + (iSlot - iStartSlot) * iSlotWidthInPx + iSlotWidthInPx - 1, iRowPositionY + 1 + yObstructedMax), fill=tColorObstruction)
                # Draw object altitude line
                if oEphemeridesDataObject.getAltitudeForSlot(iSlot) > 0:
                    sObjectVisibilityStatus = oEphemeridesDataObject.getVisibilityStatus(iSlot)
                    tColor = self._getBitmapColorForObjectAltitudeDependingOnSunAltitude(sObjectVisibilityStatus)
                    bIsObservable = (not(sObjectVisibilityStatus == "Hidden" or sObjectVisibilityStatus == "Below" or sObjectVisibilityStatus == "Impossible" or sObjectVisibilityStatus == "Difficult" or sObjectVisibilityStatus == "DifficultMoonlight") or bIsObservable)
                    if oEphemeridesDataObject.getID() != "Moon":
                        fAngularSeparationWithMoon = MeeusAlgorithms.getAngularSeparation(oEphemeridesDataObject.getRightAscensionForSlot(iSlot), oEphemeridesDataObject.getDeclinationForSlot(iSlot), oEphemeridesData.getEphemerideDataObject("Moon").getRightAscensionForSlot(iSlot),  oEphemeridesData.getEphemerideDataObject("Moon").getDeclinationForSlot(iSlot))
                        if fAngularSeparationWithMoon < fMinAngularDistanceWithMoon: fMinAngularDistanceWithMoon = fAngularSeparationWithMoon
                    if (sObjectVisibilityStatus == "Good" or sObjectVisibilityStatus == "Low"):
                        iNbSlotsObservable = iNbSlotsObservable + 1
                    if iPrevX > -1 and iPrevY > -1:
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY, iRowPositionX - 1 + x, iRowPositionY + 1 + y), fill=tColor)
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY -1, iRowPositionX - 1 + x, iRowPositionY + 1 + y -1 ), fill=tColor)
                iPrevX = x
                iPrevY = y
                
            # Draw Azimut information
            if self._oParametersRendering.get("RenderingOptions.ShowAzimutInformationOnGraph"):
                bAzimutInfoNdone = False
                bAzimutInfoSdone = False
                bAzimutInfoEdone = False
                bAzimutInfoOdone = False
                for iSlot in range(iStartSlot, iEndSlot):
                    if abs(oEphemeridesDataObject.getAzimutForSlot(iSlot) - 0.0) <= 1.4 and not bAzimutInfoNdone:
                        fAzimutInfo = "Nord"
                        bAzimutInfoNdone = True
                    elif abs(oEphemeridesDataObject.getAzimutForSlot(iSlot) - 90.0) <= 1.4 and not bAzimutInfoEdone:
                        fAzimutInfo = "Est"
                        bAzimutInfoEdone = True
                    elif abs(oEphemeridesDataObject.getAzimutForSlot(iSlot) - 180.0) <= 1.4 and not bAzimutInfoSdone:
                        fAzimutInfo = "Sud"
                        bAzimutInfoSdone = True
                    elif abs(oEphemeridesDataObject.getAzimutForSlot(iSlot) - 270.0) <= 1.4 and not bAzimutInfoOdone:
                        fAzimutInfo = "Ouest"
                        bAzimutInfoOdone = True
                    else:
                        fAzimutInfo = ""
                    if fAzimutInfo != "":
                        iStyleFontSizeAzimutInfo, theStyleFontAzimutInfo, tStyleFontColorAzimutInfo, tStyleBackColorAzimutInfo = self._getStyle("AzimutInformation")
                        theNewDraw.text((iRowPositionX - 1 + (iSlot - iStartSlot) * iSlotWidthInPx, iRowPositionY + iBitmapHeight - iStyleFontSizeAzimutInfo), fAzimutInfo, tStyleFontColorAzimutInfo, font=theStyleFontAzimutInfo)
                
        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127))
        
        # delete useless objects
        del theNewDraw        
        
        bIsDisplayed = (bIsObservable or self._oParametersRendering.get('RenderingOptions.ForceObservable') or (self._oParametersRendering.get('RenderingOptions.ForceDisplayPlanetMoon') and (oEphemeridesDataObject.getCategory() == "Planetary" or oEphemeridesDataObject.getCategory() == "Moon")))
        if bIsDisplayed:        
            return bIsDisplayed, bIsObservable, iNbSlotsObservable, fMinAngularDistanceWithMoon, oNewImg
        else:
            return False, bIsObservable, iNbSlotsObservable, fMinAngularDistanceWithMoon, oNewImg
        
    def _addObjectVisibilityInfoForDay(self, oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, iDataSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        bIsObservable = False
        iNbSlotsPerDay = (1440 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        
        bIsDisplayed, bIsObservable, iNbSlotsObservable, fMinAngularDistanceWithMoon, theNewImg = self._addObjectVisibilityBitmapForDay(oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX + 3, iRowPositionY)
        sObservableTime = "%02d" % (int(iNbSlotsObservable * self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]/60.0),) + ":" + "%02d" % (int((iNbSlotsObservable * self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]) % 60.0),)
        sMinAngularDistanceWithMoon = str(int(round(fMinAngularDistanceWithMoon,0))) + self._dicLocalizationMemBuffer["DegreesAbev"]
        
        # if the Observable Time is below a threshold taken from json parameters (depending on object type), then the object is considered as NOT observable
        iObservableMinutes = iNbSlotsObservable * self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]
        if    (iObservableMinutes < self._dicRuntimeParamMemBuffer["MinDurationForMoonObservableInMinutes"] and oEphemeridesDataObject.getCategory() == "Moon") \
           or (iObservableMinutes < self._dicRuntimeParamMemBuffer["MinDurationForPlanetObservableInMinutes"] and oEphemeridesDataObject.getCategory() == "Planetary") \
           or (iObservableMinutes < self._dicRuntimeParamMemBuffer["MinDurationForDeepSkyObservableInMinutes"] and oEphemeridesDataObject.getCategory() == "DeepSky"):
            bIsObservable = False
        
        if oEphemeridesDataObject.getCategory() == "Planetary":
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(iStartSlot) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(iStartSlot)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0)))
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' ('  + self._oParameters.Localization().getWithDefault("NearConjonction") + ')'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' ('  + self._oParameters.Localization().getWithDefault("NearOpposition") + ')'
            sAdditionalText = self._dicLocalizationMemBuffer["CulminationAbrev"] + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            sAdditionalText += ', ' + self._dicLocalizationMemBuffer["AzimutAbrev"] + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            if iNbSlotsObservable > 0: sAdditionalText += ', ' + self._dicLocalizationMemBuffer["ObservableTime"] + ' ' + sObservableTime
            if fMinAngularDistanceWithMoon < 120.0: sAdditionalText += ', ' + self._dicLocalizationMemBuffer["MinAngularDistanceWithMoon"] + ' ' + sMinAngularDistanceWithMoon
        elif oEphemeridesDataObject.getCategory() == "Moon":
            sAdditionalText  = self._dicLocalizationMemBuffer["At"] + ' ' + oCalendar.getLocalTimeForSlotAsHHMM(iDataSlot, self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]) + ':'
            sAdditionalText += ' '  + self._dicLocalizationMemBuffer["DistanceAbrev"] + ': ' + str(int(round(oEphemeridesDataObject.getDistanceForSlot(iDataSlot)))) + self._dicLocalizationMemBuffer["KilometerAbrev"] 
            #sAdditionalText += ', ' + self._dicLocalizationMemBuffer["Phase"] + ': ' + str(int(round(abs(oEphemeridesDataObject.getPhaseForSlot(iDataSlot)))))
            sAdditionalText += ', ' + self._dicLocalizationMemBuffer["IlluminationAbrev"] + ': ' + str(int(round(oEphemeridesDataObject.getIlluminationForSlot(iDataSlot) * 100))) + '%'
            sAdditionalText += ', ' + self._dicLocalizationMemBuffer["ColongitudeAbrev"] + ': ' + str(int(round(oEphemeridesDataObject.getColongitudeForSlot(iDataSlot)))) + self._dicLocalizationMemBuffer["DegreesAbev"]
            sAdditionalText += ' -=- '
            sAdditionalText += self._dicLocalizationMemBuffer["CulminationAbrev"] + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            sAdditionalText += ', ' + self._dicLocalizationMemBuffer["AzimutAbrev"] + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            if iNbSlotsObservable > 0: sAdditionalText += ', ' + self._dicLocalizationMemBuffer["ObservableTime"] + ' ' + sObservableTime
        else:
            sAdditionalText = self._dicLocalizationMemBuffer["CulminationAbrev"] + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            sAdditionalText += ', ' + self._dicLocalizationMemBuffer["AzimutAbrev"] + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot)) + self._dicLocalizationMemBuffer["DegreesAbev"]
            if iNbSlotsObservable > 0: sAdditionalText += ', ' + self._dicLocalizationMemBuffer["ObservableTime"] + ' ' + sObservableTime
            sAdditionalText += ', ' + self._dicLocalizationMemBuffer["MinAngularDistanceWithMoon"] + ' ' + sMinAngularDistanceWithMoon

        theNewDraw = ImageDraw.Draw(theNewImg)
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255), font=self._getFont("ObjectAdditionalDailyData"))
    
        return bIsDisplayed, bIsObservable, theNewImg
            
    def _addObjectVisibilityTableHeader(self, oCalendar, oEphemeridesData, sType, oImg):
        iNbSlotsPerDay = (1440 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iNbSlotsPerHour = 60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        iTableHeaderHeight = RendererBitmap.iTableHeaderRowHeight * 2 + RendererBitmap.iTableHeaderRowInterline # 2 rows + 5 pixel in between
        if sType == "Moon":
            iMaxSlot = self._dicRenderingParamMemBuffer["NumberOfSlotsForMoon"]
        elif sType == "MoonFeatures":
            iMaxSlot = self._dicRenderingParamMemBuffer["NumberOfSlotsForMoonFeatures"]
        elif sType == "Planet":
            iMaxSlot = self._dicRenderingParamMemBuffer["NumberOfSlotsForPlanets"]
        else:
            iMaxSlot = self._dicRenderingParamMemBuffer["NumberOfSlotsForDeepSky"]
        
        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        iNewWidth = RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph + (iSlotWidthInPx * iMaxSlot) + 50
        if iNewWidth < iImgWidth:
            iNewWidth = iImgWidth
        iNewHeight = iImgHeight + RendererBitmap.iTableMarginTop + iTableHeaderHeight
        oNewImg = self._changeImageSize(oImg, iNewWidth, iNewHeight)
        iStartX = RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph
        iStartY = iImgHeight + RendererBitmap.iTableMarginTop
        theNewDraw = ImageDraw.Draw(oNewImg)
        
        # print header
        iBufNumberOfMinutesPerSlot = self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]
        fontBuffRowHeaderDate = self._getFont("RowHeaderDate")
        fontBuffRowHeaderTime = self._getFont("RowHeaderTime")
        for iSlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            iDay = int(iSlot / iNbSlotsPerDay)
            iHeaderStartX = iStartX + (iDay * iNbSlotsPerDay * iSlotWidthInPx) + (iDay * RendererBitmap.iTableSpaceBetweenDays)
            iHeaderEndX = iHeaderStartX + (iNbSlotsPerDay * iSlotWidthInPx)
            iHeaderStartY = iStartY
            iHeaderEndY = iHeaderStartY + iTableHeaderHeight - 1
            theNewDraw.rectangle((iHeaderStartX, iHeaderStartY, iHeaderEndX, iHeaderEndY), fill=(255, 255, 255))
            theNewDraw.rectangle((iHeaderStartX + 1, iHeaderStartY + 1, iHeaderEndX - 1, iHeaderEndY - 1), fill=(0, 0, 0))
            # Display date
            theNewDraw.text((iHeaderStartX + 3, iHeaderStartY + 3), oCalendar.getFormattedLocalDateForSlot(iSlot, iBufNumberOfMinutesPerSlot), (255,255,255), font=fontBuffRowHeaderDate)
            # Display GMT warning
            sLabel = self._dicRenderingParamMemBuffer["GMTWarningLabel"]
            theNewDraw.text((iHeaderEndX - 3 - theNewDraw.textsize(sLabel, font=self._getFont("GMTWarning"))[0], iHeaderStartY + 3), sLabel, (255,255,255), font=self._getFont("GMTWarning"))            
            # Display hours
            for iDaySlot in range (iSlot,  iSlot + iNbSlotsPerDay, iNbSlotsPerHour ):
                theNewDraw.text((iHeaderStartX + 3 + (iDaySlot - iSlot) * iSlotWidthInPx, iStartY + RendererBitmap.iTableHeaderRowHeight + 4 + RendererBitmap.iTableHeaderRowInterline), oCalendar.getLocalTimeForSlot(iDaySlot, iBufNumberOfMinutesPerSlot)[0:2], (255,255,255), font=fontBuffRowHeaderTime)
        
        return oNewImg

    def _addTitleForSection(self, sTitle, sStyle, oImg, bFillRow, iStartY):
        # Get Style
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle(sStyle)

        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        if sStyle == "SectionTitleH0":
            iTopMargin = self._oParametersRendering.get('Styles.SectionTitle.H0.TopMargin')
            iBottomMargin = self._oParametersRendering.get('Styles.SectionTitle.H0.BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.get('Styles.SectionTitle.H0.PaddingTopBottom')
        elif sStyle == "SectionTitleH1":
            iTopMargin = self._oParametersRendering.get('Styles.SectionTitle.H1.TopMargin')
            iBottomMargin = self._oParametersRendering.get('Styles.SectionTitle.H1.BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.get('Styles.SectionTitle.H1.PaddingTopBottom')
        elif sStyle == "SectionTitleH2":
            iTopMargin = self._oParametersRendering.get('Styles.SectionTitle.H2.TopMargin')
            iBottomMargin = self._oParametersRendering.get('Styles.SectionTitle.H2.BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.get('Styles.SectionTitle.H2.PaddingTopBottom')
        else:
            iTopMargin = self._oParametersRendering.get('Styles.Default.TopMargin')
            iBottomMargin = self._oParametersRendering.get('Styles.Default.BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.get('Styles.Default.PaddingTopBottom')
        
        if iStartY == -1:
            iNewHeight = iImgHeight + iTopMargin + iStyleFontSize + iBottomMargin + iPaddingTopBottom*2
            iStartY = iImgHeight + iTopMargin
        else:
            iNewHeight = iImgHeight
        
        oNewImg = self._changeImageSize(oImg, iImgWidth, iNewHeight)
        theNewDraw = ImageDraw.Draw(oNewImg)
        
        # Draw background
        if bFillRow:
            theNewDraw.rectangle((0, iStartY, iImgWidth, iStartY + iStyleFontSize + iPaddingTopBottom*2), fill=tStyleBackColor)

        # Draw Title
        theNewDraw.text((10, iStartY + iPaddingTopBottom), sTitle, tStyleFontColor, font=theStyleFont)
        
        return iStartY, oNewImg

    def _addVisibilityFlagOnRowHeader(self, tColor, iStartY, oImg):
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight

        oNewImg = self._getImageCopy(oImg)
        theNewDraw = ImageDraw.Draw(oNewImg)
        theNewDraw.rectangle((RendererBitmap.iTableWidthObjectLabel - RendererBitmap.iTableVisibilityFlagWidth + 1, iStartY, RendererBitmap.iTableWidthObjectLabel, iStartY + iTableObjectRowHeight), fill=tColor)

        return oNewImg
   
    def getEphemeridesBitmapForPeriod(self, oCalendar, oEphemeridesData):
    
        self.initBuffersFromEphemirides(oEphemeridesData)
    
        theInitialImg = Image.new( 'RGBA', (1800, 1), (0, 0, 0, 255))
        theInitialDraw = ImageDraw.Draw(theInitialImg)

        iNbPlanetsObservable = 0
        iNbLunarFeaturesobservable = 0
        iNbDeepSkyobjectsObservable = 0
        
        bNotificationToBeSent = False
        
        #
        # HEADER
        #
        iTitlePosY, theNewImg = self._addBitmapHeader(oCalendar, theInitialImg)
        
        #
        # PLANETS
        #
        theBackupImg = self._getImageCopy(theNewImg)
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("ThePlanets"), "SectionTitleH1", theBackupImg, True, -1)
        # add header with date and time for Planets
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "Planet", theNewImg)
        # Add objects rows for Planets
        bAtLeastOnePlanetIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(1, self._oParameters.SkyObjects().getCount() +1):
            aSkyObject = self._oParameters.SkyObjects().getObjectByIndex(iObjectIndex)
            if aSkyObject.get("Category") == 'Planetary':
                if not self._bForFavouriteOnly or aSkyObject.get("IsFavourite"):
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(aSkyObject.get("ID")), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if aSkyObject.get("NotifyWhenObservable"):
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._dicRenderingParamMemBuffer["PathToLogFileName"], "     Notification for object  " + aSkyObject.get("ID"))
                    if bIsDisplayed:
                        bAtLeastOnePlanetIsDisplayed = True
        if not bAtLeastOnePlanetIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("ThePlanets") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH1", theNewImg, True, iTitlePosY)
            iNbPlanetsObservable = iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            
        #
        # MOON
        #
        theBackupImg = self._getImageCopy(theNewImg)
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("TheMoon"), "SectionTitleH1", theNewImg, True, -1)
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("MoonVisibility"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Moon
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "Moon", theNewImg)
        # Add object row for Moon
        isMoonDisplayed, isMoonObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject("Moon"), oCalendar, oEphemeridesData, theNewImg)
        if isMoonObservable:
            if self._oParameters.SkyObjects().getObjectByID("Moon").get("NotifyWhenObservable"):
                bNotificationToBeSent = True

        if isMoonDisplayed:
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            theBackupImg = self._getImageCopy(theNewImg)
            # Add Title
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("LunarFeatures"), "SectionTitleH2", theNewImg, False, -1)
            # Add header for Lunar Features
            theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "MoonFeatures", theNewImg)
            # Add rows for Lunar Features
            bAtLeastOneLunarFeatureIsDisplayed = False
            iCount = 0
            for iObjectIndex in range(1, self._oParameters.LunarFeatures().getCount() +1):
                aLunarFeature = self._oParameters.LunarFeatures().getObjectByIndex(iObjectIndex)
                if not self._bForFavouriteOnly or aLunarFeature.get("IsFavourite"):
                    bIsDisplayed, bIsObservable, theNewImg = self._addLunarFeatureRow(aLunarFeature, oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if aLunarFeature.get("NotifyWhenObservable"):
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._dicRenderingParamMemBuffer["PathToLogFileName"], "     Notification for lunar feature  " + aLunarFeature.get("ID"))
                    if bIsDisplayed:
                        bAtLeastOneLunarFeatureIsDisplayed = True
            if not bAtLeastOneLunarFeatureIsDisplayed:
                theNewImg = theBackupImg
            else:
                # Rewrite Title with counters
                iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("LunarFeatures") + " (" + str(iCount) + "/" + str(self._oParameters.LunarFeatures().getCount()) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
                iNbLunarFeaturesobservable = iCount
                # Add legend
                theNewImg = self._addLunarFeatureVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
        else:
            theNewImg = theBackupImg
        
        #
        # DEEP SKY (Favourites)
        #
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("TheDeepSkyObjects"), "SectionTitleH1", theNewImg, True, -1)
        # Favourites
        theBackupImg = self._getImageCopy(theNewImg)
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("FavouriteDeepSkyObjects"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(1, self._oParameters.SkyObjects().getCount() +1):
            aSkyObject = self._oParameters.SkyObjects().getObjectByIndex(iObjectIndex)
            if aSkyObject.get("Category") == 'DeepSky':
                if not self._bForFavouriteOnly or aSkyObject.get("IsFavourite"):
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(aSkyObject.get("ID")), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if aSkyObject.get("NotifyWhenObservable"):
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._dicRenderingParamMemBuffer["PathToLogFileName"], "     Notification for object  " + aSkyObject.get("ID"))
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("FavouriteDeepSkyObjects") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph, True)
        # Other Deep Sky Objects
        theBackupImg = self._getImageCopy(theNewImg)
        if self._bForFavouriteOnly:
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("OtherDeepSkyObjects"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(1, self._oParameters.SkyObjects().getCount() +1):
            aSkyObject = self._oParameters.SkyObjects().getObjectByIndex(iObjectIndex)
            if aSkyObject.get("Category") == 'DeepSky':
                if not aSkyObject.get("IsFavourite"):
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(aSkyObject.get("ID")), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if aSkyObject.get("NotifyWhenObservable"):
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._dicRenderingParamMemBuffer["PathToLogFileName"], "     Notification for object  " + aSkyObject.get("ID"))
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getWithDefault("OtherDeepSkyObjects") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iNbDeepSkyobjectsObservable + iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph, True)
            
        # Save and return bitmap name
        sBitmapName = 'Ephemerides_' + self._oParameters.Runtime().get("Place").get("Name").replace(' ','') + '.' + self._oParametersRendering.get('RenderingOptions.BitmapExtension')
        theNewImg.save(self._sRelativeFolderForBitmaps + sBitmapName, self._oParametersRendering.get('RenderingOptions.BitmapType'))
        Tools.logToTrace(self._dicRenderingParamMemBuffer["PathToLogFileName"], "     Bitmap generated: " + self._sRelativeFolderForBitmaps + sBitmapName)
        
        # Return bitmap URL and size
        iWidth, iHeight = theNewImg.size
        return iWidth, iHeight, self._sURLFolderForBitmaps + sBitmapName, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, self._sRelativeFolderForBitmaps + sBitmapName, sBitmapName, bNotificationToBeSent

    def getHTML(self, oCalendar, oEphemeridesData):
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        sDomain = self._oParameters.Runtime().get('NightlyBatch.Domain')
        sHTML = self.getHTMLHeaderComment(oCalendar) + "\n"
        sHTML += '<HTML>' + "\n"
        sHTML += "\n"
        sHTML += '    <HEAD>' + "\n"
        sHTML += '        <TITLE>'+ self._oParameters.Localization().getWithDefault("HTMLPageTitle") + '</TITLE>' + "\n"
        sHTML += '        <LINK rel="icon" href="http://' + sDomain + '/favicon.png">'  + "\n"
        sHTML += '        <BASE href="">' + "\n"
        sHTML += '        <LINK rel="stylesheet" href="http://' + sDomain + '/AstroNotif.css">' + "\n"
        sHTML += '        <META charset="UTF-8">' + "\n"
        sHTML += '    </HEAD>' + "\n"
        sHTML += "\n"
        sHTML += '    <BODY>' + "\n"

        iWidth, iHeight, sBitmapNameURL, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilenameWithPath, sBitmapFilename, bNotificationToBeSent = self.getEphemeridesBitmapForPeriod(oCalendar, oEphemeridesData)
        
        sHTML += '        <A href="http://' + sDomain + '" target="_blank">'   + "\n"
        sHTML += '            <IMG class="EphemeridesBitmap" src="' + sBitmapNameURL + '" alt="' +  self._oParameters.Localization().getWithDefault("EphemerisFor") + " " + oCalendar.getFormattedLocalDateForSlot(0,self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"]) +  '" height="' + str(iHeight) + '" width="' + str(iWidth) + '">' + "\n"
        sHTML += '        </A>' + "\n"
        sHTML += '    </BODY>' + "\n"
        sHTML += "\n"
        sHTML += '</HTML>' + "\n"
        return sHTML, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilenameWithPath, sBitmapFilename, bNotificationToBeSent

    def getHTMLHeaderComment(self, oCalendar):
        return ('<!-- Parameters... Date:'  + oCalendar.getLocalStartDate() + '  - Place:'  + self._oParameters.Runtime().get("Place").get("Name") + ' - Longitude:'  + str(self._oParameters.Runtime().get("Place").get("Longitude")) + ' - Latitude:'  + str(self._oParameters.Runtime().get("Place").get("Latitude")) + '  -->'  )
                
    def test(self):
        img = Image.new( 'RGB', (200, 50), "black") # create a new black image
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = self._getFont()
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, 0),"Sample Text" + " --> " + str(draw.textsize("Sample Text", font=self._getFont("ObjectName"))[0]),(255,255,255),font=self._getFont("ObjectName"))
        draw.text((0, 20),"Sample Text:  00 01 02 03 04 05 06 07" + " --> " + str(draw.textsize("Sample Text:  00 01 02 03 04 05 06 07", font=self._getFont("RowHeaderTime"))[0]),(255,255,255),font=self._getFont("RowHeaderTime"))
        finalImg = img.crop((0, 0, 500, 300))
        finalDraw = ImageDraw.Draw(finalImg)
        # Draw grid 10x10
        for iX in range (10,  271, 10 ):
            for iY in range (0,  270, 10 ):
                finalDraw.rectangle((iX, iY, iX, iY), fill=(127, 127, 127))
        finalDraw.text((300, 200),"Sample Text" + " --> " + str(draw.textsize("Sample Text", font=self._getFont("ObjectName"))[0]),(255,255,255),font=self._getFont("ObjectName"))
        finalDraw.text((300, 220),"Sample Text:  00 01 02 03 04 05 06 07" + " --> " + str(draw.textsize("Sample Text:  00 01 02 03 04 05 06 07", font=self._getFont("RowHeaderTime"))[0]),(255,255,255),font=self._getFont("RowHeaderTime"))
        finalImg.save('bitmapRenderer_sample.jpg')
                
    def _addVisibilityMapLegend(self, oImg, iPastePosX, bWithStatusDifficultMoonLight = False):
        # Add legend at bottom of the bitmap (resized to add the legend)
        
        iImgWidth, iImgHeight = oImg.size
        imgLegend = self._changeImageSize(oImg, iImgWidth, iImgHeight + 30)

        drawLegend = ImageDraw.Draw(imgLegend)
        
        iPosY = iImgHeight + 5
        iPosX = iPastePosX + 10
        
        iHeightText = self._getFontSize("Legend")

        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusImpossible"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusImpossible"])
        drawLegend.text((iPosX + 25, iPosY),  self._oParameters.Localization().getWithDefault("ImpossibleDuringDay"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("ImpossibleDuringDay"), font=self._getFont("Legend"))[0] + 25

#        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.get('ObjectVisibilityGraph.LineColorForStatus.Below'))
#        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.get('ObjectVisibilityGraph.LineColorForStatus.Below'))
#        drawLegend.text((iPosX + 25, iPosY),  self._oParameters.Localization().getWithDefault("BelowHorizon"), (255,255,255), font=self._getFont("Legend"))
#        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("BelowHorizon"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusHidden"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusHidden"])
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("HiddenByObstacle"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("HiddenByObstacle"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusVeryLow"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusVeryLow"])
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("VeryLow"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("VeryLow"), font=self._getFont("Legend"))[0] + 25
        
        if bWithStatusDifficultMoonLight:
            drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusDifficultMoonlight"])
            drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusDifficultMoonlight"])
            drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("DifficultMoonlight"), (255,255,255), font=self._getFont("Legend"))
            iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("DifficultMoonlight"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusLow"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusLow"])
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("Low"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("Low"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusDifficult"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusDifficult"])
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("DifficultToSee"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("DifficultToSee"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusGood"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusGood"])
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("GoodVisibility"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("GoodVisibility"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusUnknown"])
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._dicRenderingParamMemBuffer["LineColorForStatusUnknown"])
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("Unknown"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("Unknown"), font=self._getFont("Legend"))[0] + 25
        
        return imgLegend          
                
    def _addLunarFeatureVisibilityMapLegend(self, oImg, iPastePosX):
        # Add legend at bottom of the bitmap (resized to add the legend)
        
        iImgWidth, iImgHeight = oImg.size
        imgLegend = self._changeImageSize(oImg, iImgWidth, iImgHeight + 30)

        drawLegend = ImageDraw.Draw(imgLegend)
        
        iPosY = iImgHeight + 5
        iPosX = iPastePosX + 10
        
        iHeightText = self._getFontSize("Legend")

        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.SunBelowHorizon'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.SunBelowHorizon'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("AtFeatureSunBelowHorizon"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("AtFeatureSunBelowHorizon"), font=self._getFont("Legend"))[0] + 25
        
        for iOcc in range(20, 0, -1):
            fAlt = self._dicRenderingParamMemBuffer["MaximumLunarFeatureSunAltitude"] / 20.0 * float(iOcc)
            tColor = (255, 127 + int(fAlt / self._dicRenderingParamMemBuffer["MaximumLunarFeatureSunAltitude"] * 128.0), int(fAlt / self._dicRenderingParamMemBuffer["MaximumLunarFeatureSunAltitude"] * 255.0))
            drawLegend.line((iPosX + iOcc, iPosY + (iHeightText / 2), iPosX + iOcc, iPosY + (iHeightText / 2)), fill=tColor)
            drawLegend.line((iPosX + iOcc, iPosY + (iHeightText / 2 + 1), iPosX + iOcc, iPosY + (iHeightText / 2 + 1)), fill=tColor)
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("Observable"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("Observable"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.Good'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.Good'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("NearTerminatorGoodVisibility"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("NearTerminatorGoodVisibility"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.SunTooHigh'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.get('LunarFeatureVisibilityGraph.ColorForStatus.SunTooHigh'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getWithDefault("AtFeatureSunTooHigh"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getWithDefault("AtFeatureSunTooHigh"), font=self._getFont("Legend"))[0] + 25
        
        return imgLegend          

        
        
            
    def _addBitmapHeader(self, oCalendar, oImg):
        # Get Style
        iStyleFontSizeH0, theStyleFontH0, tStyleFontColorH0, tStyleBackColorH0 = self._getStyle("BitmapHeaderH0")
        iStyleFontSizeH1, theStyleFontH1, tStyleFontColorH1, tStyleBackColorH1 = self._getStyle("BitmapHeaderH1")
        iStyleFontSizeH2, theStyleFontH2, tStyleFontColorH2, tStyleBackColorH2 = self._getStyle("BitmapHeaderH2")

        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        iTopMarginH0 = self._oParametersRendering.get('Styles.BitmapHeader.H0.TopMargin')
        iBottomMarginH0 = self._oParametersRendering.get('Styles.BitmapHeader.H0.BottomMargin')
        iPaddingTopBottomH0 = self._oParametersRendering.get('Styles.BitmapHeader.H0.PaddingTopBottom')
        iTopMarginH1 = self._oParametersRendering.get('Styles.BitmapHeader.H1.TopMargin')
        iBottomMarginH1 = self._oParametersRendering.get('Styles.BitmapHeader.H1.BottomMargin')
        iPaddingTopBottomH1 = self._oParametersRendering.get('Styles.BitmapHeader.H1.PaddingTopBottom')
        iTopMarginH2 = self._oParametersRendering.get('Styles.BitmapHeader.H2.TopMargin')
        iBottomMarginH2 = self._oParametersRendering.get('Styles.BitmapHeader.H2.BottomMargin')
        iPaddingTopBottomH2 = self._oParametersRendering.get('Styles.BitmapHeader.H2.PaddingTopBottom')
        
        iNewHeight = iImgHeight + iTopMarginH0 + iStyleFontSizeH0 + iBottomMarginH0 + iPaddingTopBottomH0*2 + iTopMarginH1 + iStyleFontSizeH1 + iBottomMarginH1 + iPaddingTopBottomH1*2 + iTopMarginH2 + iStyleFontSizeH2 + iBottomMarginH2 + iPaddingTopBottomH2*2
        
        oNewImg = self._changeImageSize(oImg, iImgWidth, iNewHeight)
        theNewDraw = ImageDraw.Draw(oNewImg) 
        
        # Draw Row 0
        iStartY = iTopMarginH0 + iPaddingTopBottomH0
        sText0 = self._oParameters.Localization().getWithDefault("EphemerisFor") + ' ' + oCalendar.getFormattedLocalDateForSlot(0,self._dicRenderingParamMemBuffer["RenderingOptions.NumberOfMinutesPerSlot"])
        theNewDraw.text((10, iStartY), sText0, tStyleFontColorH0, font=theStyleFontH0)
        iStartY = iStartY + iStyleFontSizeH0 + iPaddingTopBottomH0 + iBottomMarginH0

        # Draw Row 1
        iStartY = iStartY + iTopMarginH1 + iPaddingTopBottomH1
        sText1 = self._oParameters.Localization().getWithDefault("Place") + ': ' + self._oParameters.Runtime().get("Place").get("Name")
        theNewDraw.text((10, iStartY), sText1, tStyleFontColorH1, font=theStyleFontH1)
        iStartY = iStartY + iStyleFontSizeH1 + iPaddingTopBottomH1 + iBottomMarginH1
        
        # Draw Row 2
        iStartY = iStartY + iTopMarginH2 + iPaddingTopBottomH2
        sText2 = self._oParameters.Localization().getWithDefault("CalculusFor") + ' ' + (datetime.now()).strftime("%d/%m/%Y %H:%M") + ' ' + self._oParameters.Localization().getWithDefault("By") + ' AstroNotifPython ' + self._oParameters.Runtime().get('Global.CurrentVersion') + " " + self._oParameters.Localization().getWithDefault("RunningOn") + " " + platform.node()
        theNewDraw.text((10, iStartY), sText2, tStyleFontColorH2, font=theStyleFontH2)
        iStartY = iStartY + iStyleFontSizeH2 + iPaddingTopBottomH2 + iBottomMarginH2
        
        return iStartY, oNewImg

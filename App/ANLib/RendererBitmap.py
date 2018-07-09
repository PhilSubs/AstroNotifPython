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
from ParametersRendering import ParametersRendering
from ParametersLocalization import ParametersLocalization


class RendererBitmap(toolObjectSerializable):
    iLeftLabelWidthInPx = 100
    iHourSlotWidthInPx = 16
    iAltitudeRowHeight = 3
    sFontDefaultName = "Resources/Fonts/arial.ttf"
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
        self._oParametersRendering = ParametersRendering()
        self._oParameters = oParameters
        self._oParametersLocalization = ParametersLocalization(self._oParameters.getLanguage())

    def _getBitmapColorForObjectAltitudeDependingOnSunAltitude(self, sObjectVisibilityStatus):
        tColor = self._oParametersRendering.getColorObjectVisibilityStatus(sObjectVisibilityStatus)
        return tColor

    def _getBitmapColorforSunAltitude(self, fSunAltitude):
        if fSunAltitude < -18.0:
            tColor = self._oParametersRendering.getColorSunAltitude('MoreThan18DegBelow')
        elif fSunAltitude < -12.0:
            tColor = self._oParametersRendering.getColorSunAltitude('12To18DegBelow')
        elif fSunAltitude < -6.0:
            tColor = self._oParametersRendering.getColorSunAltitude('06To12DegBelow')
        elif fSunAltitude < -0.0:
            tColor = self._oParametersRendering.getColorSunAltitude('00To06DegBelow')
        elif fSunAltitude < 6.0:
            tColor = self._oParametersRendering.getColorSunAltitude('00To06DegAbove')
        elif fSunAltitude < 12.0:
            tColor = self._oParametersRendering.getColorSunAltitude('06To12DegAbove')
        else:
            tColor = self._oParametersRendering.getColorSunAltitude('MoreThan12DegAbove')
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
        iStyleFontSize = self._oParametersRendering.getStyles('DefaultFontSize')
        sFontDirectory = self._oParametersRendering.getStyles('DefaultFontDirectory')
        sFont = sFontDirectory + self._oParametersRendering.getStyles('DefaultFont')
        tStyleFontColor = self._oParametersRendering.getStyles('DefaultFontColor')
        tStyleBackColor = self._oParametersRendering.getStyles('DefaultBackColor')
        
        # Style overlap
        if sStyle == "GMTWarning":
            iStyleFontSize = self._oParametersRendering.getStyles('GMTWarningFontSize')
            sFont = sFontDirectory + self._oParametersRendering.getStyles('GMTWarningFont')
        elif sStyle == "Legend":
            iStyleFontSize = self._oParametersRendering.getStyles('LegendFontSize')
            sFont = sFontDirectory + self._oParametersRendering.getStyles('LegendFont')
        elif sStyle == "RowHeaderDate":
            iStyleFontSize = self._oParametersRendering.getStyles('RowHeaderDateFontSize')
            sFont = sFontDirectory + self._oParametersRendering.getStyles('RowHeaderDateFont')
        elif sStyle == "RowHeaderTime":
            iStyleFontSize = self._oParametersRendering.getStyles('RowHeaderTimeFontSize')
        elif sStyle == "ObjectName":
            iStyleFontSize = self._oParametersRendering.getStyles('ObjectNameFontSize')
        elif sStyle == "ObjectData":
            iStyleFontSize = self._oParametersRendering.getStyles('ObjectDataFontSize')
        elif sStyle == "ObjectAdditionalDailyData":
            iStyleFontSize = self._oParametersRendering.getStyles('ObjectAdditionalDailyDataFontSize')
        elif sStyle == "SectionTitleH0":
            iStyleFontSize = self._oParametersRendering.getStyles('SectionTitleH0FontSize')
            tStyleBackColor = self._oParametersRendering.getStyles('SectionTitleH0BackColor')
            tStyleFontColor = self._oParametersRendering.getStyles('SectionTitleH0FontColor')
        elif sStyle == "SectionTitleH1":
            iStyleFontSize = self._oParametersRendering.getStyles('SectionTitleH1FontSize')
            tStyleBackColor = self._oParametersRendering.getStyles('SectionTitleH1BackColor')
            tStyleFontColor = self._oParametersRendering.getStyles('SectionTitleH1FontColor')
        elif sStyle == "SectionTitleH2":
            iStyleFontSize = self._oParametersRendering.getStyles('SectionTitleH2FontSize')
            tStyleFontColor = self._oParametersRendering.getStyles('SectionTitleH2FontColor')
        elif sStyle == "LunarFeatureName":
            iStyleFontSize = self._oParametersRendering.getStyles('LunarFeatureNameFontSize')
        elif sStyle == "LunarFeatureData":
            iStyleFontSize = self._oParametersRendering.getStyles('LunarFeatureDataFontSize')
            sFont = sFontDirectory + self._oParametersRendering.getStyles('LunarFeatureDataFont')
        
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
        iNbSlotsPerDay = (1440 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())

        sComment1 = oLunarFeatureObject.getType() + "    -    " + self._oParametersLocalization.getLabel("LongitudeAbrev") + ": " + str(oLunarFeatureObject.getLongitude()) + "  -  "  + self._oParametersLocalization.getLabel("LatitudeAbrev") + ": " + str(oLunarFeatureObject.getLatitude())
        sComment2 = ""
        sComment3 = ""
        sFormatForFloatValues = "{0:.1f}"
        if oLunarFeatureObject.getDiameter() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParametersLocalization.getLabel("Diameter") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getDiameter()) + " " + self._oParametersLocalization.getLabel("KilometerAbrev")
        if oLunarFeatureObject.getDepth() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParametersLocalization.getLabel("Depth") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getDepth()) + " " + self._oParametersLocalization.getLabel("KilometerAbrev")
        if oLunarFeatureObject.getHeight() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParametersLocalization.getLabel("Height") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getHeight()) + " " + self._oParametersLocalization.getLabel("KilometerAbrev")
        if oLunarFeatureObject.getLength() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParametersLocalization.getLabel("Length") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getLength()) + " " + self._oParametersLocalization.getLabel("KilometerAbrev")
        if oLunarFeatureObject.getBreadth() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParametersLocalization.getLabel("Breadth") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getBreadth()) + " " + self._oParametersLocalization.getLabel("KilometerAbrev")
        if oLunarFeatureObject.getRukl() != "": sComment3 += ("  -  " if len(sComment3) > 0 else "") + self._oParametersLocalization.getLabel("Rukl") + ": " + oLunarFeatureObject.getRukl()
        iRowPositionY, theNewImg = self._addLunarFeatureRowHeader(oLunarFeatureObject.getName(), sComment1, sComment2, sComment3, oImg)
        iTmpX, iTmpY = theNewImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayIsObservable = False
        bAtLeastOneDayIsNotObservable = False
        for iDaySlot in range (0,  self._oParameters.getDisplayNumberOfSlotsForMoonFeatures(), iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + self._oParameters.getDisplayDaySlotForDataInfo()
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
            theNewImg = self._addMoonMinimapBitmap( oEphemeridesData.getEphemerideDataObject("Moon").getPhaseForSlot(iDataSlot), oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), theNewImg, iPosXMoonMap, iPosYMoonMap, iBitmapSize)

        if bAtLeastOneDayToBeDisplayed:
            if not bAtLeastOneDayIsNotObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
            else:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
        else:
            theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
                
#        if not bAtLeastOneDayIsNotObservable:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
#        elif not bAtLeastOneDayIsObservable:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
#        else:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
            
        if bAtLeastOneDayToBeDisplayed:
            return True, bAtLeastOneDayIsObservable, theNewImg
        else:
            return False, bAtLeastOneDayIsObservable, oImg
                
    def _addLunarFeatureRowHeader(self, sObjectName, sComment1,  sComment2,  sComment3, oImg):
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
        theNewDraw.text((iStartX + 3, iStartY + 5), sObjectName, (0,0,0), font=self._getFont("LunarFeatureName"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), sComment1, (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), sComment2, (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 + 12), sComment3, (0,0,0), font=self._getFont("LunarFeatureData"))

        return iStartY, oNewImg

    def _addLunarFeatureVisibilityBitmapForDay(self, iStartSlot, iEndSlot, iDataSlot, oLunarFeatureObject, oCalendar, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
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
        for iSlot in range(iStartSlot, iEndSlot):
            fSunAltitudeOverFeature = MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iSlot))
            sMoonVisibilityStatus = oEphemeridesData.getObjectVisibilityStatusForSlot("Moon", iSlot, self._oParameters)
            if fSunAltitudeOverFeature > 0.0 and fSunAltitudeOverFeature <= self._oParameters.getObservationMaximumLunarFeatureSunAltitude():
                bIsObservable = True
            fLongitudeMin = (oLunarFeatureObject.getLongitudeMin() - self._oParameters.getObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg() + 360.0) % 360.0
            fLongitudeMax = (oLunarFeatureObject.getLongitudeMax() + self._oParameters.getObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg() + 360.0) % 360.0
            fTerminatorLongitudeRise = (oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot) - 90.0) % 360.0
            fTerminatorLongitudeSet = (oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot) + 90.0) % 360.0

            if fLongitudeMax < fLongitudeMin: fLongitudeMax += 360.0
            if fTerminatorLongitudeRise < fLongitudeMin: fTerminatorLongitudeRise += 360.0
            if fTerminatorLongitudeSet < fLongitudeMin: fTerminatorLongitudeSet += 360.0
            
            bIsTerminatorNearFeature = ((fTerminatorLongitudeRise >= fLongitudeMin and fTerminatorLongitudeRise <= fLongitudeMax) or (fTerminatorLongitudeSet >= fLongitudeMin and fTerminatorLongitudeSet <= fLongitudeMax))
            
            
            iTransparency = 255
            if sMoonVisibilityStatus == "Below" or sMoonVisibilityStatus == "Hidden" or sMoonVisibilityStatus == "Impossible" :
                iTransparency = 250
            if self._oParameters.getObservationShowWhenTerminatorIsOnLunarFeature() and bIsTerminatorNearFeature:
                tColor = self._oParametersRendering.getColorLunarFeatureVisibility('Good')
            elif fSunAltitudeOverFeature <= 0.0:  
                tColor = self._oParametersRendering.getColorLunarFeatureVisibility('SunBelowHorizon')
            elif fSunAltitudeOverFeature >= self._oParameters.getObservationMaximumLunarFeatureSunAltitude():
                tColor = self._oParametersRendering.getColorLunarFeatureVisibility('SunTooHigh')
            else:
                tColor = (255, 127 + int(fSunAltitudeOverFeature / self._oParameters.getObservationMaximumLunarFeatureSunAltitude() * 128.0), int(fSunAltitudeOverFeature / self._oParameters.getObservationMaximumLunarFeatureSunAltitude() * 255.0))
            tColor = (tColor[0], tColor[1], tColor[2], iTransparency)

                    
            x1 = iBorderStartX + 1 + (iSlot - iStartSlot) * iSlotWidthInPx
            x2 = x1 + iSlotWidthInPx - 1
            y1 = iBorderStartY + 1
            y2 = iBorderEndY - 1 - RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
            theNewDraw.rectangle((x1, y1, x2, y2), fill=tColor)

        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127, 255))

        # Additional data
        sAdditionalText = 'At ' + oCalendar.getTimeForSlotAsHHMM(iDataSlot, self._oParameters.getDisplayNumberOfMinutesPerSlot()) + ':   Sun Altitude: ' + str(int(round(MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot))))) + '  Sun Azimut: ' + str(int(round(MeeusAlgorithms.getSunAzimutFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot)))))
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255, 255), font=self._getFont("ObjectAdditionalDailyData"))
        
        bToBeDisplayed = (bIsObservable or self._oParameters.getObservationAlways())
        if bToBeDisplayed:        
            return True, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
                
    def _addMoonMinimapBitmap(self, iPhase, fLongitude, fLatitude, oImg, iPosX, iPosY, iBitmapSize):
        iIndicatorSizeInPx = 3
        
        tColorMoonMapBorder = self._oParametersRendering.getColorMoonMiniMap('Border')
        tColorMoonMapBackground = self._oParametersRendering.getColorMoonMiniMap('Background')
        tColorMoonMapLight = self._oParametersRendering.getColorMoonMiniMap('Light')
        tColorMoonMapDark = self._oParametersRendering.getColorMoonMiniMap('Dark')
        
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
        tColorBackground = self._oParametersRendering.getColorHeliocentricGraph('Background')
        tColorLines = self._oParametersRendering.getColorHeliocentricGraph('Lines')
        tColorSun = self._oParametersRendering.getColorHeliocentricGraph('Sun')
        tColorEarth = self._oParametersRendering.getColorHeliocentricGraph('Earth')
        tColorPlanet = self._oParametersRendering.getColorHeliocentricGraph('Planet')

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
        iNbSlotsPerDay = (1440 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        bIsObservable = False
        sHTMLObjectRow = ""
        if (oEphemeridesDataObject.getType() == "Moon"):
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, "", "", "", oImg)
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForMoon()
        elif (oEphemeridesDataObject.getType() == "Planet"):
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForPlanets()
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(0)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0))) + " " + self._oParametersLocalization.getLabel("DegreesAbev")
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (' + self._oParametersLocalization.getLabel("NearConjonction") + ')'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (' + self._oParametersLocalization.getLabel("NearOpposition") + ')'
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, self._oParametersLocalization.getLabel("Distance") + ": " +  str(int(round(oEphemeridesDataObject.getDistanceForSlot(0) * 149.600000, 1))) + ' ' + self._oParametersLocalization.getLabel("MillionKilometersAbrev"), self._oParametersLocalization.getLabel("PositionAngleAbrev") + ": " +  sMeanLongComment, self._oParametersLocalization.getLabel("ApparentDiameterAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getApparentDiameterInArcSecForSlot(0), 1))) + ' ' + self._oParametersLocalization.getLabel("SecondOfAngleAbrev"), oImg)
            # add heliocentric schema
            theNewImg = self._addHeliocentricBitmap(oEphemeridesDataObject.getName(), oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0, oEphemeridesDataObject.getMeanLongForSlot(0), iRowPositionY, theNewImg)
        else:
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForDeepSky()
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, self._oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getType(), self._oParametersLocalization.getLabel("RightAscensionAbrev") + ": " + CommonAstroFormulaes.getHMSFromDeg(self._oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getRA()) + "    " + self._oParametersLocalization.getLabel("DeclinationAbrev") + ": " +  str(round(self._oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDec(),2)), self._oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getComment1(), oImg)
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayObservable = False
        bAtLeastOneDayNotObservable = False
        for iDaySlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + self._oParameters.getDisplayDaySlotForDataInfo()
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
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
                if oEphemeridesDataObject.getID() == "Jupiter":
                    print "==> Observable  " + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[0]) + "," + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[1]) + "," + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[2])
            else:            
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
                if oEphemeridesDataObject.getID() == "Jupiter":
                    print "==> AtLEastOneDayObservable  " + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[0]) + "," + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[1]) + "," + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[2])
        else:
            theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
            if oEphemeridesDataObject.getID() == "Jupiter":
                print "==> NotObservable  " + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[0]) + "," + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[1]) + "," + str(self._oParametersRendering.getColorVisibilityFlags('Observable')[2])
            
#        if not bAtLeastOneDayNotObservable:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
#        elif not bAtLeastOneDayObservable:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
#        else:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
        
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

        theNewDraw.text((iStartX + 3, iStartY), oEphemeridesDataObject.getName(), (0,0,0), font=self._getFont("ObjectName"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), Tools.removeHTMLTags(sObjectDataRow1), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), Tools.removeHTMLTags(sObjectDataRow2), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 * 2), Tools.removeHTMLTags(sObjectDataRow3), (0,0,0), font=self._getFont("ObjectData"))
        
        if oEphemeridesDataObject.getPictureName() <> "":
            imgObjectThumbnail = Image.open(Tools.get_ResourceSubfolder_path("Bitmaps") + oEphemeridesDataObject.getPictureName())
            oNewImg.paste(imgObjectThumbnail, (iStartX + RendererBitmap.iTableWidthObjectLabel - 50 - RendererBitmap.iTableVisibilityFlagWidth - 2, iStartY + 2 ))
        
        return iStartY, oNewImg

    def _addObjectVisibilityBitmapForDay(self, oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
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
                    x2 = x1 + iSlotWidthInPx - 1
                    tColor = self._getBitmapColorforSunAltitude(oEphemeridesData.getSunAltitudeForSlot(iSlot))
                    theNewDraw.rectangle((iRowPositionX - 1 + x1, iRowPositionY + 1 + y1, iRowPositionX - 1 + x2, iRowPositionY + 1 + y2), fill=tColor)
            for iSlot in range(iStartSlot, iEndSlot):
                x = (iSlot - iStartSlot) * iSlotWidthInPx + (iSlotWidthInPx/2) - 1
                y = iBitmapHeight - int(float( oEphemeridesDataObject.getAltitudeForSlot(iSlot) / 90.0) * float(iBitmapHeight))
                if oEphemeridesDataObject.getAltitudeForSlot(iSlot) > 0:
                    sObjectVisibilityStatus = oEphemeridesData.getObjectVisibilityStatusForSlot(oEphemeridesDataObject.getID(), iSlot, self._oParameters)
                    tColor = self._getBitmapColorForObjectAltitudeDependingOnSunAltitude(sObjectVisibilityStatus)
                    bIsObservable = ((sObjectVisibilityStatus == "Good") or bIsObservable)
                    if iPrevX > -1 and iPrevY > -1:
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY, iRowPositionX - 1 + x, iRowPositionY + 1 + y), fill=tColor)
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY -1, iRowPositionX - 1 + x, iRowPositionY + 1 + y -1 ), fill=tColor)
                iPrevX = x
                iPrevY = y
        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127))
        
        # delete useless objects
        del theNewDraw        

        bIsDisplayed = (bIsObservable or self._oParameters.getObservationAlways() or (self._oParameters.getObservationForceDisplayPlanetMoon() and oEphemeridesDataObject.getCategory() == "Planetary"))
        if bIsDisplayed:        
            return bIsDisplayed, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
        
    def _addObjectVisibilityInfoForDay(self, oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, iDataSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        bIsObservable = False
        iNbSlotsPerDay = (1440 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        
        bIsDisplayed, bIsObservable, theNewImg = self._addObjectVisibilityBitmapForDay(oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX + 3, iRowPositionY)
        if oEphemeridesDataObject.getID() == "Jupiter":
            print "_addObjectVisibilityBitmapForDay   bIsDisplayed:" + str(bIsDisplayed) + ", bIsObservable:" + str(bIsObservable)

        if oEphemeridesDataObject.getType() == "Planet":
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(iStartSlot) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(iStartSlot)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0)))
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' ('  + self._oParametersLocalization.getLabel("NearConjonction") + ')'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' ('  + self._oParametersLocalization.getLabel("NearOpposition") + ')'
            sAdditionalText = self._oParametersLocalization.getLabel("CulminationAbrev") + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', ' + self._oParametersLocalization.getLabel("Azimut") + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))
        elif oEphemeridesDataObject.getType() == "Moon":
            sAdditionalText = self._oParametersLocalization.getLabel("A") + ' ' + oCalendar.getTimeForSlotAsHHMM(iDataSlot, self._oParameters.getDisplayNumberOfMinutesPerSlot()) + '  ' + self._oParametersLocalization.getLabel("GMT") + ':  ' + self._oParametersLocalization.getLabel("DistanceAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getDistanceForSlot(iDataSlot)))) + ' ' + self._oParametersLocalization.getLabel("KilometerAbrev") + ', ' + self._oParametersLocalization.getLabel("Phase") + ': ' + str(int(round(abs(oEphemeridesDataObject.getPhaseForSlot(iDataSlot))))) + ', ' + self._oParametersLocalization.getLabel("IlluminationAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getIlluminationForSlot(iDataSlot) * 100))) + '%, ' + self._oParametersLocalization.getLabel("ColongitudeAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getColongitudeForSlot(iDataSlot)))) + ' -=- ' + self._oParametersLocalization.getLabel("CulminationAbrev") + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', ' + self._oParametersLocalization.getLabel("Azimut") + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))
        else:
            sAdditionalText = self._oParametersLocalization.getLabel("CulminationAbrev") + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', ' + self._oParametersLocalization.getLabel("Azimut") + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))

        theNewDraw = ImageDraw.Draw(theNewImg)
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255), font=self._getFont("ObjectAdditionalDailyData"))
    
        return bIsDisplayed, bIsObservable, theNewImg
            
    def _addObjectVisibilityTableHeader(self, oCalendar, oEphemeridesData, sType, oImg):
        iNbSlotsPerDay = (1440 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iNbSlotsPerHour = 60 / self._oParameters.getDisplayNumberOfMinutesPerSlot()
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        iTableHeaderHeight = RendererBitmap.iTableHeaderRowHeight * 2 + RendererBitmap.iTableHeaderRowInterline # 2 rows + 5 pixel in between
        if sType == "Moon":
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForMoon()
        elif sType == "MoonFeatures":
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForMoonFeatures()
        elif sType == "Planet":
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForPlanets()
        else:
            iMaxSlot = self._oParameters.getDisplayNumberOfSlotsForDeepSky()
        
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
        for iSlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            iDay = int(iSlot / iNbSlotsPerDay)
            iHeaderStartX = iStartX + (iDay * iNbSlotsPerDay * iSlotWidthInPx) + (iDay * RendererBitmap.iTableSpaceBetweenDays)
            iHeaderEndX = iHeaderStartX + (iNbSlotsPerDay * iSlotWidthInPx)
            iHeaderStartY = iStartY
            iHeaderEndY = iHeaderStartY + iTableHeaderHeight - 1
            theNewDraw.rectangle((iHeaderStartX, iHeaderStartY, iHeaderEndX, iHeaderEndY), fill=(255, 255, 255))
            theNewDraw.rectangle((iHeaderStartX + 1, iHeaderStartY + 1, iHeaderEndX - 1, iHeaderEndY - 1), fill=(0, 0, 0))
            # Display date
            theNewDraw.text((iHeaderStartX + 3, iHeaderStartY + 3), oCalendar.getFormattedDateForSlot(iSlot,self._oParameters.getDisplayNumberOfMinutesPerSlot()), (255,255,255), font=self._getFont("RowHeaderDate"))
            # Display GMT warning
            sLabel = self._oParametersLocalization.getLabel("GMTWarning")
            theNewDraw.text((iHeaderEndX - 3 - theNewDraw.textsize(sLabel, font=self._getFont("GMTWarning"))[0], iHeaderStartY + 3), sLabel, (255,255,255), font=self._getFont("GMTWarning"))            
            # Display hours
            for iDaySlot in range (iSlot,  iSlot + iNbSlotsPerDay, iNbSlotsPerHour ):
                theNewDraw.text((iHeaderStartX + 3 + (iDaySlot - iSlot) * iSlotWidthInPx, iStartY + RendererBitmap.iTableHeaderRowHeight + 4 + RendererBitmap.iTableHeaderRowInterline), oCalendar.getTimeForSlot(iDaySlot, self._oParameters.getDisplayNumberOfMinutesPerSlot())[0:2], (255,255,255), font=self._getFont("RowHeaderTime"))
        
        return oNewImg

    def _addTitleForSection(self, sTitle, sStyle, oImg, bFillRow, iStartY):
        # Get Style
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle(sStyle)

        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        if sStyle == "SectionTitleH0":
            iTopMargin = self._oParametersRendering.getStyles('SectionTitleH0TopMargin')
            iBottomMargin = self._oParametersRendering.getStyles('SectionTitleH0BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.getStyles('SectionTitleH0PaddingTopBottom')
        elif sStyle == "SectionTitleH1":
            iTopMargin = self._oParametersRendering.getStyles('SectionTitleH1TopMargin')
            iBottomMargin = self._oParametersRendering.getStyles('SectionTitleH1BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.getStyles('SectionTitleH1PaddingTopBottom')
        elif sStyle == "SectionTitleH2":
            iTopMargin = self._oParametersRendering.getStyles('SectionTitleH2TopMargin')
            iBottomMargin = self._oParametersRendering.getStyles('SectionTitleH2BottomMargin')
            iPaddingTopBottom = self._oParametersRendering.getStyles('SectionTitleH2PaddingTopBottom')
        else:
            iTopMargin = self._oParametersRendering.getStyles('DefaultTopMargin')
            iBottomMargin = self._oParametersRendering.getStyles('DefaultBottomMargin')
            iPaddingTopBottom = self._oParametersRendering.getStyles('DefaultPaddingTopBottom')
        
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
        theInitialImg = Image.new( 'RGBA', (1800, 1), (0, 0, 0, 255))
        theInitialDraw = ImageDraw.Draw(theInitialImg)

        iNbPlanetsObservable = 0
        iNbLunarFeaturesobservable = 0
        iNbDeepSkyobjectsObservable = 0
        
        #
        # PLANETS
        #
        theBackupImg = self._getImageCopy(theInitialImg)
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("ThePlanets"), "SectionTitleH1", theBackupImg, True, -1)
        # add header with date and time for Planets
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "Planet", theNewImg)
        # Add objects rows for Planets
        bAtLeastOnePlanetIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, self._oParameters.getSkyObjects().getCount()):
            if self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getType() == 'Planet':
                if not self._bForFavouriteOnly or self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOnePlanetIsDisplayed = True
        if not bAtLeastOnePlanetIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("ThePlanets") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH1", theNewImg, True, iTitlePosY)
            iNbPlanetsObservable = iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            
        #
        # MOON
        #
        theBackupImg = self._getImageCopy(theNewImg)
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("TheMoon"), "SectionTitleH1", theNewImg, True, -1)
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("MoonVisibility"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Moon
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "Moon", theNewImg)
        # Add object row for Moon
        isMoonDisplayed, isMoonObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject("Moon"), oCalendar, oEphemeridesData, theNewImg)
        if isMoonDisplayed:
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            theBackupImg = self._getImageCopy(theNewImg)
            # Add Title
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("LunarFeatures"), "SectionTitleH2", theNewImg, False, -1)
            # Add header for Lunar Features
            theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "MoonFeatures", theNewImg)
            # Add rows for Lunar Features
            bAtLeastOneLunarFeatureIsDisplayed = False
            iCount = 0
            for iObjectIndex in range(0, self._oParameters.getLunarFeatures().getCount()):
                if not self._bForFavouriteOnly or self._oParameters.getLunarFeatures().getLunarFeatureByIndex(iObjectIndex).getIsFavourite():
                    bIsDisplayed, bIsObservable, theNewImg = self._addLunarFeatureRow(self._oParameters.getLunarFeatures().getLunarFeatureByIndex(iObjectIndex), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOneLunarFeatureIsDisplayed = True
            if not bAtLeastOneLunarFeatureIsDisplayed:
                theNewImg = theBackupImg
            else:
                # Rewrite Title with counters
                iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("LunarFeatures") + " (" + str(iCount) + "/" + str(self._oParameters.getLunarFeatures().getCount()) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
                iNbLunarFeaturesobservable = iCount
                # Add legend
                theNewImg = self._addLunarFeatureVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
        else:
            theNewImg = theBackupImg
        
        #
        # DEEP SKY (Favourites)
        #
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("TheDeepSkyObjects"), "SectionTitleH1", theNewImg, True, -1)
        # Favourites
        theBackupImg = self._getImageCopy(theNewImg)
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("FavouriteDeepSkyObjects"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, self._oParameters.getSkyObjects().getCount()):
            if self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not self._bForFavouriteOnly or self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("FavouriteDeepSkyObjects") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
        # Other Deep Sky Objects
        theBackupImg = self._getImageCopy(theNewImg)
        if self._bForFavouriteOnly:
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("OtherDeepSkyObjects"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, self._oParameters.getSkyObjects().getCount()):
            if self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(self._oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParametersLocalization.getLabel("OtherDeepSkyObjects") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iNbDeepSkyobjectsObservable + iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            
        # Save and return bitmap name
        sBitmapName = 'Ephemerides_' + self._oParameters.getPlace().getName().replace(' ','') + '.png'
        theNewImg.save(self._sRelativeFolderForBitmaps + sBitmapName, "PNG")
        
        # Return bitmap URL and size
        iWidth, iHeight = theNewImg.size
        return iWidth, iHeight, self._sURLFolderForBitmaps + sBitmapName, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable

    def getHTML(self, oCalendar, oEphemeridesData):
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.getDisplayNumberOfMinutesPerSlot())
        sHTML = self.getHTMLHeaderComment(oCalendar) + "\n"
        sHTML += '<HTML>' + "\n"
        sHTML += '	<HEAD>' + "\n"
        sHTML += '		<title>'+ self._oParametersLocalization.getLabel("HTMLPageTitle") + '</title>' + "\n"
        sHTML += '		<link rel="icon" href="http://' + self._oParameters.getNightlyBatchDomain() + '/favicon.png">' 
        sHTML += '		<base href="">' + "\n"
        sHTML += '		<link rel="stylesheet" href="AstroNotif.css">' + "\n"
        sHTML += '	</head>' + "\n"
        sHTML += '<BODY>' + "\n"

        iWidth, iHeight, sBitmapNameURL, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable = self.getEphemeridesBitmapForPeriod(oCalendar, oEphemeridesData)
        
        sHTML += '    <H1 class="PageHeader">&nbsp;&nbsp;<A href="http://' + self._oParameters.getNightlyBatchDomain() + '" target="_blank">'+ self._oParametersLocalization.getLabel("EphemerisFor") + ' <SPAN style="font-weight: bold">' + oCalendar.getFormattedDateForSlot(0,self._oParameters.getDisplayNumberOfMinutesPerSlot()) + '</SPAN></A>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<SPAN style="font-size:20px">' + self._oParametersLocalization.getLabel("Place") + ': ' + self._oParameters.getPlace().getName() + ' </SPAN>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<SPAN style="font-size:10px">' + self._oParametersLocalization.getLabel("CalculusFor") + ' ' + (datetime.now()).strftime("%d/%m/%Y %H:%M") + ' ' + self._oParametersLocalization.getLabel("By") + ' AstroNotifPython ' + self._oParameters.getGlobalCurrentVersion() + '</SPAN></H1>' + "\n"
        sHTML += '    <IMG class="EphemeridesBitmap" src="' + sBitmapNameURL + '" alt="' + self._oParametersLocalization.getLabel("EphemerisFor") + " " + oCalendar.getFormattedDateForSlot(0,self._oParameters.getDisplayNumberOfMinutesPerSlot()) + '" height="' + str(iHeight) + '" width="' + str(iWidth) + '">' + "\n"
        sHTML += '    </BODY>' + "\n"
        sHTML += '</HTML>' + "\n"

        return sHTML, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable

    def getHTMLHeaderComment(self, oCalendar):
        return ('<!-- Parameters... Date:'  + oCalendar.getDate() + '  - Place:'  + self._oParameters.getPlace().getName() + ' - Longitude:'  + str(self._oParameters.getPlace().getLongitude()) + ' - Latitude:'  + str(self._oParameters.getPlace().getLatitude()) + '  -->'  )
                
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
                
    def _addVisibilityMapLegend(self, oImg, iPastePosX):
        # Add legend at bottom of the bitmap (resized to add the legend)
        
        iImgWidth, iImgHeight = oImg.size
        imgLegend = self._changeImageSize(oImg, iImgWidth, iImgHeight + 30)

        drawLegend = ImageDraw.Draw(imgLegend)
        
        iPosY = iImgHeight + 5
        iPosX = iPastePosX + 10
        
        iHeightText = self._getFontSize("Legend")

        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Impossible'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Impossible'))
        drawLegend.text((iPosX + 25, iPosY),  self._oParametersLocalization.getLabel("ImpossibleDuringDay"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("ImpossibleDuringDay"), font=self._getFont("Legend"))[0] + 25

#        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Below'))
#        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Below'))
#        drawLegend.text((iPosX + 25, iPosY),  self._oParametersLocalization.getLabel("BelowHorizon"), (255,255,255), font=self._getFont("Legend"))
#        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("BelowHorizon"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Hidden'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Hidden'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("HiddenByObstacle"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("HiddenByObstacle"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('VeryLow'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('VeryLow'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("VeryLow"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("VeryLow"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Low'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Low'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("Low"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("Low"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Difficult'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Difficult'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("DifficultToSee"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("DifficultToSee"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Good'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Good'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("GoodVisibility"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("GoodVisibility"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Unknown'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorObjectVisibilityStatus('Unknown'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("Unknown"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("Unknown"), font=self._getFont("Legend"))[0] + 25
        
        return imgLegend          
                
    def _addLunarFeatureVisibilityMapLegend(self, oImg, iPastePosX):
        # Add legend at bottom of the bitmap (resized to add the legend)
        
        iImgWidth, iImgHeight = oImg.size
        imgLegend = self._changeImageSize(oImg, iImgWidth, iImgHeight + 30)

        drawLegend = ImageDraw.Draw(imgLegend)
        
        iPosY = iImgHeight + 5
        iPosX = iPastePosX + 10
        
        iHeightText = self._getFontSize("Legend")

        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorLunarFeatureVisibility('SunBelowHorizon'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorLunarFeatureVisibility('SunBelowHorizon'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("AtFeatureSunBelowHorizon"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("AtFeatureSunBelowHorizon"), font=self._getFont("Legend"))[0] + 25
        
        for iOcc in range(20, 0, -1):
            fAlt = self._oParameters.getObservationMaximumLunarFeatureSunAltitude() / 20.0 * float(iOcc)
            tColor = (255, 127 + int(fAlt / self._oParameters.getObservationMaximumLunarFeatureSunAltitude() * 128.0), int(fAlt / self._oParameters.getObservationMaximumLunarFeatureSunAltitude() * 255.0))
            drawLegend.line((iPosX + iOcc, iPosY + (iHeightText / 2), iPosX + iOcc, iPosY + (iHeightText / 2)), fill=tColor)
            drawLegend.line((iPosX + iOcc, iPosY + (iHeightText / 2 + 1), iPosX + iOcc, iPosY + (iHeightText / 2 + 1)), fill=tColor)
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("Observable"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("Observable"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorLunarFeatureVisibility('Good'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorLunarFeatureVisibility('Good'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("NearTerminatorGoodVisibility"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("NearTerminatorGoodVisibility"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParametersRendering.getColorLunarFeatureVisibility('SunTooHigh'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParametersRendering.getColorLunarFeatureVisibility('SunTooHigh'))
        drawLegend.text((iPosX + 25, iPosY), self._oParametersLocalization.getLabel("AtFeatureSunTooHigh"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParametersLocalization.getLabel("AtFeatureSunTooHigh"), font=self._getFont("Legend"))[0] + 25
        
        return imgLegend          

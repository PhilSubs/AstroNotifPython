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

class RendererBitmap(toolObjectSerializable):
    iLeftLabelWidthInPx = 100
    iHourSlotWidthInPx = 16
    iAltitudeRowHeight = 3
    sFontDefaultName = "arial.ttf"
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


    def __init__(self, sRelativeFolderForBitmaps, sURLFolderForBitmaps, bForFavouriteOnly = False):
        toolObjectSerializable.__init__(self)
        self._bForFavouriteOnly = bForFavouriteOnly
        self._sRelativeFolderForBitmaps = sRelativeFolderForBitmaps
        self._sURLFolderForBitmaps = sURLFolderForBitmaps
        self._oParametersRendering = ParametersRendering()

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
        if sStyle == "RowHeaderDate":
            iStyleFontSize = self._oParametersRendering.getStyles('RowHeaderDateFontSize')
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
        
    def _addLunarFeatureRow(self, oLunarFeatureObject, oCalendar, oParameters, oEphemeridesData, oImg):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())

        sComment1 = oLunarFeatureObject.getType() + "    -    Long: " + str(oLunarFeatureObject.getLongitude()) + "  -  Lat: " + str(oLunarFeatureObject.getLatitude())
        sComment2 = ""
        sComment3 = ""
        sFormatForFloatValues = "{0:.1f}"
        if oLunarFeatureObject.getDiameter() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + "Diameter: " + sFormatForFloatValues.format(oLunarFeatureObject.getDiameter()) + " km"
        if oLunarFeatureObject.getDepth() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") +  "Depth: " + sFormatForFloatValues.format(oLunarFeatureObject.getDepth()) + " km"
        if oLunarFeatureObject.getHeight() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") +  "Height: " + sFormatForFloatValues.format(oLunarFeatureObject.getHeight()) + " km"
        if oLunarFeatureObject.getLength() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") +  "Length: " + sFormatForFloatValues.format(oLunarFeatureObject.getLength()) + " km"
        if oLunarFeatureObject.getBreadth() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") +  "Breadth: " + sFormatForFloatValues.format(oLunarFeatureObject.getBreadth()) + " km"
        if oLunarFeatureObject.getRukl() != "": sComment3 += ("  -  " if len(sComment3) > 0 else "") +  "Rukl: " + oLunarFeatureObject.getRukl()
        iRowPositionY, theNewImg = self._addLunarFeatureRowHeader(oLunarFeatureObject.getName(), sComment1, sComment2, sComment3, oImg)
        iTmpX, iTmpY = theNewImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayIsObservable = False
        bAtLeastOneDayIsNotObservable = False
        for iDaySlot in range (0,  oParameters.getDisplayNumberOfSlotsForMoonFeatures(), iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + oParameters.getDisplayDaySlotForDataInfo()
            iStartX = RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph + (iDay * iNbSlotsPerDay * iSlotWidthInPx) + (iDay * RendererBitmap.iTableSpaceBetweenDays)
            bToBeDisplayed, bIsObservable, theNewImg =  self._addLunarFeatureVisibilityBitmapForDay(iDaySlot, iDaySlot + iNbSlotsPerDay, iDataSlot, oLunarFeatureObject, oCalendar, oParameters, oEphemeridesData, theNewImg, iStartX, iRowPositionY)
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

        if not bAtLeastOneDayIsNotObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
        elif not bAtLeastOneDayIsObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
        else:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
            
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
        theNewDraw.text((iStartX + 3 + 40, iStartY + 5), sObjectName, (0,0,0), font=self._getFont("LunarFeatureName"))
        theNewDraw.text((iStartX + 3 + 40, iStartY + 22 + 10), sComment1, (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3 + 40, iStartY + 22 + 10 + 12), sComment2, (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3 + 40, iStartY + 22 + 10 + 12 + 12), sComment3, (0,0,0), font=self._getFont("LunarFeatureData"))

        return iStartY, oNewImg

    def _addLunarFeatureVisibilityBitmapForDay(self, iStartSlot, iEndSlot, iDataSlot, oLunarFeatureObject, oCalendar, oParameters, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
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
            sMoonVisibilityStatus = oEphemeridesData.getObjectVisibilityStatusForSlot("Moon", iSlot, oParameters)
            if fSunAltitudeOverFeature > 0.0 and fSunAltitudeOverFeature <= oParameters.getObservationMaximumLunarFeatureSunAltitude():
                bIsObservable = True
            fLongitudeMin = (oLunarFeatureObject.getLongitudeMin() - oParameters.getObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg() + 360.0) % 360.0
            fLongitudeMax = (oLunarFeatureObject.getLongitudeMax() + oParameters.getObservationShowWhenTerminatorIsOnLunarFeatureWithinDeg() + 360.0) % 360.0
            fTerminatorLongitudeRise = (oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot) - 90.0) % 360.0
            fTerminatorLongitudeSet = (oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot) + 90.0) % 360.0
#            if oEphemeridesData.getEphemerideDataObject("Moon").getColongitudeForSlot(iSlot) < 90.0:
#                fTerminatorLongitude = oEphemeridesData.getEphemerideDataObject("Moon").getColongitudeForSlot(iSlot) + 180.0
#            elif oEphemeridesData.getEphemerideDataObject("Moon").getColongitudeForSlot(iSlot) > 90.0:
#                fTerminatorLongitude = oEphemeridesData.getEphemerideDataObject("Moon").getColongitudeForSlot(iSlot) - 180.0
#            else:
#                fTerminatorLongitude = oEphemeridesData.getEphemerideDataObject("Moon").getColongitudeForSlot(iSlot)
#            bIsTerminatorNearFeature = (fTerminatorLongitude >= fLongitudeMin and fTerminatorLongitude <= fLongitudeMax)
            bIsTerminatorNearFeature = ((fTerminatorLongitudeRise >= fLongitudeMin and fTerminatorLongitudeRise <= fLongitudeMax) or (fTerminatorLongitudeSet >= fLongitudeMin and fTerminatorLongitudeSet <= fLongitudeMax))
            if oParameters.getObservationShowWhenTerminatorIsOnLunarFeature() and bIsTerminatorNearFeature:
                if sMoonVisibilityStatus == "Below" or sMoonVisibilityStatus == "Hidden" or sMoonVisibilityStatus == "Impossible" :
                    tColor = (154, 154, 154, 255)
                else:
                    tColor = (255, 64, 0, 255)
            elif fSunAltitudeOverFeature <= 0.0:
                tColor = (0, 0, 0, 255)
            elif fSunAltitudeOverFeature >= oParameters.getObservationMaximumLunarFeatureSunAltitude():
                tColor = (255, 255, 255, 255)
            else:
                if sMoonVisibilityStatus == "Below" or sMoonVisibilityStatus == "Hidden" or sMoonVisibilityStatus == "Impossible" :
                    tColor = (180 + int(fSunAltitudeOverFeature / oParameters.getObservationMaximumLunarFeatureSunAltitude() * 75.0), 180 + int(fSunAltitudeOverFeature / oParameters.getObservationMaximumLunarFeatureSunAltitude() * 75.0), 180 + int(fSunAltitudeOverFeature / oParameters.getObservationMaximumLunarFeatureSunAltitude() * 75.0), 255)
                else:
                    tColor = (255, 127 + int(fSunAltitudeOverFeature / oParameters.getObservationMaximumLunarFeatureSunAltitude() * 128.0), int(fSunAltitudeOverFeature / oParameters.getObservationMaximumLunarFeatureSunAltitude() * 255.0), 255)
            x1 = iBorderStartX + 1 + (iSlot - iStartSlot) * iSlotWidthInPx
            x2 = x1 + iSlotWidthInPx - 1
            y1 = iBorderStartY + 1
            y2 = iBorderEndY - 1 - RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
            theNewDraw.rectangle((x1, y1, x2, y2), fill=tColor)

        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127, 255))

        # Additional data
        sAdditionalText = 'At ' + oCalendar.getTimeForSlotAsHHMM(iDataSlot, oParameters.getDisplayNumberOfMinutesPerSlot()) + ':   Sun Altitude: ' + str(int(round(MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot))))) + '  Sun Azimut: ' + str(int(round(MeeusAlgorithms.getSunAzimutFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot)))))
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255, 255), font=self._getFont("ObjectAdditionalDailyData"))
        
        bToBeDisplayed = (bIsObservable or oParameters.getObservationAlways())
        if bToBeDisplayed:        
            return True, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
                
    def _addMoonMinimapBitmap(self, iPhase, fLongitude, fLatitude, oImg, iPosX, iPosY, iBitmapSize):
        iIndicatorSizeInPx = 3
        
        tColorMoonMapBorder = self.oParametersRendering.getColorMoonMiniMap('Border')
        tColorMoonMapBackground = self.oParametersRendering.getColorMoonMiniMap('Background')
        tColorMoonMapLight = self.oParametersRendering.getColorMoonMiniMap('Light')
        tColorMoonMapDark = self.oParametersRendering.getColorMoonMiniMap('Dark')
        
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
        
    def _addObjectRow(self, oEphemeridesDataObject, oCalendar, oParameters, oEphemeridesData, oImg):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        bIsObservable = False
        sHTMLObjectRow = ""
        if (oEphemeridesDataObject.getType() == "Moon"):
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject.getName(), "", "", "", oImg)
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoon()
        elif (oEphemeridesDataObject.getType() == "Planet"):
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForPlanets()
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(0)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0))) + ' deg'
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (near conjonction)'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (near opposition)'
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject.getName(), "Distance: " +  str(int(round(oEphemeridesDataObject.getDistanceForSlot(0) * 149.600000, 1))) + ' M.Km', "Position Angle: " +  sMeanLongComment, 'Diam. app.: ' + str(int(round(oEphemeridesDataObject.getApparentDiameterInArcSecForSlot(0), 1))) + ' "', oImg)
            # add heliocentric schema
            theNewImg = self._addHeliocentricBitmap(oEphemeridesDataObject.getName(), oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0, oEphemeridesDataObject.getMeanLongForSlot(0), iRowPositionY, theNewImg)
        else:
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForDeepSky()
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject.getName(), oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getType(), "RA: " + CommonAstroFormulaes.getHMSFromDeg(oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getRA()) + "    Dec: " +  str(round(oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDec(),2)), oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getComment1(), oImg)
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayObservable = False
        bAtLeastOneDayNotObservable = False
        for iDaySlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + oParameters.getDisplayDaySlotForDataInfo()
            iStartX = RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph + (iDay * iNbSlotsPerDay * iSlotWidthInPx) + (iDay * RendererBitmap.iTableSpaceBetweenDays)
            bIsDisplayed, bIsObservable, theNewImg =  self._addObjectVisibilityInfoForDay( oEphemeridesDataObject, oCalendar, oParameters, iDaySlot, iDaySlot + iNbSlotsPerDay, iDataSlot, oEphemeridesData, theNewImg, iStartX, iRowPositionY)
            if bIsDisplayed:
                bAtLeastOneDayToBeDisplayed = True
            if bIsObservable:
                bAtLeastOneDayObservable = True
            else:
                bAtLeastOneDayNotObservable = True
        
        if not bAtLeastOneDayNotObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
        elif not bAtLeastOneDayObservable:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
        else:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParametersRendering.getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
        
        if bAtLeastOneDayToBeDisplayed:
            return bAtLeastOneDayToBeDisplayed, bAtLeastOneDayObservable, theNewImg
        else:
            return bAtLeastOneDayToBeDisplayed, bAtLeastOneDayObservable, oImg
            
    def _addObjectRowHeader(self, sObjectName, sObjectDataRow1, sObjectDataRow2, sObjectDataRow3, oImg):
        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight

        iNewHeight = iImgHeight + iTableObjectRowHeight + 1
        oNewImg = self._changeImageSize(oImg, iImgWidth, iNewHeight)
        iStartX = RendererBitmap.iTableMarginLeft
        iStartY = iImgHeight + 1
        theNewDraw = ImageDraw.Draw(oNewImg)

        theNewDraw.rectangle((iStartX, iStartY, iStartX + RendererBitmap.iTableWidthObjectLabel, iStartY + iTableObjectRowHeight), fill=(255, 255, 255))

        theNewDraw.text((iStartX + 3, iStartY), sObjectName, (0,0,0), font=self._getFont("ObjectName"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), Tools.removeHTMLTags(sObjectDataRow1), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), Tools.removeHTMLTags(sObjectDataRow2), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 * 2), Tools.removeHTMLTags(sObjectDataRow3), (0,0,0), font=self._getFont("ObjectData"))
        
        return iStartY, oNewImg

    def _addObjectVisibilityBitmapForDay(self, oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
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
                    sObjectVisibilityStatus = oEphemeridesData.getObjectVisibilityStatusForSlot(oEphemeridesDataObject.getID(), iSlot, oParameters)
                    tColor = self._getBitmapColorForObjectAltitudeDependingOnSunAltitude(sObjectVisibilityStatus)
                    if tColor == (0, 255, 0): bIsObservable = True
                    if iPrevX > -1 and iPrevY > -1:
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY, iRowPositionX - 1 + x, iRowPositionY + 1 + y), fill=tColor)
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY -1, iRowPositionX - 1 + x, iRowPositionY + 1 + y -1 ), fill=tColor)
                iPrevX = x
                iPrevY = y
        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127))
        
        # delete useless objects
        del theNewDraw        

        bIsDisplayed = (bIsObservable or oParameters.getObservationAlways() or (oParameters.getObservationForceDisplayPlanetMoon() and oEphemeridesDataObject.getCategory() == "Planetary"))
        if bIsDisplayed:        
            return bIsDisplayed, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
        
    def _addObjectVisibilityInfoForDay(self, oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, iDataSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        bIsObservable = False
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        
        bIsDisplayed, bIsObservable, theNewImg = self._addObjectVisibilityBitmapForDay(oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX + 3, iRowPositionY)

        if oEphemeridesDataObject.getType() == "Planet":
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(iStartSlot) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(iStartSlot)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0)))
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (near conjonction)'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (near opposition)'
            sAdditionalText = 'Culm. ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', azimut ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))
        elif oEphemeridesDataObject.getType() == "Moon":
            sAdditionalText = 'At ' + oCalendar.getTimeForSlotAsHHMM(iDataSlot, oParameters.getDisplayNumberOfMinutesPerSlot()) + ':  Dist: ' + str(int(round(oEphemeridesDataObject.getDistanceForSlot(iDataSlot)))) + ' Km, Phase: ' + str(int(round(abs(oEphemeridesDataObject.getPhaseForSlot(iDataSlot))))) + ', Illum: ' + str(int(round(oEphemeridesDataObject.getIlluminationForSlot(iDataSlot) * 100))) + '%, Colong: ' + str(int(round(oEphemeridesDataObject.getColongitudeForSlot(iDataSlot)))) + ' -=- Culm. ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', azimut ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))
        else:
            sAdditionalText = 'Culm. ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', azimut ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))

        theNewDraw = ImageDraw.Draw(theNewImg)
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255), font=self._getFont("ObjectAdditionalDailyData"))
    
        return bIsDisplayed, bIsObservable, theNewImg
            
    def _addObjectVisibilityTableHeader(self, oCalendar, oParameters, oEphemeridesData, sType, oImg):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iNbSlotsPerHour = 60 / oParameters.getDisplayNumberOfMinutesPerSlot()
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iTableHeaderHeight = RendererBitmap.iTableHeaderRowHeight * 2 + RendererBitmap.iTableHeaderRowInterline # 2 rows + 5 pixel in between
        if sType == "Moon":
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoon()
        elif sType == "MoonFeatures":
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoonFeatures()
        elif sType == "Planet":
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForPlanets()
        else:
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForDeepSky()
        
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
            theNewDraw.text((iHeaderStartX + 3, iHeaderStartY + 3), oCalendar.getFormattedDateForSlot(iSlot,oParameters.getDisplayNumberOfMinutesPerSlot()), (255,255,255), font=self._getFont("RowHeaderDate"))
            for iDaySlot in range (iSlot,  iSlot + iNbSlotsPerDay, iNbSlotsPerHour ):
                theNewDraw.text((iHeaderStartX + 3 + (iDaySlot - iSlot) * iSlotWidthInPx, iStartY + RendererBitmap.iTableHeaderRowHeight + 4 + RendererBitmap.iTableHeaderRowInterline), oCalendar.getTimeForSlot(iDaySlot, oParameters.getDisplayNumberOfMinutesPerSlot())[0:2], (255,255,255), font=self._getFont("RowHeaderTime"))
        
        return oNewImg

    def _addTitleForSection(self, sTitle, sStyle, oImg, bFillRow, iStartY):
        # Get Style
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle(sStyle)

        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        if sStyle == "SectionTitleH0":
            iTopMargin = 1
            iBottomMargin = 10
            iPaddingTopBottom = 6
        elif sStyle == "SectionTitleH1":
            iTopMargin = 60
            iBottomMargin = 15
            iPaddingTopBottom = 5
        elif sStyle == "SectionTitleH2":
            iTopMargin = 20
            iBottomMargin = 0
            iPaddingTopBottom = 2
        else:
            iTopMargin = 10
            iBottomMargin = 10
            iPaddingTopBottom = 2
        
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
   
    def getEphemeridesBitmapForPeriod(self, oCalendar, oParameters, oEphemeridesData):
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
        iTitlePosY, theNewImg = self._addTitleForSection("The Planets", "SectionTitleH1", theBackupImg, True, -1)
        # add header with date and time for Planets
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oParameters, oEphemeridesData, "Planet", theNewImg)
        # Add objects rows for Planets
        bAtLeastOnePlanetIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, oParameters.getSkyObjects().getCount()):
            if oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getType() == 'Planet':
                if not self._bForFavouriteOnly or oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oParameters, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOnePlanetIsDisplayed = True
        if not bAtLeastOnePlanetIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection("The Planets (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH1", theNewImg, True, iTitlePosY)
            iNbPlanetsObservable = iCount
        #
        # MOON
        #
        theBackupImg = self._getImageCopy(theNewImg)
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection("The Moon", "SectionTitleH1", theNewImg, True, -1)
        iTitlePosY, theNewImg = self._addTitleForSection("Moon Visibility", "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Moon
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oParameters, oEphemeridesData, "Moon", theNewImg)
        # Add object row for Moon
        isMoonDisplayed, isMoonObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject("Moon"), oCalendar, oParameters, oEphemeridesData, theNewImg)
        if isMoonDisplayed:
            theBackupImg = self._getImageCopy(theNewImg)
            # Add Title
            iTitlePosY, theNewImg = self._addTitleForSection("Lunar Features", "SectionTitleH2", theNewImg, False, -1)
            # Add header for Lunar Features
            theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oParameters, oEphemeridesData, "MoonFeatures", theNewImg)
            # Add rows for Lunar Features
            bAtLeastOneLunarFeatureIsDisplayed = False
            iCount = 0
            for iObjectIndex in range(0, oParameters.getLunarFeatures().getCount()):
                if not self._bForFavouriteOnly or oParameters.getLunarFeatures().getLunarFeatureByIndex(iObjectIndex).getIsFavourite():
                    bIsDisplayed, bIsObservable, theNewImg = self._addLunarFeatureRow(oParameters.getLunarFeatures().getLunarFeatureByIndex(iObjectIndex), oCalendar, oParameters, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOneLunarFeatureIsDisplayed = True
            if not bAtLeastOneLunarFeatureIsDisplayed:
                theNewImg = theBackupImg
            else:
                # Rewrite Title with counters
                iTitlePosY, theNewImg = self._addTitleForSection("Lunar Features (" + str(iCount) + "/" + str(oParameters.getLunarFeatures().getCount()) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
                iNbLunarFeaturesobservable = iCount
        else:
            theNewImg = theBackupImg
        
        #
        # DEEP SKY (Favourites)
        #
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection("The Deep Sky Objects", "SectionTitleH1", theNewImg, True, -1)
        # Favourites
        theBackupImg = self._getImageCopy(theNewImg)
        iTitlePosY, theNewImg = self._addTitleForSection("Favourites Deep Sky Objects", "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oParameters, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, oParameters.getSkyObjects().getCount()):
            if oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not self._bForFavouriteOnly or oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oParameters, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection("Favourites Deep Sky Objects (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iCount
        # Other Deep Sky Objects
        theBackupImg = self._getImageCopy(theNewImg)
        if self._bForFavouriteOnly:
            iTitlePosY, theNewImg = self._addTitleForSection("Other Deep Sky Objects", "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oParameters, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, oParameters.getSkyObjects().getCount()):
            if oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oParameters, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection("Other Deep Sky Objects (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iNbDeepSkyobjectsObservable + iCount

        # Save and return bitmap name
        sBitmapName = 'Ephemerides_' + oParameters.getPlace().getName().replace(' ','') + '.png'
        theNewImg.save(self._sRelativeFolderForBitmaps + sBitmapName, "PNG")
        
        # Return bitmap URL and size
        iWidth, iHeight = theNewImg.size
        return iWidth, iHeight, self._sURLFolderForBitmaps + sBitmapName, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable

    def getHTML(self, oCalendar, oParameters, oEphemeridesData):
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        sHTML = self.getHTMLHeaderComment(oCalendar, oParameters) + "\n"
        sHTML += '<HTML>' + "\n"
        sHTML += '	<HEAD>' + "\n"
        sHTML += '		<title>AstroNotif</title>' + "\n"
        sHTML += '		<link rel="icon" href="http://' + oParameters.getNightlyBatchDomain() + '/favicon.png">' 
        sHTML += '		<base href="">' + "\n"
        sHTML += '		<style>' + "\n"
        sHTML += '          H1   {font-family: "arial", "sans-serif"; font-size:30px; font-weight: normal; background: #6dc7ff; color: #000000; padding-top: 15px; padding-bottom: 15px;}' + "\n"
        sHTML += '		</style>' + "\n"
        sHTML += '	</head>' + "\n"
        sHTML += '<BODY>' + "\n"

        iWidth, iHeight, sBitmapNameURL, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable = self.getEphemeridesBitmapForPeriod(oCalendar, oParameters, oEphemeridesData)
        
        sHTML += '    <H1>&nbsp;&nbsp;<A href="http://' + oParameters.getNightlyBatchDomain() + '" target="_blank">Ephemerides du <SPAN style="font-weight: bold">' + oCalendar.getFormattedDateForSlot(0,oParameters.getDisplayNumberOfMinutesPerSlot()) + '</SPAN></A>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<SPAN style="font-size:20px">Lieu: ' + oParameters.getPlace().getName() + ' </SPAN>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<SPAN style="font-size:10px">Calculs du ' + (datetime.now()).strftime("%d/%m/%Y %H:%M") + ' par AstroNotifPython ' + oParameters.getGlobalCurrentVersion() + '</SPAN></H1>' + "\n"
        sHTML += '    <IMG style="border:none" src="' + sBitmapNameURL + '" alt="' + "Ephemerides du " + oCalendar.getFormattedDateForSlot(0,oParameters.getDisplayNumberOfMinutesPerSlot()) + '" height="' + str(iHeight) + '" width="' + str(iWidth) + '">' + "\n"
        sHTML += '    </BODY>' + "\n"
        sHTML += '</HTML>' + "\n"

        return sHTML, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable

    def getHTMLHeaderComment(self, oCalendar, oParameters):
        return ('<!-- Parameters... Date:'  + oCalendar.getDate() + '  - Place:'  + oParameters.getPlace().getName() + ' - Longitude:'  + str(oParameters.getPlace().getLongitude()) + ' - Latitude:'  + str(oParameters.getPlace().getLatitude()) + '  -->'  )
                
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

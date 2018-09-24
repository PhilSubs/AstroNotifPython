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

    def _getBitmapColorForObjectAltitudeDependingOnSunAltitude(self, sObjectVisibilityStatus):
        tColor = self._oParameters.Rendering().getColorObjectVisibilityStatus(sObjectVisibilityStatus)
        return tColor

    def _getBitmapColorforSunAltitude(self, fSunAltitude):
        if fSunAltitude < -18.0:
            tColor = self._oParameters.Rendering().getColorSunAltitude('MoreThan18DegBelow')
        elif fSunAltitude < -12.0:
            tColor = self._oParameters.Rendering().getColorSunAltitude('12To18DegBelow')
        elif fSunAltitude < -6.0:
            tColor = self._oParameters.Rendering().getColorSunAltitude('06To12DegBelow')
        elif fSunAltitude < -0.0:
            tColor = self._oParameters.Rendering().getColorSunAltitude('00To06DegBelow')
        elif fSunAltitude < 6.0:
            tColor = self._oParameters.Rendering().getColorSunAltitude('00To06DegAbove')
        elif fSunAltitude < 12.0:
            tColor = self._oParameters.Rendering().getColorSunAltitude('06To12DegAbove')
        else:
            tColor = self._oParameters.Rendering().getColorSunAltitude('MoreThan12DegAbove')
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
        iStyleFontSize = self._oParameters.Rendering().getStyles('DefaultFontSize')
        sFontDirectory = self._oParameters.Rendering().getStyles('DefaultFontDirectory')
        if sFontDirectory == "": sFontDirectory = Tools.get_ResourceSubfolder_path("Fonts")
        sFont = sFontDirectory + self._oParameters.Rendering().getStyles('DefaultFont')
        tStyleFontColor = self._oParameters.Rendering().getStyles('DefaultFontColor')
        tStyleBackColor = self._oParameters.Rendering().getStyles('DefaultBackColor')
        
        # Style overlap
        if sStyle == "GMTWarning":
            iStyleFontSize = self._oParameters.Rendering().getStyles('GMTWarningFontSize')
            sFont = sFontDirectory + self._oParameters.Rendering().getStyles('GMTWarningFont')
        elif sStyle == "Legend":
            iStyleFontSize = self._oParameters.Rendering().getStyles('LegendFontSize')
            sFont = sFontDirectory + self._oParameters.Rendering().getStyles('LegendFont')
        elif sStyle == "RowHeaderDate":
            iStyleFontSize = self._oParameters.Rendering().getStyles('RowHeaderDateFontSize')
            sFont = sFontDirectory + self._oParameters.Rendering().getStyles('RowHeaderDateFont')
        elif sStyle == "RowHeaderTime":
            iStyleFontSize = self._oParameters.Rendering().getStyles('RowHeaderTimeFontSize')
        elif sStyle == "ObjectName":
            iStyleFontSize = self._oParameters.Rendering().getStyles('ObjectNameFontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('ObjectNameFontColor')
        elif sStyle == "ObjectNameNotified":
            iStyleFontSize = self._oParameters.Rendering().getStyles('ObjectNameNotifiedFontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('ObjectNameNotifiedFontColor')
        elif sStyle == "ObjectData":
            iStyleFontSize = self._oParameters.Rendering().getStyles('ObjectDataFontSize')
        elif sStyle == "ObjectAdditionalDailyData":
            iStyleFontSize = self._oParameters.Rendering().getStyles('ObjectAdditionalDailyDataFontSize')
        elif sStyle == "SectionTitleH0":
            iStyleFontSize = self._oParameters.Rendering().getStyles('SectionTitleH0FontSize')
            tStyleBackColor = self._oParameters.Rendering().getStyles('SectionTitleH0BackColor')
            tStyleFontColor = self._oParameters.Rendering().getStyles('SectionTitleH0FontColor')
        elif sStyle == "SectionTitleH1":
            iStyleFontSize = self._oParameters.Rendering().getStyles('SectionTitleH1FontSize')
            tStyleBackColor = self._oParameters.Rendering().getStyles('SectionTitleH1BackColor')
            tStyleFontColor = self._oParameters.Rendering().getStyles('SectionTitleH1FontColor')
        elif sStyle == "SectionTitleH2":
            iStyleFontSize = self._oParameters.Rendering().getStyles('SectionTitleH2FontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('SectionTitleH2FontColor')
        elif sStyle == "LunarFeatureName":
            iStyleFontSize = self._oParameters.Rendering().getStyles('LunarFeatureNameFontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('LunarFeatureNameFontColor')
        elif sStyle == "LunarFeatureNameNotified":
            iStyleFontSize = self._oParameters.Rendering().getStyles('LunarFeatureNameNotifiedFontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('LunarFeatureNameNotifiedFontColor')
        elif sStyle == "LunarFeatureData":
            iStyleFontSize = self._oParameters.Rendering().getStyles('LunarFeatureDataFontSize')
            sFont = sFontDirectory + self._oParameters.Rendering().getStyles('LunarFeatureDataFont')
        elif sStyle == "BitmapHeaderH0":
            iStyleFontSize = self._oParameters.Rendering().getStyles('BitmapHeaderH0FontSize')
            tStyleBackColor = self._oParameters.Rendering().getStyles('BitmapHeaderH0BackColor')
            tStyleFontColor = self._oParameters.Rendering().getStyles('BitmapHeaderH0FontColor')
        elif sStyle == "BitmapHeaderH1":
            iStyleFontSize = self._oParameters.Rendering().getStyles('BitmapHeaderH1FontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('BitmapHeaderH1FontColor')
        elif sStyle == "BitmapHeaderH2":
            iStyleFontSize = self._oParameters.Rendering().getStyles('BitmapHeaderH2FontSize')
            tStyleFontColor = self._oParameters.Rendering().getStyles('BitmapHeaderH2FontColor')
        
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
        iNbSlotsPerDay = (1440 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))

        sComment1 = self._oParameters.Localization().getLabel(oLunarFeatureObject.getType()) + "    -    " + self._oParameters.Localization().getLabel("LongitudeAbrev") + ": " + str(oLunarFeatureObject.getLongitude()) + "  -  "  + self._oParameters.Localization().getLabel("LatitudeAbrev") + ": " + str(oLunarFeatureObject.getLatitude())
        sComment2 = ""
        sComment3 = ""
        sFormatForFloatValues = "{0:.1f}"
        if oLunarFeatureObject.getDiameter() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getLabel("Diameter") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getDiameter()) + " " + self._oParameters.Localization().getLabel("KilometerAbrev")
        if oLunarFeatureObject.getDepth() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getLabel("Depth") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getDepth()) + " " + self._oParameters.Localization().getLabel("KilometerAbrev")
        if oLunarFeatureObject.getHeight() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getLabel("Height") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getHeight()) + " " + self._oParameters.Localization().getLabel("KilometerAbrev")
        if oLunarFeatureObject.getLength() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getLabel("Length") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getLength()) + " " + self._oParameters.Localization().getLabel("KilometerAbrev")
        if oLunarFeatureObject.getBreadth() != 0.0: sComment2 += ("  -  " if len(sComment2) > 0 else "") + self._oParameters.Localization().getLabel("Breadth") + ": " + sFormatForFloatValues.format(oLunarFeatureObject.getBreadth()) + " " + self._oParameters.Localization().getLabel("KilometerAbrev")
        if oLunarFeatureObject.getRukl() != "": sComment3 += ("  -  " if len(sComment3) > 0 else "") + self._oParameters.Localization().getLabel("Rukl") + ": " + oLunarFeatureObject.getRukl()
        iRowPositionY, theNewImg = self._addLunarFeatureRowHeader(oLunarFeatureObject, sComment1, sComment2, sComment3, oImg)
        iTmpX, iTmpY = theNewImg.size
        iTableObjectRowHeight = RendererBitmap.iAltitudeRowHeight * 18 + RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayIsObservable = False
        bAtLeastOneDayIsNotObservable = False
        for iDaySlot in range (0,  self._oParameters.Rendering().getDisplay('NumberOfSlotsForMoonFeatures'), iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + self._oParameters.Rendering().getDisplay('DaySlotForDataInfo')
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
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
            else:
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
        else:
            theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
                
#        if not bAtLeastOneDayIsNotObservable:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
#        elif not bAtLeastOneDayIsObservable:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
#        else:
#                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
            
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
        
        if self._oParameters.LunarFeatures().getLunarFeatureByName(oLunarFeatureObject.getName()).getIsNotifyWhenObservable():
            theNewDraw.text((iStartX + 3, iStartY + 5), self._oParameters.Localization().getLabel(oLunarFeatureObject.getName()), tStyleFontColorNotified, font=theStyleFontNotified)
        else:
            theNewDraw.text((iStartX + 3, iStartY + 5), self._oParameters.Localization().getLabel(oLunarFeatureObject.getName()), tStyleFontColor, font=theStyleFont)
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), self._oParameters.Localization().getLabel(sComment1), (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), self._oParameters.Localization().getLabel(sComment2), (0,0,0), font=self._getFont("LunarFeatureData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 + 12), self._oParameters.Localization().getLabel(sComment3), (0,0,0), font=self._getFont("LunarFeatureData"))

        return iStartY, oNewImg

    def _addLunarFeatureVisibilityBitmapForDay(self, iStartSlot, iEndSlot, iDataSlot, oLunarFeatureObject, oCalendar, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
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
            if fSunAltitudeOverFeature > 0.0 and fSunAltitudeOverFeature <= self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude'):
                bIsObservable = True
            fLongitudeMin = (oLunarFeatureObject.getLongitudeMin() - self._oParameters.Runtime().getObservation('ShowWhenTerminatorIsOnLunarFeatureWithinDeg') + 360.0) % 360.0
            fLongitudeMax = (oLunarFeatureObject.getLongitudeMax() + self._oParameters.Runtime().getObservation('ShowWhenTerminatorIsOnLunarFeatureWithinDeg') + 360.0) % 360.0
            fTerminatorLongitudeRise = (oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot) - 90.0) % 360.0
            fTerminatorLongitudeSet = (oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot) + 90.0) % 360.0

            if fLongitudeMax < fLongitudeMin: fLongitudeMax += 360.0
            if fTerminatorLongitudeRise < fLongitudeMin: fTerminatorLongitudeRise += 360.0
            if fTerminatorLongitudeSet < fLongitudeMin: fTerminatorLongitudeSet += 360.0
            
            bIsTerminatorNearFeature = ((fTerminatorLongitudeRise >= fLongitudeMin and fTerminatorLongitudeRise <= fLongitudeMax) or (fTerminatorLongitudeSet >= fLongitudeMin and fTerminatorLongitudeSet <= fLongitudeMax))
            
            
            iTransparency = 255
            if sMoonVisibilityStatus == "Hidden" or sMoonVisibilityStatus == "Impossible" :
                iTransparency = 250
            if sMoonVisibilityStatus == "Below":
                iTransparency = 0
            if self._oParameters.Runtime().getObservation('ShowWhenTerminatorIsOnLunarFeature') and bIsTerminatorNearFeature:
                tColor = self._oParameters.Rendering().getColorLunarFeatureVisibility('Good')
            elif fSunAltitudeOverFeature <= 0.0:  
                tColor = self._oParameters.Rendering().getColorLunarFeatureVisibility('SunBelowHorizon')
            elif fSunAltitudeOverFeature >= self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude'):
                tColor = self._oParameters.Rendering().getColorLunarFeatureVisibility('SunTooHigh')
            else:
                tColor = (255, 127 + int(fSunAltitudeOverFeature / self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude') * 128.0), int(fSunAltitudeOverFeature / self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude') * 255.0))
            tColor = (tColor[0], tColor[1], tColor[2], iTransparency)

                    
            x1 = iBorderStartX + 1 + (iSlot - iStartSlot) * iSlotWidthInPx
            x2 = x1 + iSlotWidthInPx - 1
            y1 = iBorderStartY + 1
            y2 = iBorderEndY - 1 - RendererBitmap.iTableObjectRowGraphAdditionalDataHeight
            theNewDraw.rectangle((x1, y1, x2, y2), fill=tColor)

        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127, 255))

        # Additional data
        sAdditionalText = 'At ' + oCalendar.getLocalTimeForSlotAsHHMM(iDataSlot, self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')) + ':   Sun Altitude: ' + str(int(round(MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot))))) + '  Sun Azimut: ' + str(int(round(MeeusAlgorithms.getSunAzimutFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDataSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDataSlot)))))
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255, 255), font=self._getFont("ObjectAdditionalDailyData"))
        
        bToBeDisplayed = (bIsObservable or self._oParameters.Runtime().getObservation('Always'))
        if bToBeDisplayed:        
            return True, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
                
    def _addMoonMinimapBitmap(self, iPhase, fLongitude, fLatitude, oImg, iPosX, iPosY, iBitmapSize):
        iIndicatorSizeInPx = 3
        
        tColorMoonMapBorder = self._oParameters.Rendering().getColorMoonMiniMap('Border')
        tColorMoonMapBackground = self._oParameters.Rendering().getColorMoonMiniMap('Background')
        tColorMoonMapLight = self._oParameters.Rendering().getColorMoonMiniMap('Light')
        tColorMoonMapDark = self._oParameters.Rendering().getColorMoonMiniMap('Dark')
        
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
        tColorBackground = self._oParameters.Rendering().getColorHeliocentricGraph('Background')
        tColorLines = self._oParameters.Rendering().getColorHeliocentricGraph('Lines')
        tColorSun = self._oParameters.Rendering().getColorHeliocentricGraph('Sun')
        tColorEarth = self._oParameters.Rendering().getColorHeliocentricGraph('Earth')
        tColorPlanet = self._oParameters.Rendering().getColorHeliocentricGraph('Planet')

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
        iNbSlotsPerDay = (1440 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        bIsObservable = False
        sHTMLObjectRow = ""
        if (oEphemeridesDataObject.getCategory() == "Moon"):
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, "", "", "", oImg)
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForMoon')
        elif (oEphemeridesDataObject.getCategory() == "Planetary"):
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForPlanets')
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(0)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0))) + " " + self._oParameters.Localization().getLabel("DegreesAbev")
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (' + self._oParameters.Localization().getLabel("NearConjonction") + ')'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (' + self._oParameters.Localization().getLabel("NearOpposition") + ')'
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, self._oParameters.Localization().getLabel("Distance") + ": " +  str(int(round(oEphemeridesDataObject.getDistanceForSlot(0) * 149.600000, 1))) + ' ' + self._oParameters.Localization().getLabel("MillionKilometersAbrev"), self._oParameters.Localization().getLabel("PositionAngleAbrev") + ": " +  sMeanLongComment, self._oParameters.Localization().getLabel("ApparentDiameterAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getApparentDiameterInArcSecForSlot(0), 1))) + ' ' + self._oParameters.Localization().getLabel("SecondOfAngleAbrev"), oImg)
            # add heliocentric schema
            theNewImg = self._addHeliocentricBitmap(oEphemeridesDataObject.getName(), oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0, oEphemeridesDataObject.getMeanLongForSlot(0), iRowPositionY, theNewImg)
        else:
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForDeepSky')
            sDataRow1 = self._oParameters.Localization().getLabel(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getType())
            if self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDistanceUnit() != "":
                sDataRow1 += "     "  + self._oParameters.Localization().getLabel("DistanceAbrev") + ": " + str(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDistance()) + " "  + self._oParameters.Localization().getLabel(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDistanceUnit())
            sDataRow2 = self._oParameters.Localization().getLabel("RightAscensionAbrev") + ": " + CommonAstroFormulaes.getHMSFromDeg(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getRA()) + "    " + self._oParameters.Localization().getLabel("DeclinationAbrev") + ": " +  str(round(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDec(),2))
            if self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getApparentMagnitude() != "":
                sDataRow3 = self._oParameters.Localization().getLabel("ApparentMagnitudeAbrev") + ": " + str(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getApparentMagnitude())
            if self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDmensionXUnit() != "":
                if sDataRow3 != "": sDataRow3 += "     "
                sDataRow3 += self._oParameters.Localization().getLabel("DimensionAbrev") + ": " + str(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDmensionX()) + " "  + self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDmensionXUnit()
                if self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDmensionYUnit() != "":
                    sDataRow3 += " x "  + str(self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDmensionY()) + " "  + self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDmensionYUnit()
            if self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getComment1() != "":
                if sDataRow3 != "": sDataRow3 += "     "
                sDataRow3 += self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getComment1()
            iRowPositionY, theNewImg = self._addObjectRowHeader(oEphemeridesDataObject, sDataRow1, sDataRow2, sDataRow3, oImg)
        
        bAtLeastOneDayToBeDisplayed = False
        bAtLeastOneDayObservable = False
        bAtLeastOneDayNotObservable = False
        for iDaySlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            iDay = int(iDaySlot / iNbSlotsPerDay)
            iDataSlot = iDaySlot + self._oParameters.Rendering().getDisplay('DaySlotForDataInfo')
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
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('Observable'), iRowPositionY, theNewImg)
            else:            
                theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('AtLEastOneDayObservable'), iRowPositionY, theNewImg)
        else:
            theNewImg = self._addVisibilityFlagOnRowHeader(self._oParameters.Rendering().getColorVisibilityFlags('NotObservable'), iRowPositionY, theNewImg)
            
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
        
        if self._oParameters.SkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getIsNotifyWhenObservable():
            theNewDraw.text((iStartX + 3, iStartY), self._oParameters.Localization().getLabel(oEphemeridesDataObject.getName()), tStyleFontColorNotified, font=theStyleFontNotified)
        else:
            theNewDraw.text((iStartX + 3, iStartY), self._oParameters.Localization().getLabel(oEphemeridesDataObject.getName()), tStyleFontColor, font=theStyleFont)
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10), self._oParameters.Localization().getLabel(Tools.removeHTMLTags(sObjectDataRow1)), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12), self._oParameters.Localization().getLabel(Tools.removeHTMLTags(sObjectDataRow2)), (0,0,0), font=self._getFont("ObjectData"))
        theNewDraw.text((iStartX + 3, iStartY + 22 + 10 + 12 * 2), self._oParameters.Localization().getLabel(Tools.removeHTMLTags(sObjectDataRow3)), (0,0,0), font=self._getFont("ObjectData"))
        
        if oEphemeridesDataObject.getPictureName() <> "":
            imgObjectThumbnail = Image.open(Tools.get_ResourceSubfolder_path("Bitmaps") + oEphemeridesDataObject.getPictureName())
            oNewImg.paste(imgObjectThumbnail, (iStartX + RendererBitmap.iTableWidthObjectLabel - 50 - RendererBitmap.iTableVisibilityFlagWidth - 2, iStartY + 2 ))
        
        return iStartY, oNewImg

    def _addObjectVisibilityBitmapForDay(self, oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        iNbSlotsPerDay = (1440 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
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
                    bIsObservable = ((sObjectVisibilityStatus == "Good" or sObjectVisibilityStatus == "Low") or bIsObservable)
                    if iPrevX > -1 and iPrevY > -1:
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY, iRowPositionX - 1 + x, iRowPositionY + 1 + y), fill=tColor)
                        theNewDraw.line((iRowPositionX - 1 + iPrevX, iRowPositionY + 1 + iPrevY -1, iRowPositionX - 1 + x, iRowPositionY + 1 + y -1 ), fill=tColor)
                iPrevX = x
                iPrevY = y
        # Redraw border
        theNewDraw.rectangle((iBorderStartX, iBorderStartY, iBorderEndX, iBorderEndY), outline=(127, 127, 127))
        
        # delete useless objects
        del theNewDraw        

        bIsDisplayed = (bIsObservable or self._oParameters.Runtime().getObservation('Always') or (self._oParameters.Runtime().getObservation('ForceDisplayPlanetMoon') and (oEphemeridesDataObject.getCategory() == "Planetary" or oEphemeridesDataObject.getCategory() == "Moon")))
        if bIsDisplayed:        
            return bIsDisplayed, bIsObservable, oNewImg
        else:
            return False, bIsObservable, oNewImg
        
    def _addObjectVisibilityInfoForDay(self, oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, iDataSlot, oEphemeridesData, oImg, iRowPositionX, iRowPositionY):
        bIsObservable = False
        iNbSlotsPerDay = (1440 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        
        bIsDisplayed, bIsObservable, theNewImg = self._addObjectVisibilityBitmapForDay(oEphemeridesDataObject, oCalendar, iStartSlot, iEndSlot, oEphemeridesData, oImg, iRowPositionX + 3, iRowPositionY)

        if oEphemeridesDataObject.getCategory() == "Planetary":
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(iStartSlot) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(iStartSlot)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0)))
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' ('  + self._oParameters.Localization().getLabel("NearConjonction") + ')'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' ('  + self._oParameters.Localization().getLabel("NearOpposition") + ')'
            sAdditionalText = self._oParameters.Localization().getLabel("CulminationAbrev") + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', ' + self._oParameters.Localization().getLabel("Azimut") + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))
        elif oEphemeridesDataObject.getCategory() == "Moon":
            sAdditionalText = self._oParameters.Localization().getLabel("A") + ' ' + oCalendar.getLocalTimeForSlotAsHHMM(iDataSlot, self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')) + ':  ' + self._oParameters.Localization().getLabel("DistanceAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getDistanceForSlot(iDataSlot)))) + ' ' + self._oParameters.Localization().getLabel("KilometerAbrev") + ', ' + self._oParameters.Localization().getLabel("Phase") + ': ' + str(int(round(abs(oEphemeridesDataObject.getPhaseForSlot(iDataSlot))))) + ', ' + self._oParameters.Localization().getLabel("IlluminationAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getIlluminationForSlot(iDataSlot) * 100))) + '%, ' + self._oParameters.Localization().getLabel("ColongitudeAbrev") + ': ' + str(int(round(oEphemeridesDataObject.getColongitudeForSlot(iDataSlot)))) + ' -=- ' + self._oParameters.Localization().getLabel("CulminationAbrev") + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', ' + self._oParameters.Localization().getLabel("Azimut") + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))
        else:
            sAdditionalText = self._oParameters.Localization().getLabel("CulminationAbrev") + ' ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', ' + self._oParameters.Localization().getLabel("Azimut") + ' ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot))

        theNewDraw = ImageDraw.Draw(theNewImg)
        theNewDraw.text((iRowPositionX + 3, iRowPositionY + RendererBitmap.iAltitudeRowHeight * 18 + 3), sAdditionalText, (255,255,255), font=self._getFont("ObjectAdditionalDailyData"))
    
        return bIsDisplayed, bIsObservable, theNewImg
            
    def _addObjectVisibilityTableHeader(self, oCalendar, oEphemeridesData, sType, oImg):
        iNbSlotsPerDay = (1440 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iNbSlotsPerHour = 60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        iTableHeaderHeight = RendererBitmap.iTableHeaderRowHeight * 2 + RendererBitmap.iTableHeaderRowInterline # 2 rows + 5 pixel in between
        if sType == "Moon":
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForMoon')
        elif sType == "MoonFeatures":
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForMoonFeatures')
        elif sType == "Planet":
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForPlanets')
        else:
            iMaxSlot = self._oParameters.Rendering().getDisplay('NumberOfSlotsForDeepSky')
        
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
            theNewDraw.text((iHeaderStartX + 3, iHeaderStartY + 3), oCalendar.getFormattedLocalDateForSlot(iSlot,self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')), (255,255,255), font=self._getFont("RowHeaderDate"))
            # Display GMT warning
#            sLabel = self._oParameters.Localization().getLabel("GMTWarning")
#            theNewDraw.text((iHeaderEndX - 3 - theNewDraw.textsize(sLabel, font=self._getFont("GMTWarning"))[0], iHeaderStartY + 3), sLabel, (255,255,255), font=self._getFont("GMTWarning"))            
            # Display hours
            for iDaySlot in range (iSlot,  iSlot + iNbSlotsPerDay, iNbSlotsPerHour ):
                theNewDraw.text((iHeaderStartX + 3 + (iDaySlot - iSlot) * iSlotWidthInPx, iStartY + RendererBitmap.iTableHeaderRowHeight + 4 + RendererBitmap.iTableHeaderRowInterline), oCalendar.getLocalTimeForSlot(iDaySlot, self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))[0:2], (255,255,255), font=self._getFont("RowHeaderTime"))
        
        return oNewImg

    def _addTitleForSection(self, sTitle, sStyle, oImg, bFillRow, iStartY):
        # Get Style
        iStyleFontSize, theStyleFont, tStyleFontColor, tStyleBackColor = self._getStyle(sStyle)

        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        if sStyle == "SectionTitleH0":
            iTopMargin = self._oParameters.Rendering().getStyles('SectionTitleH0TopMargin')
            iBottomMargin = self._oParameters.Rendering().getStyles('SectionTitleH0BottomMargin')
            iPaddingTopBottom = self._oParameters.Rendering().getStyles('SectionTitleH0PaddingTopBottom')
        elif sStyle == "SectionTitleH1":
            iTopMargin = self._oParameters.Rendering().getStyles('SectionTitleH1TopMargin')
            iBottomMargin = self._oParameters.Rendering().getStyles('SectionTitleH1BottomMargin')
            iPaddingTopBottom = self._oParameters.Rendering().getStyles('SectionTitleH1PaddingTopBottom')
        elif sStyle == "SectionTitleH2":
            iTopMargin = self._oParameters.Rendering().getStyles('SectionTitleH2TopMargin')
            iBottomMargin = self._oParameters.Rendering().getStyles('SectionTitleH2BottomMargin')
            iPaddingTopBottom = self._oParameters.Rendering().getStyles('SectionTitleH2PaddingTopBottom')
        else:
            iTopMargin = self._oParameters.Rendering().getStyles('DefaultTopMargin')
            iBottomMargin = self._oParameters.Rendering().getStyles('DefaultBottomMargin')
            iPaddingTopBottom = self._oParameters.Rendering().getStyles('DefaultPaddingTopBottom')
        
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
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("ThePlanets"), "SectionTitleH1", theBackupImg, True, -1)
        # add header with date and time for Planets
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "Planet", theNewImg)
        # Add objects rows for Planets
        bAtLeastOnePlanetIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, self._oParameters.SkyObjects().getCount()):
            if self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'Planetary':
                if not self._bForFavouriteOnly or self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getIsNotifyWhenObservable():
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._oParameters.Runtime().getGlobal("PathToLogFileName"), "Notification for object  " + self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getName())
                    if bIsDisplayed:
                        bAtLeastOnePlanetIsDisplayed = True
        if not bAtLeastOnePlanetIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("ThePlanets") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH1", theNewImg, True, iTitlePosY)
            iNbPlanetsObservable = iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            
        #
        # MOON
        #
        theBackupImg = self._getImageCopy(theNewImg)
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("TheMoon"), "SectionTitleH1", theNewImg, True, -1)
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("MoonVisibility"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Moon
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "Moon", theNewImg)
        # Add object row for Moon
        isMoonDisplayed, isMoonObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject("Moon"), oCalendar, oEphemeridesData, theNewImg)
        if isMoonObservable:
            if self._oParameters.SkyObjects().getSkyObjectByID("Moon").getIsNotifyWhenObservable():
                bNotificationToBeSent = True

        if isMoonDisplayed:
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            theBackupImg = self._getImageCopy(theNewImg)
            # Add Title
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("LunarFeatures"), "SectionTitleH2", theNewImg, False, -1)
            # Add header for Lunar Features
            theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "MoonFeatures", theNewImg)
            # Add rows for Lunar Features
            bAtLeastOneLunarFeatureIsDisplayed = False
            iCount = 0
            for iObjectIndex in range(0, self._oParameters.LunarFeatures().getCount()):
                if not self._bForFavouriteOnly or self._oParameters.LunarFeatures().getLunarFeatureByIndex(iObjectIndex).getIsFavourite():
                    bIsDisplayed, bIsObservable, theNewImg = self._addLunarFeatureRow(self._oParameters.LunarFeatures().getLunarFeatureByIndex(iObjectIndex), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if self._oParameters.LunarFeatures().getLunarFeatureByIndex(iObjectIndex).getIsNotifyWhenObservable():
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._oParameters.Runtime().getGlobal("PathToLogFileName"), "Notification for lunar feature  " + self._oParameters.LunarFeatures().getLunarFeatureByIndex(iObjectIndex).getName())
                    if bIsDisplayed:
                        bAtLeastOneLunarFeatureIsDisplayed = True
            if not bAtLeastOneLunarFeatureIsDisplayed:
                theNewImg = theBackupImg
            else:
                # Rewrite Title with counters
                iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("LunarFeatures") + " (" + str(iCount) + "/" + str(self._oParameters.LunarFeatures().getCount()) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
                iNbLunarFeaturesobservable = iCount
                # Add legend
                theNewImg = self._addLunarFeatureVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
        else:
            theNewImg = theBackupImg
        
        #
        # DEEP SKY (Favourites)
        #
        # Add Title
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("TheDeepSkyObjects"), "SectionTitleH1", theNewImg, True, -1)
        # Favourites
        theBackupImg = self._getImageCopy(theNewImg)
        iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("FavouriteDeepSkyObjects"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, self._oParameters.SkyObjects().getCount()):
            if self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not self._bForFavouriteOnly or self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getIsNotifyWhenObservable():
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._oParameters.Runtime().getGlobal("PathToLogFileName"), "Notification for object  " + self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getName())
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("FavouriteDeepSkyObjects") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
        # Other Deep Sky Objects
        theBackupImg = self._getImageCopy(theNewImg)
        if self._bForFavouriteOnly:
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("OtherDeepSkyObjects"), "SectionTitleH2", theNewImg, False, -1)
        # add header with date and time for Deep Sky objects
        theNewImg = self._addObjectVisibilityTableHeader(oCalendar, oEphemeridesData, "DeepSky", theNewImg)
        # Add object row for Deep Sky objects
        bAtLeastOneObjectIsDisplayed = False
        iNumber = 0
        iCount = 0
        for iObjectIndex in range(0, self._oParameters.SkyObjects().getCount()):
            if self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    iNumber = iNumber + 1
                    bIsDisplayed, bIsObservable, theNewImg = self._addObjectRow(oEphemeridesData.getEphemerideDataObject(self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oEphemeridesData, theNewImg)
                    if bIsObservable:
                        iCount = iCount + 1
                        if self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getIsNotifyWhenObservable():
                            bNotificationToBeSent = True
                            Tools.logToTrace(self._oParameters.Runtime().getGlobal("PathToLogFileName"), "Notification for object  " + self._oParameters.SkyObjects().getSkyObjectByIndex(iObjectIndex).getName())
                    if bIsDisplayed:
                        bAtLeastOneObjectIsDisplayed = True
        if not bAtLeastOneObjectIsDisplayed:
            theNewImg = theBackupImg
        else:
            # Rewrite Title with counters
            iTitlePosY, theNewImg = self._addTitleForSection(self._oParameters.Localization().getLabel("OtherDeepSkyObjects") + " (" + str(iCount) + "/" + str(iNumber) + ")", "SectionTitleH2", theNewImg, True, iTitlePosY)
            iNbDeepSkyobjectsObservable = iNbDeepSkyobjectsObservable + iCount
            # Add legend
            theNewImg = self._addVisibilityMapLegend(theNewImg, RendererBitmap.iTableMarginLeft + RendererBitmap.iTableWidthObjectLabel + RendererBitmap.iTableSpaceBetweenLabelAndGraph)
            
        # Save and return bitmap name
        sBitmapName = 'Ephemerides_' + self._oParameters.Runtime().getPlace().getName().replace(' ','') + '.' + self._oParameters.Rendering().getDisplay('BitmapExtension')
        theNewImg.save(self._sRelativeFolderForBitmaps + sBitmapName, self._oParameters.Rendering().getDisplay('BitmapType'))
        
        # Return bitmap URL and size
        iWidth, iHeight = theNewImg.size
        return iWidth, iHeight, self._sURLFolderForBitmaps + sBitmapName, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, self._sRelativeFolderForBitmaps + sBitmapName, bNotificationToBeSent

    def getHTML(self, oCalendar, oEphemeridesData):
        iSlotWidthInPx = RendererBitmap.iHourSlotWidthInPx / (60 / self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        sHTML = self.getHTMLHeaderComment(oCalendar) + "\n"
        sHTML += '<HTML>' + "\n"
        sHTML += '	<HEAD>' + "\n"
        sHTML += '      <title>'+ self._oParameters.Localization().getLabel("HTMLPageTitle") + '</title>' + "\n"
        sHTML += '      <link rel="icon" href="http://' + self._oParameters.Runtime().getNightlyBatch('Domain') + '/favicon.png">' 
        sHTML += '      <base href="">' + "\n"
        sHTML += '      <link rel="stylesheet" href="http://' + self._oParameters.Runtime().getNightlyBatch('Domain') + '/AstroNotif.css">' + "\n"
        sHTML += '      <meta charset="UTF-8">' + "\n"
        sHTML += '	</head>' + "\n"
        sHTML += '<BODY>' + "\n"

        iWidth, iHeight, sBitmapNameURL, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilename, bNotificationToBeSent = self.getEphemeridesBitmapForPeriod(oCalendar, oEphemeridesData)
        
        sHTML += '    <H1 class="PageHeader">&nbsp;&nbsp;'
        sHTML += '<A href="http://' + self._oParameters.Runtime().getNightlyBatch('Domain') + '" target="_blank">' + self._oParameters.Localization().getLabel("EphemerisFor") + ' <SPAN style="font-weight: bold">' + oCalendar.getFormattedLocalDateForSlot(0,self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')) + '</SPAN></A>'
        sHTML += '</H1>' + "\n"
        sHTML += '    <IMG class="EphemeridesBitmap" src="' + sBitmapNameURL + '" alt="' +  self._oParameters.Localization().getLabel("EphemerisFor") + " " + oCalendar.getFormattedLocalDateForSlot(0,self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot')) +  '" height="' + str(iHeight) + '" width="' + str(iWidth) + '">' + "\n"
        sHTML += '    </BODY>' + "\n"
        sHTML += '</HTML>' + "\n"
        return sHTML, iNbPlanetsObservable, iNbLunarFeaturesobservable, iNbDeepSkyobjectsObservable, sBitmapFilename, bNotificationToBeSent

    def getHTMLHeaderComment(self, oCalendar):
        return ('<!-- Parameters... Date:'  + oCalendar.getLocalStartDate() + '  - Place:'  + self._oParameters.Runtime().getPlace().getName() + ' - Longitude:'  + str(self._oParameters.Runtime().getPlace().getLongitude()) + ' - Latitude:'  + str(self._oParameters.Runtime().getPlace().getLatitude()) + '  -->'  )
                
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

        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Impossible'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Impossible'))
        drawLegend.text((iPosX + 25, iPosY),  self._oParameters.Localization().getLabel("ImpossibleDuringDay"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("ImpossibleDuringDay"), font=self._getFont("Legend"))[0] + 25

#        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Below'))
#        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Below'))
#        drawLegend.text((iPosX + 25, iPosY),  self._oParameters.Localization().getLabel("BelowHorizon"), (255,255,255), font=self._getFont("Legend"))
#        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("BelowHorizon"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Hidden'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Hidden'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("HiddenByObstacle"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("HiddenByObstacle"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('VeryLow'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('VeryLow'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("VeryLow"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("VeryLow"), font=self._getFont("Legend"))[0] + 25
        
        if bWithStatusDifficultMoonLight:
            drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('DifficultMoonlight'))
            drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('DifficultMoonlight'))
            drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("DifficultMoonlight"), (255,255,255), font=self._getFont("Legend"))
            iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("DifficultMoonlight"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Low'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Low'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("Low"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("Low"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Difficult'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Difficult'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("DifficultToSee"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("DifficultToSee"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Good'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Good'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("GoodVisibility"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("GoodVisibility"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Unknown'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorObjectVisibilityStatus('Unknown'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("Unknown"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("Unknown"), font=self._getFont("Legend"))[0] + 25
        
        return imgLegend          
                
    def _addLunarFeatureVisibilityMapLegend(self, oImg, iPastePosX):
        # Add legend at bottom of the bitmap (resized to add the legend)
        
        iImgWidth, iImgHeight = oImg.size
        imgLegend = self._changeImageSize(oImg, iImgWidth, iImgHeight + 30)

        drawLegend = ImageDraw.Draw(imgLegend)
        
        iPosY = iImgHeight + 5
        iPosX = iPastePosX + 10
        
        iHeightText = self._getFontSize("Legend")

        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorLunarFeatureVisibility('SunBelowHorizon'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorLunarFeatureVisibility('SunBelowHorizon'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("AtFeatureSunBelowHorizon"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("AtFeatureSunBelowHorizon"), font=self._getFont("Legend"))[0] + 25
        
        for iOcc in range(20, 0, -1):
            fAlt = self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude') / 20.0 * float(iOcc)
            tColor = (255, 127 + int(fAlt / self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude') * 128.0), int(fAlt / self._oParameters.Runtime().getObservation('MaximumLunarFeatureSunAltitude') * 255.0))
            drawLegend.line((iPosX + iOcc, iPosY + (iHeightText / 2), iPosX + iOcc, iPosY + (iHeightText / 2)), fill=tColor)
            drawLegend.line((iPosX + iOcc, iPosY + (iHeightText / 2 + 1), iPosX + iOcc, iPosY + (iHeightText / 2 + 1)), fill=tColor)
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("Observable"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("Observable"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorLunarFeatureVisibility('Good'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorLunarFeatureVisibility('Good'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("NearTerminatorGoodVisibility"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("NearTerminatorGoodVisibility"), font=self._getFont("Legend"))[0] + 25
        
        drawLegend.line((iPosX, iPosY + (iHeightText / 2), iPosX + 20, iPosY + (iHeightText / 2)), fill=self._oParameters.Rendering().getColorLunarFeatureVisibility('SunTooHigh'))
        drawLegend.line((iPosX, iPosY + (iHeightText / 2 + 1), iPosX + 20, iPosY + (iHeightText / 2 + 1)), fill=self._oParameters.Rendering().getColorLunarFeatureVisibility('SunTooHigh'))
        drawLegend.text((iPosX + 25, iPosY), self._oParameters.Localization().getLabel("AtFeatureSunTooHigh"), (255,255,255), font=self._getFont("Legend"))
        iPosX += 25 + drawLegend.textsize(self._oParameters.Localization().getLabel("AtFeatureSunTooHigh"), font=self._getFont("Legend"))[0] + 25
        
        return imgLegend          

        
        
            
    def _addBitmapHeader(self, oCalendar, oImg):
        # Get Style
        iStyleFontSizeH0, theStyleFontH0, tStyleFontColorH0, tStyleBackColorH0 = self._getStyle("BitmapHeaderH0")
        iStyleFontSizeH1, theStyleFontH1, tStyleFontColorH1, tStyleBackColorH1 = self._getStyle("BitmapHeaderH1")
        iStyleFontSizeH2, theStyleFontH2, tStyleFontColorH2, tStyleBackColorH2 = self._getStyle("BitmapHeaderH2")

        # Resize Image and define starting point to draw header
        iImgWidth, iImgHeight = oImg.size
        iTopMarginH0 = self._oParameters.Rendering().getStyles('BitmapHeaderH0TopMargin')
        iBottomMarginH0 = self._oParameters.Rendering().getStyles('BitmapHeaderH0BottomMargin')
        iPaddingTopBottomH0 = self._oParameters.Rendering().getStyles('BitmapHeaderH0PaddingTopBottom')
        iTopMarginH1 = self._oParameters.Rendering().getStyles('BitmapHeaderH1TopMargin')
        iBottomMarginH1 = self._oParameters.Rendering().getStyles('BitmapHeaderH1BottomMargin')
        iPaddingTopBottomH1 = self._oParameters.Rendering().getStyles('BitmapHeaderH1PaddingTopBottom')
        iTopMarginH2 = self._oParameters.Rendering().getStyles('BitmapHeaderH2TopMargin')
        iBottomMarginH2 = self._oParameters.Rendering().getStyles('BitmapHeaderH2BottomMargin')
        iPaddingTopBottomH2 = self._oParameters.Rendering().getStyles('BitmapHeaderH2PaddingTopBottom')
        
        iNewHeight = iImgHeight + iTopMarginH0 + iStyleFontSizeH0 + iBottomMarginH0 + iPaddingTopBottomH0*2 + iTopMarginH1 + iStyleFontSizeH1 + iBottomMarginH1 + iPaddingTopBottomH1*2 + iTopMarginH2 + iStyleFontSizeH2 + iBottomMarginH2 + iPaddingTopBottomH2*2
        
        oNewImg = self._changeImageSize(oImg, iImgWidth, iNewHeight)
        theNewDraw = ImageDraw.Draw(oNewImg) 
        
        # Draw Row 0
        iStartY = iTopMarginH0 + iPaddingTopBottomH0
        sText0 = self._oParameters.Localization().getLabel("EphemerisFor") + ' ' + oCalendar.getFormattedLocalDateForSlot(0,self._oParameters.Rendering().getDisplay('NumberOfMinutesPerSlot'))
        theNewDraw.text((10, iStartY), sText0, tStyleFontColorH0, font=theStyleFontH0)
        iStartY = iStartY + iStyleFontSizeH0 + iPaddingTopBottomH0 + iBottomMarginH0

        # Draw Row 1
        iStartY = iStartY + iTopMarginH1 + iPaddingTopBottomH1
        sText1 = self._oParameters.Localization().getLabel("Place") + ': ' + self._oParameters.Runtime().getPlace().getName()
        theNewDraw.text((10, iStartY), sText1, tStyleFontColorH1, font=theStyleFontH1)
        iStartY = iStartY + iStyleFontSizeH1 + iPaddingTopBottomH1 + iBottomMarginH1
        
        # Draw Row 2
        iStartY = iStartY + iTopMarginH2 + iPaddingTopBottomH2
        sText2 = self._oParameters.Localization().getLabel("CalculusFor") + ' ' + (datetime.now()).strftime("%d/%m/%Y %H:%M") + ' ' + self._oParameters.Localization().getLabel("By") + ' AstroNotifPython ' + self._oParameters.Runtime().getGlobal('CurrentVersion')
        theNewDraw.text((10, iStartY), sText2, tStyleFontColorH2, font=theStyleFontH2)
        iStartY = iStartY + iStyleFontSizeH2 + iPaddingTopBottomH2 + iBottomMarginH2
        
        return iStartY, oNewImg

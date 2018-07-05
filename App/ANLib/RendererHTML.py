#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class RendererHTML
# 
from toolObjectSerializable import toolObjectSerializable
from CommonAstroFormulaes import CommonAstroFormulaes
from MeeusAlgorithms import MeeusAlgorithms
from Tools import Tools
from PIL import Image, ImageDraw
#from toolTrace import toolTrace


class RendererHTML(toolObjectSerializable):
    iLeftLabelWidthInPx = 100
    iHourSlotWidthInPx = 16
    iAltitudeRowHeight = 3

    def __init__(self,sRelateFolderForBitmaps, sURLFolderForBitmaps, bForFavouriteOnly = False):
        toolObjectSerializable.__init__(self)
        self._bForFavouriteOnly = bForFavouriteOnly
        self._sRelativeFolderForBitmaps = sRelateFolderForBitmaps
        self._sURLFolderForBitmaps = sURLFolderForBitmaps
    def __getObjectsTableHeader(self, oCalendar, oParameters, oEphemeridesData, sType):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iNbSlotsPerHour = 60 / oParameters.getDisplayNumberOfMinutesPerSlot()
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())

        sHTML = "            <!-- " + "\n"
        sHTML += "                OBJECT TABLE HEADER" + "\n"
        sHTML += "            -->" + "\n"

        sHTML += '            <TR style="height: 20px;">' + "\n"
        sHTML += '                <!-- Header right-->' + "\n"
        sHTML += '                <TD width="250px"> &nbsp; </TD>' + "\n"
        
        if sType == "Moon":
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoon()
        elif sType == "MoonFeatures":
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoonFeatures()
        elif sType == "Planet":
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForPlanets()
        else:
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForDeepSky()
        
        for iSlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            sHTML += '                <!-- Header ' + oCalendar.getDateForSlot(iSlot,oParameters.getDisplayNumberOfMinutesPerSlot()) + ' -->' + "\n"
            sHTML += '                <TD style="border: 1px solid white;" class="Head18">' + "\n"
            sHTML += '                    <TABLE style="border-collapse: collapse;">' + "\n"
            sHTML += '                        <TR style="height: 20px;">' + "\n"
            sHTML += '                            <TD class="Head18" style="text-align:center;" colspan=24">' + oCalendar.getFormattedDateForSlot(iSlot,oParameters.getDisplayNumberOfMinutesPerSlot()) + '</TD>' + "\n"
            sHTML += '                        </TR>' + "\n"
            sHTML += '                        <TR style="height: 20px;">' + "\n"
            for iDaySlot in range (iSlot,  iSlot + iNbSlotsPerDay, iNbSlotsPerHour ):
                sHTML += '<TD class="Head18">' + oCalendar.getTimeForSlot(iDaySlot, oParameters.getDisplayNumberOfMinutesPerSlot())[0:2] + '</TD>'
            sHTML += '                        </TR>' + "\n"
            sHTML += '                    </TABLE>' + "\n"
            sHTML += '                </TD>' + "\n"
        sHTML += '            </TR>' + "\n"
        
        return sHTML
   
    def __getObjectRow(self, oEphemeridesDataObject, oCalendar, oParameters, oEphemeridesData):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        bIsObservable = False
        sHTMLObjectRow = "            <!--" + "\n"
        sHTMLObjectRow += "                OBJECT ROW : " + oEphemeridesDataObject.getName() + "\n"
        sHTMLObjectRow += "            -->" + "\n"
        sHTMLObjectRow += '            <TR style="border: 1px solid black; padding: 0px; margin:0px;">' + "\n"
        if (oEphemeridesDataObject.getType() == "Moon"):
            sHTMLObjectRow += self.__getObjectRowHeader(oEphemeridesDataObject.getName(), "", "", "")
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoon()
        elif (oEphemeridesDataObject.getType() == "Planet"):
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForPlanets()
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(0) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(0)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0)))
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (near conjonction)'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (near opposition)'
            sHTMLObjectRow += self.__getObjectRowHeader(oEphemeridesDataObject.getName(), "Distance: <B>" +  str(int(round(oEphemeridesDataObject.getDistanceForSlot(0) * 149.600000, 1))) + ' M.Km</B>', "Position Angle : <B>" +  sMeanLongComment + '</B> deg', 'Diam. app. : <B>' + str(int(round(oEphemeridesDataObject.getApparentDiameterInArcSecForSlot(0), 1))) + '</B> "')
        else:
            iMaxSlot = oParameters.getDisplayNumberOfSlotsForDeepSky()
            sHTMLObjectRow += self.__getObjectRowHeader(oEphemeridesDataObject.getName(), '<B>' + oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getType() + '</B>', "RA: <B>" + CommonAstroFormulaes.getHMSFromDeg(oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getRA()) + "</B>&nbsp;&nbsp;-&nbsp;&nbsp;Dec: <B>" +  str(round(oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getDec(),2)) + '</B>', oParameters.getSkyObjects().getSkyObjectByID(oEphemeridesDataObject.getID()).getComment1())
        for iDaySlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            sHTML =  self.__getObjectVisibilityTableForDay( oEphemeridesDataObject, oCalendar, oParameters, iDaySlot, iDaySlot + iNbSlotsPerDay, oEphemeridesData)
            if len(sHTML) > 0 and sHTML[0:23] != "<!-- Not Observable -->":
                bIsObservable = True
            sHTMLObjectRow += sHTML
        sHTMLObjectRow += "            </TR>" + "\n"
        
        if bIsObservable or oParameters.getObservationAlways():
            return sHTMLObjectRow
        else:
            return ""
        
    def __getObjectRowHeader(self, sObjectName, sObjectDataRow1, sObjectDataRow2, sObjectDataRow3):
        sHTML='                <!-- Object header -->' + "\n"
        sHTML += '                <TD align="center">' + "\n"
        sHTML += '                    <TABLE style="border:none; border-collapse: collapse">' + "\n"
        sHTML += '                        <TR>' + "\n"
        sHTML += '                            <TD class="ObjectBitmap">&nbsp;</TD>' + "\n"
        sHTML += '                            <TD class="ObjectName">' + sObjectName + '</TD>' + "\n"
        sHTML += '                        </TR>' + "\n"
        sHTML += '                        <TR>' + "\n"
        sHTML += '                            <TD colspan=2 class="ObjectDataRow">' + sObjectDataRow1 + '</TD>' + "\n"
        sHTML += '                        </TR>' + "\n"
        sHTML += '                        <TR>' + "\n"
        sHTML += '                            <TD colspan=2 class="ObjectDataRow">' + sObjectDataRow2 + '</TD>' + "\n"
        sHTML += '                        </TR>' + "\n"
        sHTML += '                        <TR>' + "\n"
        sHTML += '                            <TD colspan=2 class="ObjectDataRow">' + sObjectDataRow3 + '</TD>' + "\n"
        sHTML += '                        </TR>' + "\n"
        sHTML += '                    </TABLE>' + "\n"
        sHTML += '                </TD>' + "\n"
        return sHTML
        
    def __getObjectVisibilityTableForDay(self, oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, oEphemeridesData):
        bIsObservable = False
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        
        sHTML='                <!-- Visibility Data Day ' + oCalendar.getDateForSlot(iStartSlot,oParameters.getDisplayNumberOfMinutesPerSlot()) + ' -->' + "\n"
        sHTML += '                <TD style="border: 1px solid white; padding: 0px; margin:0px;">' + "\n"
        sHTML += '                    <TABLE style="border:none; border-collapse: collapse;">' + "\n"
        
        if oParameters.getDisplayVisibilityTableAsBitmap():
            sHTML += '                        <TR style="height:' + str(RendererHTML.iAltitudeRowHeight) + 'px;">' + "\n"
            sImgTag = self.__getObjectVisibilityBitmapForDay2(oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, oEphemeridesData)
            sHTML += '<TD style="padding: 0px; margin:0px;">' + sImgTag + '</TD>' + "\n"
            if sImgTag[0:4] != '<!--': bIsObservable = True
            sHTML += '                        </TR>' + "\n"        
        else:
            for iRowAltitude in range(90, 0, -5):
                sHTML += '                        <TR style="height:' + str(RendererHTML.iAltitudeRowHeight) + 'px;">   <!-- Altitude: ' + str(iRowAltitude) + '-->' + "\n"
                for iSlot in range(iStartSlot, iEndSlot):
                    if oEphemeridesDataObject.getAltitudeForSlot(iSlot) <= float(iRowAltitude) and oEphemeridesDataObject.getAltitudeForSlot(iSlot) > float(iRowAltitude - 5):
                        sClassName = self.getDataClassForObjectAltitudeDependingOnSunAltitude(oEphemeridesDataObject.getID(), oEphemeridesDataObject.getCategory(), oEphemeridesDataObject.getAzimutForSlot(iSlot),  oEphemeridesDataObject.getAltitudeForSlot(iSlot), oEphemeridesData.getSunAltitudeForSlot(iSlot), oParameters.getPlace(), oParameters)
                        if sClassName == "DatG": bIsObservable = True
                    else:
                        sClassName = self.getBackClassForBackgroundDependingonSunAltitude(oEphemeridesData.getSunAltitudeForSlot(iSlot))
                    sHTML += '<TD class="' + sClassName + '">&nbsp;</TD>'
                sHTML += '                        </TR>' + "\n"

        sHTML += '                        <TR style="height:5px;">' + "\n"
        if oEphemeridesDataObject.getType() == "Planet":
            fDiffMeanLong = oEphemeridesData.getSunMeanLongInDegForSlot(iStartSlot) - 180.0 - oEphemeridesDataObject.getMeanLongForSlot(iStartSlot)
            while fDiffMeanLong < 0:  
                fDiffMeanLong = fDiffMeanLong + 360
            if fDiffMeanLong > 180: fDiffMeanLong = 360 - fDiffMeanLong
            sMeanLongComment = str(int(round(fDiffMeanLong, 0)))
            if fDiffMeanLong < 25: sMeanLongComment = sMeanLongComment + ' (near conjonction)'
            if fDiffMeanLong > 155: sMeanLongComment = sMeanLongComment + ' (near opposition)'
            sHTML += '                            <TD class="ObjectAdditionalData" colspan=' + str(iNbSlotsPerDay) + '>Culm. ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', azimut ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot)) + ' </TD>' + "\n"
        elif oEphemeridesDataObject.getType() == "Moon":
            sHTML += '                            <TD class="ObjectAdditionalData" colspan=' + str(iNbSlotsPerDay) + '>Dist: ' + str(int(round(oEphemeridesDataObject.getDistanceForSlot(iStartSlot)))) + ' Km    Phase: ' + str(int(round(oEphemeridesDataObject.getPhaseForSlot(iStartSlot)))) + '   Illum: ' + str(int(round(oEphemeridesDataObject.getIlluminationForSlot(iStartSlot)))) + '%    Colong: ' + str(int(round(oEphemeridesDataObject.getColongitudeForSlot(iStartSlot)))) + '       Culm. ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', azimut ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot)) + '</TD>' + "\n"
        else:
            sHTML += '                            <TD class="ObjectAdditionalData" colspan=' + str(iNbSlotsPerDay) + '>Culm. ' + str(oEphemeridesDataObject.getCulminAltitude(iStartSlot, iEndSlot)) + ', azimut ' + str(oEphemeridesDataObject.getCulminAzimut(iStartSlot, iEndSlot)) + '</TD>' + "\n"
    
        sHTML += '                        </TR>' + "\n"
        sHTML += '                    </TABLE>' + "\n"
        sHTML += '                </TD>' + "\n"

        if bIsObservable or oParameters.getObservationAlways():        
            return sHTML
        else:
            return "<!-- Not Observable -->" + sHTML

    def __getObjectVisibilityBitmapForDay(self, oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, oEphemeridesData):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iNbRow = 90 / 5
        bIsObservable = False
        # create image and draw objects
        img = Image.new( 'RGB', (iSlotWidthInPx * iNbSlotsPerDay, iNbRow * RendererHTML.iAltitudeRowHeight - 1), "black") # create a new black image
        draw = ImageDraw.Draw(img)
        # draw table
        for iRowAltitude in range(90, 0, -5):
            iRow = iRowAltitude / 5
            y1 = (iNbRow * RendererHTML.iAltitudeRowHeight) - (iRow * RendererHTML.iAltitudeRowHeight)
            y2 = y1 + RendererHTML.iAltitudeRowHeight - 1
            for iSlot in range(iStartSlot, iEndSlot):
                x1 = (iSlot - iStartSlot) * iSlotWidthInPx
                x2 = x1 + iSlotWidthInPx - 1
                if oEphemeridesDataObject.getAltitudeForSlot(iSlot) <= float(iRowAltitude) and oEphemeridesDataObject.getAltitudeForSlot(iSlot) > float(iRowAltitude - 5):
                    tColor = self.getBitmapColorForObjectAltitudeDependingOnSunAltitude(oEphemeridesDataObject.getID(), oEphemeridesDataObject.getCategory(), oEphemeridesDataObject.getAzimutForSlot(iSlot),  oEphemeridesDataObject.getAltitudeForSlot(iSlot), oEphemeridesData.getSunAltitudeForSlot(iSlot), oParameters.getPlace(), oParameters)
                    if tColor == (0, 255, 0): bIsObservable = True
                else:
                    tColor = self.getBitmapColorforSunAltitude(oEphemeridesData.getSunAltitudeForSlot(iSlot))
                draw.rectangle((x1, y1, x2, y2), fill=tColor)
        del draw        
        sBitmapName = 'AN_'+ oEphemeridesDataObject.getID() + "-" + str(iStartSlot) + '.jpg'
        img.save(self._sRelativeFolderForBitmaps + sBitmapName, "JPEG")
        
        sHTML = '<IMG style="border:none" src="' + self._sURLFolderForBitmaps + sBitmapName + '" alt="' + sBitmapName + '" height="' + str(iNbRow * RendererHTML.iAltitudeRowHeight - 1) + '" width="' + str(iNbSlotsPerDay * iSlotWidthInPx) + '">'
        if bIsObservable or oParameters.getObservationAlways():        
            return sHTML
        else:
            return "<!-- Not Observable -->" + sHTML

    def __getObjectVisibilityBitmapForDay2(self, oEphemeridesDataObject, oCalendar, oParameters, iStartSlot, iEndSlot, oEphemeridesData):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iNbRow = 90 / 5
        bIsObservable = False
        # create image and draw objects
        iBitmapHeight = iNbRow * RendererHTML.iAltitudeRowHeight - 1
        iBitmapWidth = iSlotWidthInPx * iNbSlotsPerDay
        img = Image.new( 'RGB', (iBitmapWidth, iBitmapHeight), "black") # create a new black image
        draw = ImageDraw.Draw(img)
        # draw table
        iPrevX = -1
        iPrevY = -1
        for iRowAltitude in range(90, 0, -5):
            iRow = iRowAltitude / 5
            y1 = (iNbRow * RendererHTML.iAltitudeRowHeight) - (iRow * RendererHTML.iAltitudeRowHeight)
            y2 = y1 + RendererHTML.iAltitudeRowHeight - 1
            for iSlot in range(iStartSlot, iEndSlot):
                x1 = (iSlot - iStartSlot) * iSlotWidthInPx
                x2 = x1 + iSlotWidthInPx - 1
                tColor = self.getBitmapColorforSunAltitude(oEphemeridesData.getSunAltitudeForSlot(iSlot))
                draw.rectangle((x1, y1, x2, y2), fill=tColor)
        for iSlot in range(iStartSlot, iEndSlot):
            x = (iSlot - iStartSlot) * iSlotWidthInPx + (iSlotWidthInPx/2) - 1
            y = iBitmapHeight - int(float( oEphemeridesDataObject.getAltitudeForSlot(iSlot) / 90.0) * float(iBitmapHeight))
            if oEphemeridesDataObject.getAltitudeForSlot(iSlot) > 0:
                tColor = self.getBitmapColorForObjectAltitudeDependingOnSunAltitude(oEphemeridesDataObject.getID(), oEphemeridesDataObject.getCategory(), oEphemeridesDataObject.getAzimutForSlot(iSlot),  oEphemeridesDataObject.getAltitudeForSlot(iSlot), oEphemeridesData.getSunAltitudeForSlot(iSlot), oParameters.getPlace(), oParameters)
                if tColor == (0, 255, 0): bIsObservable = True
                if iPrevX > -1 and iPrevY > -1:
                    draw.line((iPrevX, iPrevY, x, y), fill=tColor)
                    draw.line((iPrevX, iPrevY -1, x, y -1 ), fill=tColor)
            iPrevX = x
            iPrevY = y
        del draw        
        sBitmapName = 'AN_'+ oEphemeridesDataObject.getID() + "-" + str(iStartSlot) + '.jpg'
        img.save(self._sRelativeFolderForBitmaps + sBitmapName, "JPEG")
        
        sHTML = '<IMG style="border:none" src="' + self._sURLFolderForBitmaps + sBitmapName + '" alt="' + sBitmapName + '" height="' + str(iNbRow * RendererHTML.iAltitudeRowHeight - 1) + '" width="' + str(iNbSlotsPerDay * iSlotWidthInPx) + '">'
        if bIsObservable or oParameters.getObservationAlways():        
            return sHTML
        else:
            return "<!-- Not Observable -->" + sHTML

    def getBitmapColorForObjectAltitudeDependingOnSunAltitude(self, fObjectID, fObjectCategory, fObjectAZimut, fObjectAltitude, fSunAltitude, oPlace, oParameters):
        # DatH - Hidden: object is visible but hidden by something
        # DatI - Impossible:  object is visible but sun makes it impossible to see
        # DatD - Difficult: object is visible but sun makes it difficult to see
        # DatB - Below : object is below horizon
        # DatV - VeryLow: object is visible but very low   (<15)
        # DatL - Low: object is visible but low  (<35)
        # DatG - Good
        fDisplayMaxAltitudeForObjectVeryLow = oParameters.getDisplayMaxAltitudeForObjectVeryLow()
        fDisplayMaxAltitudeForObjectLow = oParameters.getDisplayMaxAltitudeForObjectLow()
        fDisplayMaxSunAltitudeForObservableDeepSky = oParameters.getDisplayMaxSunAltitudeForObservableDeepSky()
        fDisplayMaxSunAltitudeForObservableBrightObjects = oParameters.getDisplayMaxSunAltitudeForObservableBrightObjects()
        fDisplayMaxSunAltitudeForDifficultBrightObjects = oParameters.getDisplayMaxSunAltitudeForDifficultBrightObjects()
        fDisplayMaxSunAltitudeFoImpossibleBrightObjects = oParameters.getDisplayMaxSunAltitudeFoImpossibleBrightObjects()
        fDisplayMaxSunAltitudeForObservableMediumObjects = oParameters.getDisplayMaxSunAltitudeForObservableMediumObjects()
        fDisplayMaxSunAltitudeForDifficultMediumObjects = oParameters.getDisplayMaxSunAltitudeForDifficultMediumObjects()

        # Below horizon and hidden
        if fObjectAltitude < 0.0:
            tColor = (153, 153, 153)
        elif oPlace.getObstructedSkyAreas().getVisibilityStatus(fObjectAZimut, fObjectAltitude) == "0":
            tColor = (195, 0, 255)
        # Deepsky
        elif fObjectCategory == "DeepSky":
            if fSunAltitude <= fDisplayMaxSunAltitudeForObservableDeepSky:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    tColor = (253, 100, 0)
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    tColor = (253, 134, 0)
                else:
                    tColor = (0, 255, 0)
            else:
                tColor = (28, 69, 135)            
        # Bright Planet and Moon
        elif fObjectID == "Moon" or fObjectID == "Venus" or fObjectID == "Jupiter":
            if fSunAltitude < fDisplayMaxSunAltitudeForObservableBrightObjects:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    tColor = (253, 100, 0)
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    tColor = (253, 134, 0)
                else:
                    tColor = (0, 255, 0)
            elif fSunAltitude < fDisplayMaxSunAltitudeForDifficultBrightObjects:
                tColor = (255, 0, 0)
            elif fSunAltitude < fDisplayMaxSunAltitudeFoImpossibleBrightObjects:
                if fObjectID == "Moon":
                    tColor = (255, 0, 0)
                else:
                    tColor = (28, 69, 135)
            else:
                tColor = (28, 69, 135)
        # Medium objects
        else:
            if fSunAltitude < fDisplayMaxSunAltitudeForObservableMediumObjects:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    tColor = (253, 100, 0)
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    tColor = (253, 134, 0)
                else:
                    tColor = (0, 255, 0)
            elif fSunAltitude < fDisplayMaxSunAltitudeForDifficultMediumObjects:
                tColor = (255, 0, 0)
            else:
                tColor = (28, 69, 135)
            
        return tColor


    def getBitmapColorforSunAltitude(self, fSunAltitude):
        if fSunAltitude < -18.0:
            tColor = (0, 0, 0)
        elif fSunAltitude < -12.0:
            tColor = ((28, 69, 135))
        elif fSunAltitude < -6.0:
            tColor = (17, 85, 204)
        elif fSunAltitude < -0.0:
            tColor = (60, 120, 216)
        elif fSunAltitude < 6.0:
            tColor = (249, 203, 156)
        elif fSunAltitude < 12.0:
            tColor = (255, 242, 204)
        else:
            tColor = (255, 255, 255)
        return tColor
            
    def getBackClassForBackgroundDependingonSunAltitude(self, fSunAltitude):
        if fSunAltitude < -18.0:
            sClassName = "Bck18"
        elif fSunAltitude < -12.0:
            sClassName = "Bck12"
        elif fSunAltitude < -6.0:
            sClassName = "Bck6"
        elif fSunAltitude < -0.0:
            sClassName = "Bck0"
        elif fSunAltitude < 6.0:
            sClassName = "BckSL"
        elif fSunAltitude < 12.0:
            sClassName = "BckSH"
        else:
            sClassName = "BckSV"
        return sClassName

    def getDataClassForObjectAltitudeDependingOnSunAltitude(self, fObjectID, fObjectCategory, fObjectAZimut, fObjectAltitude, fSunAltitude, oPlace, oParameters):
        # DatH - Hidden: object is visible but hidden by something
        # DatI - Impossible:  object is visible but sun makes it impossible to see
        # DatD - Difficult: object is visible but sun makes it difficult to see
        # DatB - Below : object is below horizon
        # DatV - VeryLow: object is visible but very low   (<15)
        # DatL - Low: object is visible but low  (<35)
        # DatG - Good
        fDisplayMaxAltitudeForObjectVeryLow = oParameters.getDisplayMaxAltitudeForObjectVeryLow()
        fDisplayMaxAltitudeForObjectLow = oParameters.getDisplayMaxAltitudeForObjectLow()
        fDisplayMaxSunAltitudeForObservableDeepSky = oParameters.getDisplayMaxSunAltitudeForObservableDeepSky()
        fDisplayMaxSunAltitudeForObservableBrightObjects = oParameters.getDisplayMaxSunAltitudeForObservableBrightObjects()
        fDisplayMaxSunAltitudeForDifficultBrightObjects = oParameters.getDisplayMaxSunAltitudeForDifficultBrightObjects()
        fDisplayMaxSunAltitudeFoImpossibleBrightObjects = oParameters.getDisplayMaxSunAltitudeFoImpossibleBrightObjects()
        fDisplayMaxSunAltitudeForObservableMediumObjects = oParameters.getDisplayMaxSunAltitudeForObservableMediumObjects()
        fDisplayMaxSunAltitudeForDifficultMediumObjects = oParameters.getDisplayMaxSunAltitudeForDifficultMediumObjects()

        # Below horizon and hidden
        if fObjectAltitude < 0.0:
            sClassName = "B"
        elif oPlace.getObstructedSkyAreas().getVisibilityStatus(fObjectAZimut, fObjectAltitude) == "0":
            sClassName = "H"
        # Deepsky
        elif fObjectCategory == "DeepSky":
            if fSunAltitude <= fDisplayMaxSunAltitudeForObservableDeepSky:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    sClassName = "V"
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    sClassName = "L"
                else:
                    sClassName = "G"
            else:
                sClassName = "I"            
        # Bright Planet and Moon
        elif fObjectID == "Moon" or fObjectID == "Venus" or fObjectID == "Jupiter":
            if fSunAltitude < fDisplayMaxSunAltitudeForObservableBrightObjects:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    sClassName = "V"
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    sClassName = "L"
                else:
                    sClassName = "G"
            elif fSunAltitude < fDisplayMaxSunAltitudeForDifficultBrightObjects:
                sClassName = "D"
            elif fSunAltitude < fDisplayMaxSunAltitudeFoImpossibleBrightObjects:
                if fObjectID == "Moon":
                    sClassName = "D"
                else:
                    sClassName = "I"
            else:
                sClassName = "I"
        # Medium objects
        else:
            if fSunAltitude < fDisplayMaxSunAltitudeForObservableMediumObjects:
                if fObjectAltitude < fDisplayMaxAltitudeForObjectVeryLow:
                    sClassName = "V"
                elif fObjectAltitude < fDisplayMaxAltitudeForObjectLow:
                    sClassName = "L"
                else:
                    sClassName = "G"
            elif fSunAltitude < fDisplayMaxSunAltitudeForDifficultMediumObjects:
                sClassName = "D"
            else:
                sClassName = "I"
            
        return ( 'Dat' + sClassName)

   
    def __getLunarFeatureRow(self, oLunarFeatureObject, oCalendar, oParameters, oEphemeridesData):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        sPictureName = Tools.getGenerateMoonFeatureBitmap(self._sRelativeFolderForBitmaps, oLunarFeatureObject.getID(), oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), 35, 35, 5)
        sHTMLObjectRow = "            <!--" + "\n"
        sHTMLObjectRow += "                LUNAR FEATURE ROW : " + oLunarFeatureObject.getName() + "\n"
        sHTMLObjectRow += "            -->" + "\n"
        sHTMLObjectRow += '            <TR style="border: 1px solid black; padding: 0px; margin:0px;">' + "\n"
        sHTMLObjectRow += '                <!-- Object header -->' + "\n"
        sHTMLObjectRow += '                <TD align="center">' + "\n"
        sHTMLObjectRow += '                    <TABLE style="border:none; border-collapse: collapse">' + "\n"
        sHTMLObjectRow += '                        <TR>' + "\n"
        sHTMLObjectRow += '                            <TD class="ObjectBitmap"><IMG src="' + self._sURLFolderForBitmaps + sPictureName + '" style="width:35px; height:35px; "></TD>' + "\n"
        sHTMLObjectRow += '                            <TD class="ObjectName">' + oLunarFeatureObject.getName() + '</TD>' + "\n"
        sHTMLObjectRow += '                        </TR>' + "\n"
        sHTMLObjectRow += '                        <TR>' + "\n"
        sHTMLObjectRow += '                            <TD class="ObjectDataName">Lat: ' + str(oLunarFeatureObject.getLatitude()) + '</TD>' + "\n"
        sHTMLObjectRow += '                            <TD class="ObjectDataName">Long: ' + str(oLunarFeatureObject.getLongitude()) + '</TD>' + "\n"
        sHTMLObjectRow += '                        </TR>' + "\n"
        sHTMLObjectRow += '                    </TABLE>' + "\n"
        sHTMLObjectRow += '                </TD>' + "\n"
        iMaxSlot = oParameters.getDisplayNumberOfSlotsForMoonFeatures()
        bToBeDisplayed = False
        for iDaySlot in range (0,  iMaxSlot, iNbSlotsPerDay ):
            sHTMLObjectRow += '                <!-- Visibility Data Day -->' + "\n"
            sHTMLObjectRow += '                <TD style="border: 1px solid white; padding: 0px; margin:0px;">' + "\n"
            sHTMLObjectRow += '                    <TABLE style="border:none; border-collapse: collapse;">' + "\n"
            sHTMLObjectRow += '                        <TR style="height:35px;">' + "\n"
            if oParameters.getDisplayVisibilityTableAsBitmap():
                sHTMLBitmap = self.__getLunarFeatureVisibilityBitmapForDay(iDaySlot, iDaySlot + iNbSlotsPerDay, oLunarFeatureObject, oCalendar, oParameters, oEphemeridesData)
                sHTMLObjectRow += '<TD style="padding: 0px; margin:0px;">' + sHTMLBitmap + '</TD>'
                if sHTMLBitmap[0:23] != "<!-- Not Observable -->":
                    bToBeDisplayed = True
            else:
                for iSlot in range(iDaySlot, iDaySlot + iNbSlotsPerDay):
                    fSunAltitudeOverFeature = MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iSlot))
                    if fSunAltitudeOverFeature > 0.0 and fSunAltitudeOverFeature <= oParameters.getObservationMaximumLunarFeatureSunAltitude():
                        bToBeDisplayed = True
                    if fSunAltitudeOverFeature <= 0.0:
                        sClassName = "MooF00"
                    elif fSunAltitudeOverFeature <= 10.0:
                        sClassName = "MooF10"
                    elif fSunAltitudeOverFeature <= 20.0:
                        sClassName = "MooF20"
                    elif fSunAltitudeOverFeature <= 30.0:
                        sClassName = "MooF30"
                    elif fSunAltitudeOverFeature <= 40.0:
                        sClassName = "MooF40"
                    elif fSunAltitudeOverFeature <= 50.0:
                        sClassName = "MooF50"
                    elif fSunAltitudeOverFeature <= 60.0:
                        sClassName = "MooF60"
                    elif fSunAltitudeOverFeature <= 70.0:
                        sClassName = "MooF70"
                    elif fSunAltitudeOverFeature <= 80.0:
                        sClassName = "MooF80"
                    else:
                        sClassName = "MooF90"
                    sHTMLObjectRow += '<TD class="' + sClassName + '">&nbsp;</TD>'
            sHTMLObjectRow += '                        </TR>' + "\n"
            sHTMLObjectRow += '                        <TR style="height:5px;">' + "\n"
            if oParameters.getDisplayVisibilityTableAsBitmap():
                sHTMLObjectRow += '                            <TD class="ObjectAdditionalData">Sun Altitude: ' + str(int(round(MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDaySlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDaySlot))))) + '  Sun Azimut: ' + str(int(round(MeeusAlgorithms.getSunAzimutFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDaySlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDaySlot))))) + '</TD>'
            else:
                sHTMLObjectRow += '                            <TD class="ObjectAdditionalData" colspan=' + str(iNbSlotsPerDay) + '>Sun Altitude: ' + str(int(round(MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDaySlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDaySlot))))) + '  Sun Azimut: ' + str(int(round(MeeusAlgorithms.getSunAzimutFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iDaySlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iDaySlot))))) + '</TD>'
            sHTMLObjectRow += '                        </TR>' + "\n"
            sHTMLObjectRow += '                    </TABLE>' + "\n"
            sHTMLObjectRow += '                </TD>' + "\n"
        sHTMLObjectRow += "            </TR>" + "\n"
        if bToBeDisplayed:
            return sHTMLObjectRow
        else:
            return ""

    def __getLunarFeatureVisibilityBitmapForDay(self, iStartSlot, iEndSlot, oLunarFeatureObject, oCalendar, oParameters, oEphemeridesData):
        iNbSlotsPerDay = (1440 / oParameters.getDisplayNumberOfMinutesPerSlot())
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        bToBeDisplayed = False
        # create image and draw objects
        img = Image.new( 'RGB', (iSlotWidthInPx * iNbSlotsPerDay, 35), "black") # create a new black image
        draw = ImageDraw.Draw(img)
        # draw table
        for iSlot in range(iStartSlot, iEndSlot):
            fSunAltitudeOverFeature = MeeusAlgorithms.getSunAltitudeFromMoonFeature(oLunarFeatureObject.getLongitude(), oLunarFeatureObject.getLatitude(), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLongitudeForSlot(iSlot), oEphemeridesData.getEphemerideDataObject("Moon").getSelenographicLatitudeForSlot(iSlot))
            if fSunAltitudeOverFeature > 0.0 and fSunAltitudeOverFeature <= oParameters.getObservationMaximumLunarFeatureSunAltitude():
                bToBeDisplayed = True
            if fSunAltitudeOverFeature <= 0.0:
                tColor = (0, 0, 0)
            elif fSunAltitudeOverFeature <= 10.0:
                tColor = (255, 136, 0)
            elif fSunAltitudeOverFeature <= 20.0:
                tColor = (255, 171, 76)
            elif fSunAltitudeOverFeature <= 30.0:
                tColor = (255, 202, 142)
            elif fSunAltitudeOverFeature <= 40.0:
                tColor = (209, 205, 200)
            elif fSunAltitudeOverFeature <= 50.0:
                tColor = (229, 226, 222)
            elif fSunAltitudeOverFeature <= 60.0:
                tColor = (237, 235, 232)
            elif fSunAltitudeOverFeature <= 70.0:
                tColor = (249, 248, 247)
            elif fSunAltitudeOverFeature <= 80.0:
                tColor = (255, 255, 255)
            else:
                tColor = (255, 255, 255)
            x1 = (iSlot - iStartSlot) * iSlotWidthInPx
            x2 = x1 + iSlotWidthInPx - 1
            y1 = 0
            y2 = 35
            draw.rectangle((x1, y1, x2, y2), fill=tColor)
        del draw        
        sBitmapName = 'AN_'+ oLunarFeatureObject.getID() + "-" + str(iStartSlot) + '.jpg'
        img.save(self._sRelativeFolderForBitmaps + sBitmapName, "JPEG")
        sHTML = '<IMG style="border:none" src="' + self._sURLFolderForBitmaps + sBitmapName + '" alt="' + sBitmapName + '" height="35" width="' + str(iNbSlotsPerDay * iSlotWidthInPx) + '">'
        if bToBeDisplayed or oParameters.getObservationAlways():        
            return sHTML
        else:
            return "<!-- Not Observable -->" + sHTML

        
    def getObjectEphemeridesTableForMoonHTML(self, oCalendar, oParameters, oEphemeridesData):
        sHTML = '       <TABLE style="table-layout: fixed; border-collapse: collapse;  border: 1px solid black; padding: 0px; margin:0px;">' + "\n"
        sHTML += self.__getObjectsTableHeader(oCalendar, oParameters, oEphemeridesData, "Moon")
        sHTMLData = self.__getObjectRow(oEphemeridesData.getEphemerideDataObject("Moon"), oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLData) > 0 and (not self._bForFavouriteOnly or oParameters.getSkyObjects().getSkyObjectByID("Moon").getIsFavourite()):
            sHTML += sHTMLData
            sHTML += '       </TABLE>' + "\n"
            return sHTML
        else:
            return ""

    def getObjectEphemeridesTableForPlanetsHTML(self, oCalendar, oParameters, oEphemeridesData):
        sHTML = '       <TABLE style="table-layout: fixed; border-collapse: collapse;  border: 1px solid black; padding: 0px; margin:0px;">' + "\n"
        sHTML += self.__getObjectsTableHeader(oCalendar, oParameters, oEphemeridesData, "Planet")
        sHTMLData = ""
        for iObjectIndex in range(0, oParameters.getSkyObjects().getCount()):
            if oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getType() == 'Planet':
                if not self._bForFavouriteOnly or oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    sHTMLData += self.__getObjectRow(oEphemeridesData.getEphemerideDataObject(oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLData) > 0:
            sHTML += sHTMLData
            sHTML += '       </TABLE>' + "\n"
            return sHTML
        else:
            return ""

    def getObjectEphemeridesTableForDeepSkyHTML(self, oCalendar, oParameters, oEphemeridesData):
        sHTML = '       <TABLE style="table-layout: fixed; border-collapse: collapse;  border: 1px solid black; padding: 0px; margin:0px;">' + "\n"
        sHTML += self.__getObjectsTableHeader(oCalendar, oParameters, oEphemeridesData, "DeepSky")
        sHTMLData = ""
        for iObjectIndex in range(0, oParameters.getSkyObjects().getCount()):
            if oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getCategory() == 'DeepSky':
                if not self._bForFavouriteOnly or oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getIsFavourite():
                    sHTMLData += self.__getObjectRow(oEphemeridesData.getEphemerideDataObject(oParameters.getSkyObjects().getSkyObjectByIndex(iObjectIndex).getID()), oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLData) > 0:
            sHTML += sHTMLData
            sHTML += '       </TABLE>' + "\n"
            return sHTML
        else:
            return ""

    def getLunarFeaturesEphemeridesTableHTML(self, oCalendar, oParameters, oEphemeridesData):
        sHTML = '       <TABLE style="table-layout: fixed; border-collapse: collapse;  border: 1px solid black; padding: 0px; margin:0px;">' + "\n"
        sHTML += self.__getObjectsTableHeader(oCalendar, oParameters, oEphemeridesData, "MoonFeatures")
        sHTMLData = ""
        for iObjectIndex in range(0, oParameters.getLunarFeatures().getCount()):
            if not self._bForFavouriteOnly or oParameters.getLunarFeatures().getLunarFeatureByIndex(iObjectIndex).getIsFavourite():
                sHTMLData += self.__getLunarFeatureRow(oParameters.getLunarFeatures().getLunarFeatureByIndex(iObjectIndex), oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLData) > 0:
            sHTML += sHTMLData
            sHTML += '       </TABLE>' + "\n"
            return sHTML
        else:
            return ""

    def getHTML(self, oCalendar, oParameters, oEphemeridesData):
        iSlotWidthInPx = RendererHTML.iHourSlotWidthInPx / (60 / oParameters.getDisplayNumberOfMinutesPerSlot())
        sHTML = self.getHTMLHeaderComment(oCalendar, oParameters) + "\n"
        sHTML += '<HTML>' + "\n"
        sHTML += '	<HEAD>' + "\n"
        sHTML += '		<base href="">' + "\n"
        sHTML += '		<style>' + "\n"
        sHTML += '          H1                        {font-family: "arial", "sans-serif"; font-size:30px; font-weight: normal; background: #6dc7ff; color: #000000; padding-top: 15px; padding-bottom: 15px;}' + "\n"
        sHTML += '          H2                        {font-family: "arial", "sans-serif"; font-size:25px; background: #bfdafc; color: #000000; padding-top: 10px; padding-bottom: 10px;}' + "\n"
        sHTML += '          TR                        {border: none;}' + "\n"
        sHTML += '          TD.Head18                 {font-family: "arial", "sans-serif"; font-style: normal; font-size:10px; border: none;color:#ffffff; background:#000000; padding: 0px; margin:0px; min-width:' + str(RendererHTML.iHourSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.Head00                 {font-family: "arial", "sans-serif"; font-style: normal; font-size:12px; border: none;color:#ffffff; background:#3c78d8; padding: 0px; margin:0px; min-width:' + str(RendererHTML.iHourSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.Hour06                 {font-family: "arial", "sans-serif"; font-style: normal; font-size:12px; border: none;color:#ffffff; background:#1155cc; padding: 0px; margin:0px; min-width:' + str(RendererHTML.iHourSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.Hour12                 {font-family: "arial", "sans-serif"; font-style: normal; font-size:12px; border: none;color:#ffffff; background:#1c4587; padding: 0px; margin:0px; min-width:' + str(RendererHTML.iHourSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.HourSL                 {font-family: "arial", "sans-serif"; font-style: normal; font-size:12px; border: none;color:#000000; background:#f9cb9c; padding: 0px; margin:0px; min-width:' + str(RendererHTML.iHourSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.HourSH                 {font-family: "arial", "sans-serif"; font-style: normal; font-size:12px; border: none;color:#000000; background:#fff2cc; padding: 0px; margin:0px; min-width:' + str(RendererHTML.iHourSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD                        {border: none; font-size:1px; }' + "\n"
        sHTML += '          TD.MooF00                 {background:#000000; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF10                 {background:#ff8800; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF20                 {background:#ffab4c; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF30                 {background:#ffca8e; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF40                 {background:#d1cdc8; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF50                 {background:#e5e2de; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF60                 {background:#edebe8; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF70                 {background:#f9f8f7; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF80                 {background:#ffffff; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.MooF90                 {background:#ffffff; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px}' + "\n"
        sHTML += '          TD.Bck18                  {background:#000000; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.Bck12                  {background:#1c4587; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.Bck6                   {background:#1155cc; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.Bck0                   {background:#3c78d8; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.BckSL                  {background:#f9cb9c; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.BckSH                  {background:#fff2cc; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.BckSV                  {background:#ffffff; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatH                   {background:#c300ff; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatI                   {background:#1c4587; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatD                   {background:#ff0000; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatB                   {background:#999999; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatV                   {background:#fd6400; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatL                   {background:#fd8600; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.DatG                   {background:#00ff00; padding: 0px; margin:0px; min-width:' + str(iSlotWidthInPx) + 'px; height:' + str(RendererHTML.iAltitudeRowHeight) + 'px}' + "\n"
        sHTML += '          TD.ObjectBitmap           {min-width: 40px; vertical-align:middle; align: center; border: none; font-family: "arial", "sans-serif"; font-size:20px;}' + "\n"
        sHTML += '          TD.ObjectName             {min-width: 210px; vertical-align:middle; align: left; border: none; font-family: "arial", "sans-serif"; font-size:20px;}' + "\n"
        sHTML += '          TD.ObjectDataRow          {border: none; font-family: "arial", "sans-serif"; font-size:9px; text-align: center; }' + "\n"
        sHTML += '          TD.ObjectAdditionalData   {background:#bbbbbb; border: none; font-family: "arial", "sans-serif"; font-size:8px; text-align:left;}' + "\n"
        sHTML += '          TD.BackSeeingOK           {background:#00ff00;}' + "\n"
        sHTML += '          P.Category                {padding-top: 15px; padding-bottom: 15px;}' + "\n"
        sHTML += '		</style>' + "\n"
        sHTML += '	</head>' + "\n"
        sHTML += '<BODY>' + "\n"

        sHTML += '    <H1>&nbsp;&nbsp;<A href="http://astronot.heliohost.org" target="_blank">Ephemerides du <SPAN style="font-weight: bold">' + oCalendar.getFormattedDateForSlot(0,oParameters.getDisplayNumberOfMinutesPerSlot()) + '</SPAN></A>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<SPAN style="font-size:20px">Lieu: ' + oParameters.getPlace().getName() + ' </SPAN></H1>' + "\n"
        sHTMLDataPlanets = self.getObjectEphemeridesTableForPlanetsHTML(oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLDataPlanets) >0 :
            sHTML += '<P class="Category"><H2>&nbsp;Les Planetes&nbsp;&nbsp;<SPAN style="font-weight: normal">(' + str(sHTMLDataPlanets.count("OBJECT ROW : ")) + '/7)</SPAN></H2>'
            sHTML += sHTMLDataPlanets
            sHTML += '</P>' + '\n'
        sHTMLDataMoon = self.getObjectEphemeridesTableForMoonHTML(oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLDataMoon) >0:
            sHTML += '<P class="Category"><H2>&nbsp;La Lune</H2>'
            sHTML += sHTMLDataMoon
            sHTML += '</P>' + '\n'
            sHTMLLunarFeatures = self.getLunarFeaturesEphemeridesTableHTML(oCalendar, oParameters, oEphemeridesData)
            if len(sHTMLLunarFeatures) > 0:
                sHTML += '<P class="Category"><H2>&nbsp;Les Formations Lunaires&nbsp;&nbsp;<SPAN style="font-weight: normal">(' + str(sHTMLLunarFeatures.count("LUNAR FEATURE ROW : ")) + '/' + str(oParameters.getLunarFeatures().getCount()) + ')</SPAN></H2>'
                sHTML += sHTMLLunarFeatures
                sHTML += '</P>' + '\n'
        sHTMLDataDeepSky = self.getObjectEphemeridesTableForDeepSkyHTML(oCalendar, oParameters, oEphemeridesData)
        if len(sHTMLDataDeepSky) > 0:
            sHTML += '<P class="Category"><H2>&nbsp;Le Ciel Profond&nbsp;&nbsp;<SPAN style="font-weight: normal">(' + str(sHTMLDataDeepSky.count("OBJECT ROW : ")) + '/' + str(oParameters.getSkyObjects().getCountDeepSky()) + ')</SPAN></H2>'
            sHTML += sHTMLDataDeepSky
            sHTML += '</P>' + '\n'
        sHTML += '    </BODY>' + "\n"
        sHTML += '</HTML>' + "\n"

        return sHTML
    def getHTMLHeaderComment(self, oCalendar, oParameters):
        return ('<!-- Parameters... Date:'  + oCalendar.getDate() + '  - Place:'  + oParameters.getPlace().getName() + ' - Longitude:'  + str(oParameters.getPlace().getLongitude()) + ' - Latitude:'  + str(oParameters.getPlace().getLatitude()) + '  -->'  )
        

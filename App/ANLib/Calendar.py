#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Calendar
# 
from toolObjectSerializable import toolObjectSerializable
#from toolTrace import toolTrace
import datetime
from MeeusAlgorithmsFormulas import MeeusAlgorithmsFormulas

class Calendar(toolObjectSerializable):
    def __init__(self, sDate, sTime, fLocalTimeDifferenceWithGMT):
        toolObjectSerializable.__init__(self)
        self._date = sDate # date as YYYYMMDD  (Local Time)
        self._time = sTime # Time as HHMMSS    (Local Time)
        self._fLocalTimeDifferenceWithGMT = fLocalTimeDifferenceWithGMT
        self._iYear = int(sDate[0:4])
        self._iMonth = int(sDate[4:6])
        self._iDay = int(sDate[6:8])
        self._iHours = int(sTime[0:2])
        self._iMinutes = int(sTime[2:4])
        self._iSeconds = int(sTime[4:8])
        self._dtLocalDateTime =  datetime.datetime(int(sDate[0:4]),int(sDate[4:6]),int(sDate[6:8]),int(sTime[0:2]),int(sTime[2:4]),int(sTime[4:8]))
        self._dtGMTLocalDateTime =  self._dtLocalDateTime - datetime.timedelta(hours=self._fLocalTimeDifferenceWithGMT)
        self._fLocalDateValue = self.__computeDateValueFromDateAndTime(sDate, sTime)
    def __computeDateValueFromDateAndTime(self, sDate, sTime):
        # Compute the number of days since 01/01/2000 at 00:00 which is the reference date
        # Split date and time 
        #fDateValue = float(367 * self._iYear - 7 * (self._iYear + (self._iMonth + 9) / 12) / 4 + 275 * self._iMonth/9 + self._iDay - 730530)
        #fDateValue = fDateValue + (float(self._iHours) + float(self._iMinutes) / 60.0 + float(self._iSeconds) / 3600.0)/24.0
        #fDateValue = fDateValue # - 0.5
        fDateValue = self.getJulianDate() - MeeusAlgorithmsFormulas.JulianDay_07_01(2000, 1, 1, 0, 0, 0)
        return fDateValue
    def getLocalDate(self): return self._date
    def getGMTDate(self): return self._date
    def getJulianDate(self):
        return MeeusAlgorithmsFormulas.JulianDay_07_01(self._dtGMTLocalDateTime.year, self._dtGMTLocalDateTime.month, self._dtGMTLocalDateTime.day, self._dtGMTLocalDateTime.hour, self._dtGMTLocalDateTime.minute, self._dtGMTLocalDateTime.second)
    def getLocalDateForSlot(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%Y%m%d')
    def getGMTDateForSlot(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtGMTLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%Y%m%d')
    def getFormattedLocalDateForSlot(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%d %b %Y')
    def getFormattedGMTDateForSlot(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtGMTLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%d %b %Y')
    def getTime(self): return self._time
    def getLocalTimeForSlot(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%H%M%S') 
    def getGMTTimeForSlot(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtGMTLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%H%M%S')
    def getLocalTimeForSlotAsHHMM(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%H:%M')  #TODO: compute local time based on DST and area
    def getGMTTimeForSlotAsHHMM(self, iSlot, iNumberOfMinutesPerSlot): return (self._dtGMTLocalDateTime + datetime.timedelta(minutes=(iNumberOfMinutesPerSlot * iSlot))).strftime('%H:%M')
    def getNumberOfDaysSinceRef(self): return self._fDateValue
    def getLocalDateValueForTimeSlot(self, iTimeSlot, iNumberOfMinutesPerSlot):
        # add delta corresponding to timeslot
        fDateValue = self._fLocalDateValue + (float(iNumberOfMinutesPerSlot) / 1440.0 * float(iTimeSlot))
        return fDateValue
    def getGMTDateValueForTimeSlot(self, iTimeSlot, iNumberOfMinutesPerSlot):
        # add delta corresponding to timeslot
        fDateValue = self._fLocalDateValue + (float(iNumberOfMinutesPerSlot) / 1440.0 * float(iTimeSlot)) - (fLocalTimeDifferenceWithGMT / 24.0)
        return fDateValue
    

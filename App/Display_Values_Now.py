#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

# Import libs for ephemerides
from datetime import datetime, timedelta
import ANLib

fNowYear    = int(datetime.now().strftime("%Y"))
fNowMonth   = int(datetime.now().strftime("%m"))
fNowDay     = int(datetime.now().strftime("%d"))
fNowHours   = int(datetime.now().strftime("%H"))
fNowMinutes = int(datetime.now().strftime("%M"))
fNowSeconds = int(datetime.now().strftime("%S"))
ANLib.MeeusAlgorithmsFormulasTests.DisplayValues(fNowYear, fNowMonth, fNowDay, fNowHours, fNowMinutes, fNowSeconds)

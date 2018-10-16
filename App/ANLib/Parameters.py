#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class Parameters
# 
from ParametersJsonGeneric import ParametersJsonGeneric
from ParametersJsonGenericObjects import ParametersJsonGenericObjects
from toolJSON import toolJSON
from Tools import Tools
import time


class Parameters():
    def __init__(self):
        self._ParametersLocalization = None
        self._ParametersLunarFeatures = None
        self._ParametersRendering = None
        self._ParametersRuntime = None
        self._ParametersSkyObjects = None
        self._ParametersPlaces = None
        self.__load()

    def Localization(self): return self._ParametersLocalization
    def LunarFeatures(self): return self._ParametersLunarFeatures
    def Rendering(self): return self._ParametersRendering
    def Runtime(self): return self._ParametersRuntime
    def SkyObjects(self): return self._ParametersSkyObjects
    def Places(self): return self._ParametersPlaces
    
    def __load(self):
        self._ParametersRuntime       = ParametersJsonGeneric("parameters_Runtime.json")
        self._ParametersRendering     = ParametersJsonGeneric("parameters_Rendering.json")
        self._ParametersLocalization  = ParametersJsonGeneric("parameters_Localization.json", self._ParametersRendering.get("RenderingOptions.Language"))
        self._ParametersSkyObjects    = ParametersJsonGenericObjects("parameters_SkyObjects.json")
        self._ParametersLunarFeatures = ParametersJsonGenericObjects("parameters_LunarFeatures.json")
        self._ParametersPlaces        = ParametersJsonGenericObjects('parameters_Places.json')
        
        for iPlace in range (1, self._ParametersPlaces.getCount() +1 ):
            aPlace = self._ParametersPlaces.getObjectByIndex(iPlace)
            #
            # Handle property CurrentLocalTimeDifferenceWithGMT
            #
            fTimeDiff = aPlace.get("LocalTimeDifferenceWithGMT")
            if time.localtime().tm_isdst == 1: fTimeDiff = fTimeDiff + 1.0
            aPlace.set("CurrentLocalTimeDifferenceWithGMT", fTimeDiff, "float")
            #
            # Handle property   getIndexFromAzimutAltitude
            #                   getVisibilityStatus
            #
            dicObjstructedSkyAreas = aPlace.get("ObstructedSkyAreas")
            sObstructedSkyAreasMap = "1"*180*360
            arrObstructedSkyAreasColor = {}
            for i in range(1, len(dicObjstructedSkyAreas) +1):
                aArea = dicObjstructedSkyAreas[str(i)]
                fAz = aArea["Azimut-Min"]
                fAzMax = aArea["Azimut-Max"]
                while (fAz <= fAzMax):
                    fAlt = aArea["Altitude-Min"]
                    fAltMax = aArea["Altitude-Max"]
                    while (fAlt <= fAltMax):
                        iPos = Tools.getIndexFromAzimutAltitude(fAz, fAlt)
                        if (iPos == 0):
                            sObstructedSkyAreasMap = "0" + sObstructedSkyAreasMap[1:]
                        elif (iPos == 64799):
                            sObstructedSkyAreasMap = sObstructedSkyAreasMap[:iPos] + "0"
                        else:
                            sObstructedSkyAreasMap = sObstructedSkyAreasMap[:iPos] + "0" + sObstructedSkyAreasMap[iPos + 1:]
                        # Add color in dictionary with key = index
                        arrObstructedSkyAreasColor[str(iPos)] = eval(aArea["Color"])
                        fAlt = fAlt + 1.0
                    fAz = fAz + 1.0
            aPlace.set("VisibilityStatus", sObstructedSkyAreasMap, "string")
            aPlace.set("ColorForAzimutAltitude", arrObstructedSkyAreasColor, "object")
            #
            # handle getMinMaxAltitudeObstructedForAzimut
            #
            dicMinMaxAltitudeObstructedForAzimut = {}
            for iAzimut in range (0, 360):
                fAzimut = float(iAzimut)
                fMinAltitude = 999.0
                fMaxAltitude = -999.0
                fAzimut360 = (fAzimut + 360.0) % 360.0
                for iAltitude in range (0, 90):
                    fAltitude = float(iAltitude)
                    if sObstructedSkyAreasMap[Tools.getIndexFromAzimutAltitude(fAzimut360, fAltitude)] == "0":
                        if fAltitude > fMaxAltitude: fMaxAltitude = fAltitude
                        if fAltitude < fMinAltitude: fMinAltitude = fAltitude
                if fMinAltitude == 999.0:
                    fMinAltitude = 0
                    fMaxAltitude = 0
                dicMinMaxAltitudeObstructedForAzimut[str(int(fAzimut))] = (fMinAltitude, fMaxAltitude)
            aPlace.set("MinMaxAltitudeObstructedForAzimut", dicMinMaxAltitudeObstructedForAzimut, "object")
        
        self._ParametersRuntime.set("Place" , self._ParametersPlaces.getObjectByID(self._ParametersRuntime.get('Observation.PlaceName')), "object")

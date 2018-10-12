#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersJsonGenericObject
# 

class ParametersJsonGenericObject():
    def __init__(self, dicData):
        self._dicData = dicData

    
    def set(self, sCode, aValue, sType):
        sDic = {}
        sDic["value"] = aValue
        sDic["type"] = sType
        self._dicData[sCode] = sDic
    
    def get(self, sCode): 
        aReturnValue = None
        sType = None
        try:
            aAttribute = self._dicData[sCode]
        except:
            aAttribute = None
            print "   >>>> ERROR >>>>  attribute " + sCode + " not found !!!"
        if not aAttribute is None:
            if isinstance(aAttribute, dict):
                try:
                    sType = aAttribute["type"]
                except:
                    sType = None
                if sType == "tuple":    
                    aReturnValue = eval(aAttribute["value"])
                else:
                    try:
                        aReturnValue = aAttribute["value"]
                    except:
                        aReturnValue = aAttribute
            else:
                aReturnValue = aAttribute
        return aReturnValue

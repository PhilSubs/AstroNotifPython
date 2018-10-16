#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersJsonGenericObject
# 

class ParametersJsonGenericObject():
    def __init__(self, dicData):
        self._dicData = dicData
        self._buffer = {}

    
    def set(self, sCode, aValue, sType):
        sDic = {}
        sDic["value"] = aValue
        sDic["type"] = sType
        self._dicData[sCode] = sDic
    
    def get(self, sCode): 
        if not self._buffer.get(sCode) is None :
            aReturnValue = self._buffer[sCode]
        else:
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
                self._buffer[sCode] = aReturnValue
        return aReturnValue

#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersJsonGeneric
# 
from toolJSON import toolJSON

class ParametersJsonGeneric:
    def __init__(self, sJsonFileName):
        self._jsonFileName = sJsonFileName
        self._dicParameters = toolJSON.getContent(self._jsonFileName)
    
    def set(self, sParameterName, aValue, sType):
        sDic = {}
        sDic["value"] = aValue
        sDic["type"] = sType
        self._dicParameters[sParameterName] = sDic
        
    def get(self, sParameterName, bNotifyMissing = True):
        # Parameter name has following form :  param1.param2.param3...
        # Compute path from parameter name in order to have something like: ["param1"]["param2"]["param3"
        arrPath = sParameterName.split(".")
        sDicPath = ""
        for i in range (0, len(arrPath)):
            sDicPath = sDicPath + '["' + arrPath[i] + '"]'
        try:
            dicParameter = eval("self._dicParameters" + sDicPath)
        except:
            if bNotifyMissing:
                print ""
                print "   >>> ERROR >>> get json parameter '" + sParameterName + "' from  file  '" + self._jsonFileName + "'  FAILED !!"
                print "                 Unknown parameter !!"
                print ""
            raise
        # get the parameter type from the JSON file content
        sParameterType = "unknown"
        try:
            sParameterType = dicParameter["type"].lower()
        except:
            if isinstance(dicParameter, dict):
                sParameterType = "dict"
            else:
                if bNotifyMissing:
                    print ""
                    print "   >>> ERROR >>> get json parameter '" + sParameterName + "' from  file  '" + self._jsonFileName + "'  FAILED !!"
                    print "                 Can't find parameter type !!"
                    print ""
                raise
        #Compute the return value depending on the parameter type
        sReturn = None
        try:
            if sParameterType == "string":
                sReturn = dicParameter["value"]
            elif sParameterType == "int":
                sReturn = dicParameter["value"]
            elif sParameterType == "float":
                sReturn = dicParameter["value"]
            elif sParameterType == "bool":
                sReturn = (dicParameter["value"].lower() == "true")
            elif sParameterType == "tuple":
                sReturn = eval(dicParameter["value"])
            elif sParameterType == "dict":
                sReturn = dicParameter
            elif sParameterType == "object":
                sReturn = dicParameter["value"]
        except:
            if bNotifyMissing:
                print ""
                print "   >>> ERROR >>> get json parameter '" + sParameterName + "' from  file  '" + self._jsonFileName + "'  FAILED !!"
                print "                 Can't find parameter value !!"
                print ""
            raise
        # return the parameter value as string, int, float, tuple, boolean or dict
        return sReturn

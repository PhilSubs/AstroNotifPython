#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
#
# Class ParametersJsonGeneric
# 
from toolJSON import toolJSON

class ParametersJsonGeneric:
    def __init__(self, sJsonFileName, sDefaultPrefix = ""):
        self._jsonFileName = sJsonFileName
        self._dicParameters = toolJSON.getContent(self._jsonFileName)
        self._sDefaultPrefix = sDefaultPrefix  #  Default prefix used for any get
    
    def setDefaultPrefix(self, sDefaultPrefix): self._sDefaultPrefix = sDefaultPrefix
    def getDefaultPrefix(self): return self._sDefaultPrefix 
    
    def set(self, sCode, aValue, sType):
        sDic = {}
        sDic["value"] = aValue
        sDic["type"] = sType
        self._dicParameters[sCode] = sDic
        
    def get(self, sCode, bNotifyMissing = True, bReturnDefaultValue = False):
        # Parameter name has following form :  param1.param2.param3...
        # Compute path from parameter name in order to have something like: ["param1"]["param2"]["param3"
        arrPath = sCode.split(".")
        sDicPath = ""
        for i in range (0, len(arrPath)):
            sDicPath = sDicPath + '["' + arrPath[i] + '"]'
        # Add default prefix if any
        if self._sDefaultPrefix != "": sDicPath = '["' + self._sDefaultPrefix + '"]' + sDicPath
        # Retrieve the parameter, based on the path, as a dict
        dicParameter = None
        try:
            dicParameter = eval("self._dicParameters" + sDicPath)
        except:
            if bNotifyMissing:
                print ""
                print "   >>> ERROR >>> get json parameter '" + sCode + "' from  file  '" + self._jsonFileName + "'  FAILED !!"
                print "                 Unknown parameter !!"
                print ""
                raise
        # get the parameter type from the JSON file content
        sParameterType = "unknown"
        if not dicParameter is None:
            try:
                sParameterType = dicParameter["type"].lower()
            except:
                if isinstance(dicParameter, dict):
                    sParameterType = "dict"
                else:
                    if bNotifyMissing:
                        print ""
                        print "   >>> ERROR >>> get json parameter '" + sCode + "' from  file  '" + self._jsonFileName + "'  FAILED !!"
                        print "                 Can't find parameter type !!"
                        print ""
                    raise
        #Compute the return value depending on the parameter type
        try:
            if sParameterType == "string":
                sReturn = dicParameter["value"]
            elif sParameterType == "int":
                sReturn = dicParameter["value"]
            elif sParameterType == "float":
                sReturn = dicParameter["value"]
            elif sParameterType == "bool":
                sReturn = dicParameter["value"]
            elif sParameterType == "tuple":
                sReturn = eval(dicParameter["value"])
            elif sParameterType == "dict":
                sReturn = dicParameter
            elif sParameterType == "object":
                sReturn = dicParameter["value"]
            else:
                sReturn = None
        except:
            if bNotifyMissing:
                print ""
                print "   >>> ERROR >>> get json parameter '" + sCode + "' from  file  '" + self._jsonFileName + "'  FAILED !!"
                print "                 Can't find parameter value !!"
                print ""
                raise
        # return the parameter value as string, int, float, tuple, boolean or dict
        if sReturn is None and bReturnDefaultValue:
            sReturn = sCode
        return sReturn

    def getWithDefault(self, sCode): return self.get(sCode, bNotifyMissing = False, bReturnDefaultValue = True)

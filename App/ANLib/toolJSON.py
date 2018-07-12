#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

import json
from toolObjectSerializable import toolObjectSerializable
from Tools import Tools

class toolJSON(toolObjectSerializable):
    @staticmethod
    def _parseJSON(obj):
        if isinstance(obj, dict):
            newobj = {}
            for key, value in obj.iteritems():
                key = str(key)
                newobj[key] = toolJSON._parseJSON(value)
        elif isinstance(obj, list):
            newobj = []
            for value in obj:
                newobj.append(toolJSON._parseJSON(value))
        elif isinstance(obj, unicode):
            newobj = str(obj).encode("iso-8859-1" )
        else:
            newobj = obj
        return newobj

    @staticmethod
    def getContent(sFilename):
        # load parameters file
        with open(sFilename, 'r') as fJSONFile:
            dictData = json.load(fJSONFile, parse_float=float, parse_int=int)
            dictData  = toolJSON._parseJSON(dictData)
        return dictData

    @staticmethod
    def saveContent(sFilename, oContent):
        with open(sFilename, "w") as fJSONFile:
            json.dump(oContent, fJSONFile)
    
    
#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

import json
from ANLib import *

class toolSerialization:
    @staticmethod
    def deserializeFromString(sSerializedObjectAsString):
        aTraceObj = toolTrace.toolTrace()
        # Convert string JSON to Dict object
        obj_dict = json.loads(sSerializedObjectAsString)
        # if "__class__" item exists, then the Dict object is the serialization of a custom class
        if "__class__" in obj_dict:
            # create an object 'obj' of type defined by the '__class__' item
            aTraceObj.debugLevel1("[deserializeFromString.1]... contains __class__ = " + obj_dict["__class__"] + " --> deserializing object of type " + obj_dict["__class__"])
            aClass = globals()[obj_dict["__class__"]]
            obj = aClass()
            # process all other items as attributes of the object created
            for sAttr, sValue in obj_dict.iteritems():
                if sAttr != "__class__":
                    aTraceObj.debugLevel1("[deserializeFromString.1.1]...... attr " + sAttr + " of type " + sValue.__class__.__name__)
                    # special case: if the attribute contains a Dict, then it has to be deserialized as well
                    if sValue.__class__.__name__ == "dict":
                        aTraceObj.debugLevel1("[deserializeFromString.1.1.1]...... attr " + sAttr + " of type " + sValue.__class__.__name__ + "==> call toolSerialization.deserialize(json.dumps(sValue))")
                        dicTmpDeserial = toolSerialization.deserializeFromString(json.dumps(sValue))
                        setattr(obj, sAttr, dicTmpDeserial)
                    # if the attribute is not a dict, the the value is affected to the attribute of the class
                    else:
                        aTraceObj.debugLevel1("[deserializeFromString.1.1.2]......... set value of attribute " + sAttr)
                        setattr(obj, sAttr, sValue)
            # return the object 'obj' deserialized
            return obj
        # in case there is not '__class__' atribute in the dict: all the dict items are deserialized before returning the dict objet
        else:
            aTraceObj.debugLevel1("[deserializeFromString.2]... no __class__ item: loop through all items...")
            for sAttr, sValue in obj_dict.iteritems():
                aTraceObj.debugLevel1("[deserializeFromString.2.1]...... item " + sAttr + " of type " + sValue.__class__.__name__)
                if sValue.__class__.__name__ == "dict":
                    aTraceObj.debugLevel1("[deserializeFromString.2.1.1]...... attr " + sAttr + " of type " + sValue.__class__.__name__ + "==> call toolSerialization.deserialize(json.dumps(sValue))")
                    dicTmpDeserial = toolSerialization.deserializeFromString(json.dumps(sValue))
                    obj_dict[sAttr] = dicTmpDeserial
            # return the dict object
            return obj_dict


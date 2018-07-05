#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

import json
#from toolTrace import toolTrace
from pprint import pprint

class toolObjectSerializable:
    def __init__(self):
        pass
#        self._TraceObj = toolTrace()
    def serializeToString(self):
        # Return the object serialized as a Dict and then converted to a JSON string
        return json.dumps(self.serialize())
    def serialize(self):
        # Serialize the object as a dictionary
        dicSerial = {}
        # add '__class__' item in the dict so we know the class of the object serialized as Dict
        dicSerial["__class__"] = self.__class__.__name__
#        self._TraceObj.debugLevel1("[serialize]........ class:" + self.__class__.__name__)
#        self._TraceObj.debugLevel1("[serialize]........... loop on attributes")
        # loop through each attribute of the object
        for attr, value in self.__dict__.iteritems():
#            self._TraceObj.debugLevel1("[serialize].............. Attribute " + self.__class__.__name__ + " attr:" + attr + " type:" + value.__class__.__name__)
            # only process attributes with name beggining with '_'
            if attr[0:1] == "_" and attr != "_TraceObj":
                # if attribute is a Dict, then it has to be serialized as well
                if value.__class__.__name__ == "dict":
#                    self._TraceObj.debugLevel1("[serialize]................. Attribute is dict ==> serialize all items using toolObjectSerializable.serializeDictAttr(value)")
                    dicSerial[attr] = toolObjectSerializable.serializeDictAttr(value)
                # if attribute is not a Dict, but has a method 'serialize', then it is a custom class object and it can be serialized
                elif hasattr(value, 'serialize'):
#                    self._TraceObj.debugLevel1("[serialize]................. Attribute is not dict but have method 'Serialize' ==> call attribute.serialize()")
                    dicSerial[attr] = value.serialize()
                # attribute if not a Dict and not a custom object, it can't be serialized and its value is stored in the Dict
                else:
#                    self._TraceObj.debugLevel1("[serialize]................. Attribute is not dict and does not have method 'Serialize' ==> standard attribute stored with its value")
                    dicSerial[attr] = value
        # return object serialized as a Dict
        return dicSerial
    @staticmethod
    def serializeDictAttr(aDic):
#        aTraceObj = toolTrace()
        # process a Dict to serialize its attributes
        dicTmpSerial = {}
#        aTraceObj.debugLevel1("[serializeDictAttr].................... loop on items")
        for sKey,aObject in aDic.iteritems():
            # if item contains a Dict, then it has to be serialized as well
            if aObject.__class__.__name__ == "dict":
#                aTraceObj.debugLevel1("[serializeDictAttr]....................... items:" + aObject.__class__.__name__ + " is dict ==> serialize all items using toolObjectSerializable.serializeDictAttr(value)")
                dicTmpSerial[sKey] = toolObjectSerializable.serializeDictAttr(aObject)
            # if item is not a Dict, but is an object with a method 'serialize', then it is a custom class object and it can be serialized
            elif hasattr(aObject, 'serialize'):
#                aTraceObj.debugLevel1("[serializeDictAttr]....................... items:" + aObject.__class__.__name__ + " is not dict but have method 'Serialize' ==> call attribute.serialize()")
                dicTmpSerial[sKey] = aObject.serialize()
            # if item is not a Dict and not a custom object, it can't be serialized and its value is stored in the Dict
            else:
                dicTmpSerial[sKey] = aObject
        # return the Dict processed
        return dicTmpSerial

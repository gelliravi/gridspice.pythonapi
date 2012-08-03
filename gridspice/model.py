'''
Created on Jul 11, 2012

@author: jimmy
'''
# Intro To Python:  Modules
# book.py

import config
import requests
import urllib
import json

class SchematicType:
    """
        SchematicType contains three constants which represent the model type: UNKNOWN, TRANSMISSION, DISTRIBUTION
    """
    UNKNOWN = "UNKNOWN" 
    TRANSMISSION = "TRANSMISSION"
    DISTRIBUTION = "DISTRIBUTION"
    
class MapType:
    """
        MapType contains two constants which represent the map type: BLANK, POLITICAL
    """
    BLANK = "BLANK"
    POLITICAL = "POLITICAL"

class Model:
    """
      The GridSpice model contains the network model (transmission, distribution, etc)
    """
    def __init__(self, name, project, schematicType = SchematicType.DISTRIBUTION, mapType = MapType.POLITICAL, empty = 0):
        if (project.id != None and project.id > 0):
            self.id = None
            self.name = name
            self.projectId = project.id    
            self.loaded = 0
            self.APIKey = project.APIKey
            if (empty == 0):
                self.counter = 0
                self.elementDict = []
                self.climate = config.DEFAULT_CLIMATE
                self.schematicType = schematicType
                self.mapType = mapType
                self.loaded = 1
        else:
            raise ValueError("'" + project.name + "'"  + " has not yet been stored.")
    
    def _loadElements(self, key):
        if (key != None):
            payload = {'id':self.id}
            headers = {'APIKey':self.APIKey}
            r = requests.get(config.URL + "multipleelements.xml", params = payload, headers = headers)
            if (r.status_code == requests.codes.ok):
                data = r.text
                if (data != config.INVALID_API_KEY):
                    self.xmldata = data #temporary attribute
                    self.elementDict = []
                    return 1
                else: 
                    raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
        return 0

    def load(self):
	"""
	   fills in the other information to the model object
	"""
        if (self.id != None):
            payload = {'id':self.id}
            headers = {'APIKey':self.APIKey}
            r = requests.get(config.URL + "models/ids", params = payload, headers = headers)
            if (r.status_code == requests.codes.ok):
                data = r.text
                if (data != config.INVALID_API_KEY):
                    jsonModel = json.loads(data);
                    self.counter = int(jsonModel['counter'])
                    self.climate = jsonModel['climate'].encode('ascii')
                    self.schematicType = jsonModel['schematicType'].encode('ascii')
                    self.mapType = jsonModel['mapType'].encode('ascii')
                    self.loaded = self._loadElements(jsonModel['modelDataKey'].encode('ascii'))
                    if (self.loaded == 1):
                        print self.name + " has been loaded."
                else:
                    raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
        else:
            print self.name + " has not yet been stored in the database."
            
            
    def _store(self):
        dictCopy = self.__dict__.copy()
        del dictCopy['APIKey']
        payload = urllib.urlencode(dictCopy)
        headers = {'APIKey':self.APIKey}
        r = requests.post(config.URL + "models/create", data=payload, headers = headers)
        if (r.status_code == requests.codes.ok):
            data = r.text
            if (data != config.INVALID_API_KEY):
                result = int(data)
                if (result > 0):
                    self.id = result
                    print self.name + " has been stored in the database."
                else:
                    print "Error saving. A different version of this project already exists. Has " + self.name + " been loaded?"
            else:
                raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
        else:
            print "Error in the server."    
            
    def _update(self):
        dictCopy = self.__dict__.copy()
        del dictCopy['APIKey']
        payload = urllib.urlencode(dictCopy)
        headers = {'APIKey':self.APIKey}
        r = requests.post(config.URL + "models/update", data=payload, headers = headers)
        if (r.status_code == requests.codes.ok):
            data = r.text
            if (data != config.INVALID_API_KEY):
                result = int(data)
                if (result > 0):
                    self.id = result
                    print self.name + " has been updated."
                else:
                    print "Error updating."
            else:
                raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
        else:
            print "Error in the server."
            
    def save(self):
	"""
	   saves this model
	"""
        if (self.loaded == 1):
            if (self.id is None):
                self._store()
            else:
                self._update()
        else:
            print "Please load " + self.name + " before updating."

    def	delete(self):
	"""
	   deletes this model
	"""
        if (self.id != None):
            headers = {'APIKey':self.APIKey, 'Content-Length':'0'}
            r = requests.post(config.URL + "models/destroy/" + repr(self.id), headers = headers)
            if (r.status_code == requests.codes.ok):
                data = r.text
                if (data != config.INVALID_API_KEY):
                    result = int(data)
                    if (result == 1):
                        self.id = None
                        print self.name + " has been deleted from the database."
                    else:
                        print "Error deleting."
                else:
                    raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
            else:
                print "Error in the server."
        else:
            print self.name + "has not yet been stored in the database"


    def	add (self, element):
	"""
	   Adds the element to the model
	"""
	
    def	remove(self, element):
	"""	
	   Removes the element from the model
	"""
	
    def	copy(self, project):
	"""
	   Returns a copy of this model
    """

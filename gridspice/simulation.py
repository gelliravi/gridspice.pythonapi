# Intro To Python:  Modules
# book.py
import requests
import urllib
import json
import config

class Simulation:

    """
      The GridSpice simulation object contains a project's simulation requests
    """
    def __init__(self, id, project):
        self.id = id
        self.projectId = project.id
        self.APIKey = project.APIKey
        
    def load(self):
        """
            loads the Simulation report
        """
        self.urls = []
        if (self.id != None):
            payload = {'id':self.id}
            headers = {'APIKey':self.APIKey}
            r = requests.get(config.URL + "simulations/ids", params = payload, headers = headers)
            if (r.status_code == requests.codes.ok):
                data = r.text
                if (data != config.INVALID_API_KEY):
                    jsonSimulation = json.loads(data)
                    self.id = int(jsonSimulation['id'])
                    tempUrls = jsonSimulation['fileUrls']
                    for x in tempUrls:
                        self.urls.append(x.encode('ascii'))
                    self.deleted = jsonSimulation['deleted'].encode('ascii')
                else:
                    raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
            print "Simulation " + repr(self.id) + " has been loaded."
        else:
            print "Simulation " + repr(self.id) + " has not yet been stored in the database."



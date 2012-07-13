# Intro To Python:  Modules
# book.py
import config

class Model:
    """
      The GridSpice model contains the network model (transmission, distribution, etc)
    """
    def __init__(self, name, project, empty = 0):
	self.id = None
    self.name = name
    self.loaded = 0
    #TODO print error if project has no id
    
    if (empty == 0):
    	self.projectId = project.id	
        self.mapType = mapType
        self.counter = 0
        self.climate = config.DEFAULT_CLIMATE
        self.schematicType = schematicType
        self.loaded = 1
    

    def load(self):
	"""
	   fills in the other information to the model object
	"""
	
    def save(self):
	"""
	   saves this model
	"""

    def	delete(self):
	"""
	   deletes this model
	"""

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


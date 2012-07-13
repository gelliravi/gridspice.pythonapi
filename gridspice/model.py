# Intro To Python:  Modules
# book.py
import config

class Model:
    """
      The GridSpice model contains the network model (transmission, distribution, etc)
    """
    def __init__(self, name, project, schematicType = config.DEFAULT_SCHEMATIC_TYPE, mapType = config.DEFAULT_MAP_TYPE, empty = 0):
        if (project.id != None and project.id > 0):
            self.id = None
            self.name = name
            self.projectId = project.id    
            self.loaded = 0
            if (empty == 0):
                self.counter = 0
                self.climate = config.DEFAULT_CLIMATE
                self.schematicType = schematicType
                self.mapType = mapType
                self.layoutType = config.DEFAULT_LAYOUT_TYPE
                self.loaded = 1
        else:
            raise ValueError("'" + project.name + "'"  + " has not yet been stored.")


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


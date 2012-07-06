# Intro To Python:  Modules
# book.py

class Model:
    """
      The GridSpice model contains the network model (transmission, distribution, etc)
    """
    def __init__(self, name, project):
	self.name = name;
	self.projectId = project.getId()	

    def load():
	"""
	   fills in the other information to the model object
	"""
	
    def save():
	"""
	   saves this model
	"""

    def	delete():
	"""
	   deletes this model
	"""

    def	add (element):
	"""
	   Adds the element to the model
	"""
	
    def	remove(element):
	"""	
	   Removes the element from the model
	"""
	
    def	copy(project):
	"""
	   Returns a copy of this model
    	"""


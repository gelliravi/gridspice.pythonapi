# Intro To Python:  Modules
# book.py

import account

class Project:

    """
      The GridSpice project object keeps track of the group of models to be simulated, as well as global settings
      which pertain to all models in the simulation.
    """
    def __init__(self, name, account):
	self.name = name
	self.accountId = account.getId()
	
    def getEmptyModels():
	"""	
   	   Gets the models associated with this project (Models need to be loaded.)
	"""

    def load():
	"""
	   fills in the other information to the project object
	"""

    def save():
	"""
	   saves this project
	"""

    def delete():
	"""
	   deletes this project
	"""

    def copy(account):
	"""
	   returns a copy of this project
	"""

    def getId():
	"""
	   returns this project's id
	"""
	return self.id


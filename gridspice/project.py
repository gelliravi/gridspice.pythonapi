# Intro To Python:  Modules
# book.py

import account
import config
import connection
import json
import urllib

class Project:

	"""
		The GridSpice project object keeps track of the group of models to be simulated, as well as global settings
		which pertain to all models in the simulation.
	"""
	def __init__(self, name, account):
		self.name = name
		self.id = None
		if (account.__class__.__name__ != 'Account'):
			raise ValueError("Invalid account inputted.")
		self.accountId = account.id
		self.emailAddress = account.email
		self.startDateTime = config.DEFAULT_DATE
		self.endDateTime = config.DEFAULT_DATE
		self.transmissionId = "-1"
		self.climate = config.DEFAULT_CLIMATE
		self.timeZone = config.DEFAULT_TIMEZONE	
		self.modules = { }
		for x in config.DEFAULT_MODULE_NAMES:
			self.modules[x] = ""

	def getEmptyModels(self):
		"""	
		Gets the models associated with this project (Models need to be loaded.)
		"""

	def load(self):
		"""
		fills in the other information to the project object
		"""
		conn = connection.create()
		conn.request("GET", "/projects.json" + "?" + "id=" + repr(self.id))
		res = conn.getresponse()
		emptyProjects = []
		if (res.status == 200 and res.reason == "OK"):
			data = res.read()
			jsonProj = json.loads(data)
			self.email = jsonProj['email']
			self.timeZone = jsonProj['timeZone']
			self.startDateTime = jsonProj['startDateTime']
			self.endDateTime = jsonProj['endDateTime']
			print "Project " + self.name + " has been loaded."

	def _store(self):
		conn = connection.create()
		params = urllib.urlencode(self.__dict__)
		headers = {"Content-Type":"application/x-www-form-urlencoded", "Accept":"text/json"}
		conn.request("POST", "/projects.json", params, headers)
		res = conn.getresponse()
		if (res.status == 200 and res.reason == "OK"):
			data = res.read()
			result = int(data)
			if (result == 1):
				print self.name + " has been stored."
			else:
				print "Error saving. A different version of this project already exists. Has " + self.name + " been loaded?"
		else:
			print "Error in the server."	
	def _update(self):
		
		print self.name + " has been updated."

	def save(self):
		"""
			saves this project
		"""
		if (self.id is None):
			self._store()
		else:
			self._update()

	def delete(self):
		"""
		deletes this project
		"""

	def copy(self, account):
		"""
		returns a copy of this project
		"""

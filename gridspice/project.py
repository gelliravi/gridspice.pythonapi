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
	def __init__(self, name, account, empty = 0):
		self.name = name
		self.id = None
		if (account.__class__.__name__ != 'Account'):
			raise ValueError("Invalid account inputted.")
		self.accountId = account.id
		self.emailAddress = account.email
		self.loaded = 0
		if (empty == 0):
			self.startDateTime = config.DEFAULT_DATE
			self.endDateTime = config.DEFAULT_DATE
			self.transmissionId = "-1"
			self.climate = config.DEFAULT_CLIMATE
			self.timeZone = config.DEFAULT_TIMEZONE	
			self.loaded = 1
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
		conn.request("GET", "/projects/ids" + "?" + "id=" + repr(self.id))
		res = conn.getresponse()
		emptyProjects = []
		if (res.status == 200 and res.reason == "OK"):
			data = res.read()
			jsonProj = json.loads(data)
			self.loaded = 1
			self.email = jsonProj['email'].encode('ascii')
			self.timeZone = jsonProj['timeZone'].encode('ascii')
			self.startDateTime = jsonProj['startDateTime'].encode('ascii')
			self.endDateTime = jsonProj['endDateTime'].encode('ascii')
			self.modules = {}
			tempModules = jsonProj['modules'];
			for key in tempModules:
				self.modules[key.encode('ascii')] = tempModules[key].encode('ascii')
			print "Project " + self.name + " has been loaded."

	def _store(self):
		conn = connection.create()
		params = urllib.urlencode(self.__dict__)
		headers = {"Content-Type":"application/x-www-form-urlencoded", "Accept":"text/json"}
		conn.request("POST", "/projects/create", params, headers)
		res = conn.getresponse()
		if (res.status == 200 and res.reason == "OK"):
			data = res.read()
			result = int(data)
			if (result > 0):
				self.id = result
				print self.name + " has been stored in the database."
			else:
				print "Error saving. A different version of this project already exists. Has " + self.name + " been loaded?"
		else:
			print "Error in the server."	
			
	def _update(self):
		if (self.loaded == 1):
			conn = connection.create()
			params = urllib.urlencode(self.__dict__)
			headers = {"Content-Type":"application/x-www-form-urlencoded", "Accept":"text/json"}
			conn.request("POST", "/projects/update", params, headers)
			res = conn.getresponse()
			if (res.status == 200 and res.reason == "OK"):
				data = res.read()
				result = int(data)
				if (result > 0):
					self.id = result
					print self.name + " has been updated."
				else:
					print "Error updating."
			else:
				print "Error in the server."
		else:
			print "Please load " + self.name + " before updating."

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
		if (self.id != None):
			conn = connection.create()
			params = urllib.urlencode({'id':repr(self.id)})
			headers = {"Content-Type":"application/x-www-form-urlencoded", "Accept":"text/json"}
			conn.request("POST", "/projects/destroy/" + repr(self.id), params, headers)
			res = conn.getresponse()
			if (res.status == 200 and res.reason == "OK"):
				data = res.read()
				result = int(data)
				if (result == 1):
					self.id = None
					print self.name + " has been deleted from the database."
				else:
					print "Error deleting."
			else:
				print "Error in the server."
		else:
			print self.name + "has not yet been stored in the database"
			
	def copy(self, account):
		"""
		returns a copy of this project
		"""

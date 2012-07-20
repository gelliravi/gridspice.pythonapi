# Intro To Python:  Modules
# book.py

import account
import config
import json
import urllib
import requests
import model
import simulation

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
		self.APIKey = account.APIKey
		self.emailAddress = account.email
		self.loaded = 0
		if (empty == 0):
			self.startDateTime = config.DEFAULT_DATE
			self.endDateTime = config.DEFAULT_DATE
			self.transmissionId = "-1"
			#self.timeZone = config.DEFAULT_TIMEZONE	
			self.loaded = 1
			self.modules = { }
			for x in config.DEFAULT_MODULE_NAMES:
				self.modules[x] = ""

	def getModels(self):
		"""	
		Gets the models associated with this project (Models need to be loaded.)
		"""
		emptyModels = []
		outputString = ""
		if (self.id != None):
			payload = {'id':self.id}
			headers = {'APIKey':self.APIKey}
			r = requests.get(config.URL + "multiplemodels.json", params = payload, headers = headers)
			count = 0
			if (r.status_code == requests.codes.ok):
				data = r.text
				if (data != config.INVALID_API_KEY):
					jsonList = json.loads(data)
					for x in jsonList:
						mod = model.Model(x['name'].encode('ascii'), self, empty = 1)
						mod.id = int(x['id'])
						emptyModels.append(mod)
						outputString += "(" + repr(count) + ") " + mod.name + "  "
						count = count + 1
				else:
					raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
		else:
			print "This project has not yet been stored."
		
		print outputString
		return emptyModels
		

	def load(self):
		"""
		fills in the other information to the project object
		"""
		if (self.id != None):
			payload = {'id':self.id}
			headers = {'APIKey':self.APIKey}
			r = requests.get(config.URL + "projects/ids", params = payload, headers = headers)
			if (r.status_code == requests.codes.ok):
				data = r.text
				if (data != config.INVALID_API_KEY):
					jsonProj = json.loads(data)
					self.loaded = 1
					self.email = jsonProj['email'].encode('ascii')
					#self.timeZone = jsonProj['timeZone'].encode('ascii')
					self.startDateTime = jsonProj['startDateTime'].encode('ascii')
					self.endDateTime = jsonProj['endDateTime'].encode('ascii')
					self.modules = {}
					tempModules = jsonProj['modules'];
					for key in tempModules:
						self.modules[key.encode('ascii')] = tempModules[key].encode('ascii')
					print "Project " + self.name + " has been loaded."
				else:
					raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
		else:
			print self.name + " has not yet been stored in the database."
	
	def _store(self):
		dictCopy = self.__dict__.copy()
		del dictCopy['APIKey']
		payload = urllib.urlencode(dictCopy)
		headers = {'APIKey':self.APIKey}
		r = requests.post(config.URL + "projects/create", data=payload, headers = headers)
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
		headers = {'APIKey': self.APIKey}
		r = requests.post(config.URL + "projects/update", data=payload, headers = headers)
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
			saves this project
		"""
		if (self.loaded == 1):
			if (self.id is None):
				self._store()
			else:
				self._update()
		else:
			print "Please load " + self.name + " before updating."

	def delete(self):
		"""
			deletes this project
		"""
		if (self.id != None):
			headers = {'APIKey': self.APIKey, 'Content-Length':'0'}
			r = requests.post(config.URL + "projects/destroy/" + repr(self.id), headers = headers)
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
			
	def copy(self, account):
		"""
			returns a copy of this project
		"""
	
	def runSimulation(self):
		"""
			runs the simulator on this project
		"""

	def getPastSimulations(self):
		"""
			returns the results of the simulation in the form of Simulation objects
		"""
		simulationResults = []
		if (self.id != None):
			headers = {'APIKey': self.APIKey}
			payload = {'id': self.id}
			r = requests.get(config.URL + "multiplesimulations.json", params = payload, headers = headers)
			if (r.status_code == requests.codes.ok):
				data = r.text
				if (data != config.INVALID_API_KEY):
					simulationJSONList = json.loads(data)
					for x in simulationJSONList:
						simulationResults.append(simulation.Simulation(x['id'], self.id))
				else:
					raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")
			else:
				print "Error in the server."
		return simulationResults
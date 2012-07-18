# Intro To Python:  Modules
# book.py

import config
import project
import json
import requests
import webbrowser

class Account:
	"""
		The GridSpice account object contains the credentials for communication with the model server
	"""
	def __init__(self, APIKey): 
			headers = {'APIKey':APIKey}
			r = requests.get(config.URL + "users/login.json", headers = headers)
			if (r.status_code == requests.codes.ok):
				data = r.text
				if (data.strip() != "-1"):
					accObject = json.loads(data);
					self.id = int(accObject['id'])
					self.email = accObject['email']
					self.APIKey = APIKey
					print "Welcome " + self.email + "!"
				else:   
					raise ValueError("'" + APIKey + "'"  + " is not a valid API key.")

	def getProjects(self):
		"""
			Gets the projects associated with this account (Projects need to be loaded)
		"""
		payload = {'email':self.email}
		headers = {'APIKey':self.APIKey}
		r = requests.get(config.URL + "multipleprojects.json", params = payload, headers = headers)
		emptyProjects = []
		outputString = ""
		count = 0
		if (r.status_code == requests.codes.ok):
			data = r.text
			if (data != config.INVALID_API_KEY):
				jsonList = json.loads(data)
				for x in jsonList:
					proj = project.Project(x['name'].encode('ascii'), self, empty = 1)
					proj.id = int(x['id'])
					emptyProjects.append(proj)
					outputString += "(" + repr(count) + ") " + x['name'] + "  "
					count = count + 1
			else:
				outputString = config.INVALID_API_KEY
		print outputString
		return emptyProjects

	def logout(self):
		"""
			Logs out the current user
		"""
		return

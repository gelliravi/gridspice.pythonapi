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
	def __init__(self, apiKEY): 
			payload = {'apiKEY':apiKEY}
			r = requests.get(config.URL + "users/login.json", params = payload)
			if (r.status_code == requests.codes.ok):
				data = r.text
				if (data != "-1"):
					accObject = json.loads(data);
					self.id = accObject['id']
					self.email = accObject['email']
					self.APIKey = apiKey
					print "Welcome " + email + "!"
				else:   
					raise ValueError("'" + email + "'"  + " is not a valid email address.")

	def getProjects(self):
		"""
			Gets the projects associated with this account (Projects need to be loaded)
		"""
		payload = {'email':self.email, 'APIKey':self.APIKey}
		r = requests.get(config.URL + "multipleprojects.json", params = payload)
		emptyProjects = []
		outputString = ""
		count = 0
		if (r.status_code == requests.codes.ok):
			data = r.text
			jsonList = json.loads(data)
			for x in jsonList:
				proj = project.Project(x['name'].encode('ascii'), self, empty = 1)
				proj.id = int(x['id'])
				emptyProjects.append(proj)
				outputString += "(" + repr(count) + ") " + x['name'] + "  "
				count = count + 1
		print outputString
		return emptyProjects

	def logout(self):
		"""
			Logs out the current user
		"""
		return

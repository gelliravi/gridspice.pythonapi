# Intro To Python:  Modules
# book.py

import config
import connection
import project
import json

class Account:
	"""
		The GridSpice account object contains the credentials for communication with the model server
	"""
	def __init__(self, email = "null"):
		if (email != "null") :
			conn = connection.create()
			conn.request("GET", "/users/login.json"
							+ "?" + "email=" + email)
			res = conn.getresponse()
			if (res.status == 200 and res.reason == "OK"):
				data = res.read()
				id = int(data)
				if (id > 0):
					self.id = id
					self.email = email.strip()
					print "Welcome " + email + "!"
				else:   
					conn.close()
					raise ValueError("'" + email + "'"  + " is not a valid email address.")

	def getProjects(self):
		"""
			Gets the projects associated with this account (Projects need to be loaded)
		"""
		conn = connection.create()
		conn.request("GET", "/multipleprojects.json" + "?" + "email=" + self.email)
		res = conn.getresponse()
		emptyProjects = []
		outputString = ""
		count = 0
		if (res.status == 200 and res.reason == "OK"):
			data = res.read()
			jsonList = json.loads(data)
			for x in jsonList:
				proj = project.Project(x['name'], self, empty = 1)
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

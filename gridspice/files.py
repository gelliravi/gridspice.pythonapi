__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

class File:
	def __init__(self, name, project, empty=0):
		self.name = name
		self.id = None
		if (project.__class__.__name__ != 'Project'):
			raise ValueError("Invalid project inputted.")
		self.projectId = project.id
		self.APIKey = project.APIKey
		self.content = None
		self.loaded = 0
		if (empty == 0):
			self.loaded = 1

	def load(self):
		if (self.id != None):
			payload = {'id':self.id}
			headers = {'APIKey':self.APIKey}
			r = requests.get(config.URL + "files/ids", params = payload, headers = headers)
			if (r.status_code == requests.codes.ok):
				data = r.text
				if (data != config.INVALID_API_KEY):
					self.content = data
					self.loaded = 1
					print self.name + " has been loaded."
				else:
					raise ValueError("'" + self.APIKey + "'" + " is not a valid API key.")
		else:
			print self.name + " has not yet been stored in the database."

	def import(self, filepath):
		with (filepath) open as fileImport:
			self.content = fileImport.read()

	# TODO: Use multiform post
	def _store(self):
		pass

	# TODO: Use multiform post
	def _update(self):
		pass

	def save(self):
		if (self.loaded == 1):
			if (self.id is None):
				self._store()
			else:
				self._update()
		else:
			print "Please load " + self.name + " before updating."

	def delete(self):
		if (self.id != None):
			headers = {'APIKey':self.APIKey, 'Content-Length':'0'}
			r = requests.post(config.URL + "files/destroy/" + repr(self.id), headers = headers)
			if (r.status_code == requests.codes.ok):
				data = r.text
			if (data != config.INVALID_API_KEY):
				if (data != "null"):
					self.id = None
					print self.nam + " has been deleted from the database."
				else:
					print "Error deleting."
			else:
					raise ValueError("'" + self.APIKey + "'" + " is not a valid API key.")
		else:
			print self.name + "has not yet been stored int eh database."

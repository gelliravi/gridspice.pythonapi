__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

from pyparsing import *
import glm_grammer

class Parser:

	@classmethod
	def generateObjects(self, filepath):
		objects = []
		with open(self.filepath) as glm_file:
			pass
		return objects

	@classmethod
	def generateGLM(self, objects, filepath):
		pass

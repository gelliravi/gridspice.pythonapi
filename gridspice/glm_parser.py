__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

from pyparsing import *
import glm_grammar

class Parser:

	@staticmethod
	def parseGLM(filepath):
		objects = []
		with open(filepath) as glm_file:
			content = glm_file.read()
			objects = glm_grammar.glm_file.parseString(content)
		return objects

	@staticmethod
	def generateGLM(objects, filepath):
		pass

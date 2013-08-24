__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

from pyparsing import *

MODULE = Literal('module')
OBJECT = Literal('object')
CLOCK = Literal('clock')
COMMENT_START = Literal('//')
SEMI_COLON = Literal(';')
COLON = Literal(':')
NEW_LINE = Literal('\n')
OPEN_BRACKET = Literal('{')
CLOSE_BRACKET = Literal('}')
POUND = Literal('#')

word = Word(alphas + "'.")
number = Word(nums)
unit = word
comment = COMMENT_START + SkipTo(NEW_LINE)
value = oneOf([word, number]) + Optional(unit)
property_ = attribute + value + SEMI_COLON  
properties = OneOrMore(oneOf([property_, object_block]))
properties_block = OPEN_BRACKET + properties + CLOSE_BRACKET
module_block = MODULE + word + Optional(properties_block) + SEMI_COLON
object_block = OBJECT + word + COLON + number + properties
clock_block = CLOCK + properties
macro = POUND + SkipTo(NEW_LINE, include=True) 
glm_file = OneOrMore(oneOf([comment, module_block, object_block, clock_block, macro])



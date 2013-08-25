__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

from pyparsing import *

# Lexemes
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
APOSTROPHE = Literal("'")
DASH = Literal('-')
COLON = Literal(':')
PLUS = Literal('+')

word = Word(alphas)
number = Word(nums)

# Clock properties
date = Combine(Word(nums, exact=4) + DASH + Word(nums, exact=2) + DASH + Word(nums, exact=2)).setResultsName('date') 
time = Combine(Word(nums, max=2) + COLON + Word(nums, exact=2) + COLON + Word(nums, exact=2)).setResultsName('time')
timestamp = Group(APOSTROPHE + date + time + APOSTROPHE).setResultsName('timestamp')
timezone = Combine(word + PLUS + number + word).setResultsName('timezone') 

identifier = Group(number).setResultsName('identifier')
unit = Group(word).setResultsName('unit')
name = Group(Word(alphas+nums+'-_')).setResultsName('name')
attribute = Group(name).setResultsName('attribute')
comment = Group(COMMENT_START + SkipTo(NEW_LINE)).setResultsName('comment')
value = Group((name + Optional(unit)) ^ timestamp ^ timezone).setResultsName('value')

# Property block
property_ = Group(attribute + value + SEMI_COLON).setResultsName('property')  
properties = Group(OneOrMore(property_)).setResultsName('properties') # Currently no support for nested objects
properties_block = Group(OPEN_BRACKET + properties + CLOSE_BRACKET).setResultsName('properties_block')

# File Blocks
module_block = Group(MODULE + name + Optional(properties_block) + SEMI_COLON).setResultsName('module_block')
object_block = Group(OBJECT + name + Optional(COLON + identifier) + properties_block).setResultsName('object_block')
clock_block = Group(CLOCK + properties_block).setResultsName('clock_block')
macro = Group(POUND + SkipTo(NEW_LINE)).setResultsName('macro')
glm_file = Group(ZeroOrMore(module_block ^ object_block ^ clock_block ^ macro)) + stringEnd

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
date = Group(Word(nums, exact=4) + DASH + Word(nums, exact=2) + DASH + Word(nums, exact=2)) 
time = Group(Word(nums, max=2) + COLON + Word(nums, exact=2) + COLON + Word(nums, exact=2))
timestamp = Group(APOSTROPHE + date + time + APOSTROPHE)
timezone = Group(word + PLUS + number + word) 

identifier = Group(number)
unit = Group(word)
name = Group(Word(alphas+nums+'-_'))
attribute = Group(name)
comment = Group(COMMENT_START + SkipTo(NEW_LINE))
value = Group((name + Optional(unit)) ^ timestamp ^ timezone)

# Property block
property_ = Group(attribute + value + SEMI_COLON)  
properties = Group(OneOrMore(property_)) # Currently no support for nested objects
properties_block = Group(OPEN_BRACKET + properties + CLOSE_BRACKET)

# File Blocks
module_block = Group(MODULE + name + properties_block + SEMI_COLON)
object_block = Group(OBJECT + name + Optional(COLON + identifier) + properties_block)
clock_block = Group(CLOCK + properties_block)
macro = Group(POUND + SkipTo(NEW_LINE))
glm_file = Group(OneOrMore(comment | module_block | object_block | clock_block | macro))

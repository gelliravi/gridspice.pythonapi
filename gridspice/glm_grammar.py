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
RECORDER = Literal('recorder')
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
date = Combine(Word(nums, exact=4) + DASH + Word(nums, exact=2) + DASH + Word(nums, exact=2))('date') 
time = Combine(Word(nums, max=2) + COLON + Word(nums, exact=2) + COLON + Word(nums, exact=2))('time')
timestamp = Group(APOSTROPHE + date + time + APOSTROPHE)('timestamp')
timezone = Combine(word + PLUS + number + word)('timezone') 

identifier = number('identifier')
unit = word('unit')
name = Word(alphas+nums+'-_*(,.):+/,"')('name')
attribute = name('attribute')
comment = Group(COMMENT_START + SkipTo(NEW_LINE))('comment')
value = (Group(name('value_name') + Optional(unit)) ^ timestamp ^ timezone)('value')
object_type = Word(alphas+'_')('type')
identity = (COLON + identifier)

# Property block
property_ = Group(attribute + value + SEMI_COLON).setResultsName('properties') #List  
properties = Forward()

# File Blocks
module_block = Group(MODULE + name('module_name') + Optional(properties) + SEMI_COLON).setResultsName('modules') #List
object_block = Group(OBJECT + object_type + Optional(identity) + properties).setResultsName('objects') #List
recorder_block = Group(OBJECT + RECORDER + Optional(identity) + properties + SEMI_COLON).setResultsName('recorders') #List
clock_block = Group(CLOCK + properties).setResultsName('clock')
macro = Group(POUND + SkipTo(NEW_LINE)('macro_content')).setResultsName('macros') #List
glm_file = ZeroOrMore(module_block ^ object_block ^ clock_block ^ macro ^ recorder_block) + stringEnd

# Initialization
properties << (OPEN_BRACKET + OneOrMore(property_ | object_block) + CLOSE_BRACKET)
glm_file.ignore(comment)


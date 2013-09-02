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
date = Combine(Word(nums, exact=4) + DASH + Word(nums, exact=2) + DASH + Word(nums, exact=2)).setResultsName('date') 
time = Combine(Word(nums, max=2) + COLON + Word(nums, exact=2) + COLON + Word(nums, exact=2)).setResultsName('time')
timestamp = Group((APOSTROPHE + date + time + APOSTROPHE).setParseAction(lambda s: s[1:-1])).setResultsName('timestamp')
timezone = Combine(word + PLUS + number + word).setResultsName('timezone') 

identifier = number.setResultsName('identifier')
unit = word.setResultsName('unit')
name = Word(alphas+nums+'-_*(,.):+/,"').setResultsName('name')
attribute = name.setResultsName('attribute')
comment = Group(COMMENT_START + SkipTo(NEW_LINE)).setResultsName('comment')
value = (Group(name + Optional(unit)) ^ timestamp ^ timezone).setResultsName('value')
object_type = Word(alphas+'_').setResultsName('type')
identity = (COLON + identifier).setParseAction(lambda s: s[1:])

# Property block
property_ = (attribute + value + SEMI_COLON).setParseAction(lambda s: s[:-1]).setResultsName('properties', listAllMatches=True)  
properties = Forward()

# File Blocks
module_block = Group((MODULE + name + Optional(properties) + SEMI_COLON).setParseAction(lambda s,l,t: t[1:-1])).setResultsName('modules', listAllMatches=True)
object_block = Group((OBJECT + object_type + Optional(identity) + properties).setParseAction(lambda s,l,t: t[1:])).setResultsName('objects', listAllMatches=True)
recorder_block = Group((OBJECT + RECORDER + Optional(identity) + properties + SEMI_COLON).setParseAction(lambda s,l,t: t[1:-1])).setResultsName('recorders', listAllMatches=True)
clock_block = Group((CLOCK + properties).setParseAction(lambda s,l,t: t[1:])).setResultsName('clock')
macro = Group((POUND + SkipTo(NEW_LINE)).setParseAction(lambda s: s[1:])).setResultsName('macros', listAllMatches=True)
glm_file = ZeroOrMore(module_block ^ object_block ^ clock_block ^ macro ^ recorder_block) + stringEnd

# Initialization
properties << (OPEN_BRACKET + OneOrMore(property_ | object_block) + CLOSE_BRACKET).setParseAction(lambda s: s[1:-1])
glm_file.ignore(comment)


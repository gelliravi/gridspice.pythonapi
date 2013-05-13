#!/usr/bin/python 

import os;

def processfile(file_path, conversion_rules):
	with open(file_path) as file:
		content = file.readlines();
		for line in content:
			if line.startswith('class '):
				header, sep, tail = line.partition('(')
				head, sep, type = header.partition(' ')
				location = file_path[:-3] + '/' + type;
				location = location.replace('/', '.');
				conversion_rules.write('        ' + "'" + type + "': " + "'" + location + "',\n");

powerflow_directory = 'element/powerflow';
wholesale_directory = 'element/wholesale';

preface = '__author__ = "Jimmy Du and Kyle Anderson" \n\
__copyright__ = "Copyright 2013, The GridSpice Project" \n\
__license__ = "BSD" \n\
__version__ = "1.0" \n\
__maintainer__ = ["Kyle Anderson", "Jimmy Du"] \n\
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"] \n\
__status__ = "Development" \n\
\n\
def get_class_path(type): \n\
    return { \n'

end = '    }.get(type, None) \n'

with open('conversion.py', 'w') as conversion_rules:

	conversion_rules.write(preface);

	for filename in os.listdir(powerflow_directory):
		if filename.endswith(".py"):
			processfile(powerflow_directory + '/' + filename, conversion_rules);

	for filename in os.listdir(wholesale_directory):
		if filename.endswith(".py"):
			processfile(wholesale_directory + '/' + filename, conversion_rules);

	conversion_rules.write(end);

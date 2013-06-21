#!/usr/bin/python

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

import sys
import element
import conversion

class TextBlock:
    def __init__(self, blob, lineno):
        self.string = blob[lineno];
        self.lineno = lineno + 1;
        numlines = len(blob);
        brackets = 0;		
        if ('{' in self.string):
            brackets += 1; 
        while ((self.lineno < numlines) and (brackets > 0)): 
            currline = blob[self.lineno]; 
            if ('}' in currline): 
                brackets -= 1; 
            if ('{' in currline): 
                brackets += 1;
            self.string += currline;
            self.lineno += 1; 

class GlmFile:
	def __init__(self, file_name):
		with open(file_name) as file:
			self.content = file.readlines();
	'''
		# File Properties
		linenum = 0;
		numlines = len(self.content);
		self.file_path = file_name;
		self.clock = ''; 
		self.modules = []; 
		self.objects = []; 

		while(linenum < numlines):
			line = self.content[linenum];
			brackets = 0;

			# Save clock block
			if (line.startswith('clock')):
				block = TextBlock(self.content, linenum);
				self.clock = block.string;
				linenum = block.lineno;
			# Save module blocks
			elif (line.startswith('module')):
				block = TextBlock(self.content, linenum);
				self.modules.append(block.string);
				linenum = block.lineno;
			# Save object blocks
			elif (line.startswith('object')):
				block = TextBlock(self.content, linenum);
				obj = self._parseElem(block.string);
				if (obj != None):
					self.objects.append(obj);
				linenum = block.lineno;
			else:
				linenum += 1;
	'''
	def _parseElem(self, object_text):
		object_block = object_text.split('\n');
		header = object_block[0];
		if 'recorder' in header:
			elem_type = 'recorder';
			elem_id = None;
		else:
			header_info = header.split()[1].split(':');
			elem_type = header_info[0];
			elem_id = header_info[1];
		attributes = self._constructAttributes(object_block, elem_id);
		return self._constructElem(elem_type, attributes);
		

	def _constructAttributes(self, object_block, elem_id):
		num_lines = len(object_block);
		attributes = {};
		attributes['id'] = elem_id;
		for i in range(1, num_lines - 2):
			feature = object_block[i].replace(';', '')
			if ('//' not in feature):
				feature = feature.split();
				key = feature[0];
				value = feature[1];
				attributes[key] = value;
		return attributes;

	def _constructElem(self, elem_type, attributes):
		full_type = conversion.get_class_path(elem_type);
		if (full_type != None):
			full_type = eval(conversion.get_class_path(elem_type));
			elem = full_type();
			elem.__dict__.update(attributes);
			return elem;	
		return None;

	def _write_object(self, obj, glm_file):
		attributes = obj.__dict__;
		elem_type = obj.__class__.__name__;
		header = 'object ' + elem_type + ':' + obj.id + ' {\n';
		glm_file.write(header);
		for key, value in attributes.iteritems():
			if (value != None and key != 'id'):
				glm_file.write('\t' + key + ' ' + value + ';\n');
		glm_file.write('}\n');
		glm_file.write('\n');

	def _write(self, glm_file):
		glm_file.write(self.clock + '\n');
		for mod in self.modules:
			glm_file.write(mod + '\n');
		for obj in self.objects:
			self._write_object(obj, glm_file);

	def store(self, file_path = None):
		if (file_path == None):
			with open(self.file_path, 'w') as glm_file:
				self._write(glm_file);
		else:
			with open(file_path, 'w') as glm_file:
				self._write(glm_file);
			

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

import datetime
import copy

level_to_unit = {
	0: 'minute',
	1: 'hour',
	2: 'day',
	3: 'month',
}

unit_to_level = {
	'minute': 0,
	'hour': 1,
	'day': 2,
	'month': 3,
}

# Does not take into account leap years/ months where there are less than 31 days
unit_upperbound = {
	'minute': 59,
	'hour': 23,
	'day': 31,
	'month': 12,
}

unit_lowerbound = {
	'minute': 0,
	'hour': 0,
	'day': 1,
	'month': 1,
}

class ScheduleEntry:
	def __init__(self, minute, hour, day, month, weekday, value):
		self.minute = minute
		self.hour = hour
		self.day = day
		self.month = month
		self.weekday = weekday
		self.value = value

	def toString(self):
		return self.minute + ' ' + self.hour + ' ' + self.day + ' ' + \
						self.month + ' ' + self.weekday + ' ' + self.value

class Schedule:
	def __init__(self, name):
		self.scheduleEntries = []
		self.name = name

	# Iterates backward from the highest level (month) 
	def _findHighestDiffLevel(self, startEntry, endEntry):
		if (endEntry.month > startEntry.month):
			return unit_to_level['month']
		elif (endEntry.day > startEntry.day):
			return unit_to_level['day']
		elif (endEntry.hour > startEntry.hour):
			return unit_to_level['hour']
		elif (endEntry.minute > startEntry.minute):
			return unit_to_level['minute']
		else:
			return None

	# Edits Start Entry based on level
	def _addEditedStartEntry(self, startEntry, level):
		unit = level_to_unit[level]
		orig_val = startEntry.__dict__[unit]
		if (int(orig_val) == unit_upperbound[unit]):
			new_val = orig_val
		else:
			new_val = repr(int(orig_val) + 1) + '-' + repr(unit_upperbound[unit])
		newEntry = copy.deepcopy(startEntry)
		newEntry.__dict__[unit] = new_val
		for i in range(0, level):
			lower_unit = level_to_unit[i]
			newEntry.__dict__[lower_unit] = '*'
		self.scheduleEntries.append(newEntry)

	# Edits Start Entry based on level
	def _addEditedEndEntry(self, endEntry, level):
		unit = level_to_unit[level]
		orig_val = endEntry.__dict__[unit]
		if (int(orig_val) == unit_lowerbound[unit]):
			new_val = orig_val
		else:
			new_val = repr(unit_lowerbound[unit]) + '-' + orig_val 
		newEntry = copy.deepcopy(endEntry)
		newEntry.__dict__[unit] = new_val
		for i in range(0, level):
			lower_unit = level_to_unit[i]
			newEntry.__dict__[lower_unit] = '*' 
		self.scheduleEntries.append(newEntry)

	# Goes from lower units to higher units, editing to match cron format, and adds entry to schedule
	def _populateEntries(self, startEntry, endEntry, level_limit):
		# Upper entries
		for i in range(0, level_limit):
			self._addEditedStartEntry(startEntry, i)

		# Middle entry
		unit = level_to_unit[level_limit]
		startVal = startEntry.__dict__[unit]
		endVal = endEntry.__dict__[unit]
		if (startVal > endVal - 1):
			levelVal = startVal + '-' + repr(endVal - 1)
			middleEntry = copy.deepcopy(startEntry)
			middleEntry.__dict__[unit] = levelVal
			for i in range(0, level_limit):
				lower_unit = level_to_unit[i]
				middleEntry.__dict__[lower_unit] = '*'
			self.scheduleEntries.append(middleEntry)

		# Bottom entries
		for i in range(level_limit - 1, -1, -1):
			self._addEditedEndEntry(endEntry, i)

	# Adds schedule entrie(s) to schedule by filling the gap between starttime and endtime
	def addEntries(self, starttime, endtime, value):
		startEntry = ScheduleEntry(repr(int(starttime.minute)), repr(int(starttime.hour)), \
						repr(int(starttime.day)), repr(int(starttime.month)), '*', repr(int(value)))
		endEntry = ScheduleEntry(repr(int(endtime.minute)), repr(int(endtime.hour)), \
							repr(int(endtime.day)), repr(int(endtime.month)), '*', repr(int(value)))
		level = self._findHighestDiffLevel(startEntry, endEntry)  
		if (level != None):
			self._populateEntries(startEntry, endEntry, level)
		else:
			raise ValueError('End time is not later than start time.')

	def _parseCronToScheduleEntry(self, string):
		stringSplit = string.split(' ')
		if (len(stringSplit) == 6):
			return ScheduleEntry(stringSplit[0], stringSplit[1], stringSplit[2], \
											stringSplit[3], stringSplit[4], stringSplit[5])

	# Adds schedule entry for a single time 
	def addEntry(self, string=None, dateTime=None, value=None):
		scheduleEntry = None
		if (string != None):
			scheduleEntry = self._parseCronToScheduleEntry(string)			
		elif ((time != None) and (value !=None)):
			scheduleEntry = ScheduleEntry(dateTime.minute, dateTime.hour, dateTime.day, \
																dateTime.month, '*', value) 	
		if (scheduleEntry != None):
			self.scheduleEntries.append(scheduleEntry)
	
	# Print in glm format 
	def toGLM(self):
		glm = 'schedule ' + self.name + ' {\n'
		for entry in self.scheduleEntries:
			glm += '	' + entry.toString() + '\n'
		glm += '}\n'
		return glm

	#TODO 5: Implement once a rest interface has been implemented for schedules
	def save(self):
		glm = getGLM()
		#save the glm format
		

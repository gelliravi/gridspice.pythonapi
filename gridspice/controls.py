#!/usr/bin/env python

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

import paramiko
import os, sys, shutil
import config
import scp

"""
Zips up the directory, and sends it to the user's account on the model server
"""
def simulate(directory): 
	if (os.path.isabs(directory)):
		zip_path = shutil.make_archive(directory, "gztar", directory);
		url = config.URL.replace('http://', '')[:-1]
		if (config.SSH_LOCATION == None):
			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(url, username=config.USER_NAME, password=config.PASSWORD)
			myScp = scp.SCPClient(client.get_transport())
			myScp.put(zip_path, '~/');
		else:
			os.system('scp -i ' + config.SSH_LOCATION + ' ' + zip_path + ' ec2-user@' + url + ':~/');
	else:
		raise ValueError("'" + directory + "'"  + " is not an absolute pathname.")

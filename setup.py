#!/usr/bin/env python
from boto.ec2.connection import EC2Connection
from boto.s3.connection import S3Connection
import boto.ec2, os, math, sys, time, random, string
from getpass import getpass

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

# Root Installation
def root_install(accessKey, secretKey, key_name):
	steps = 1; 

	# Sets up connection.
	print(repr(steps) + "] Retrieving connection.\n");
	steps += 1;
	regionName = boto.ec2.get_region(region_name = 'us-west-1');
	conn_ec2 = EC2Connection(accessKey, secretKey, region = regionName);
	conn_s3 = S3Connection(accessKey, secretKey);

	# Creates Security Group
	security_groups = conn_ec2.get_all_security_groups();
	containsGridSpiceDev = False;
	for group in security_groups:
		if group.name == 'gridspice_dev':
			containsGridSpiceDev = True;

	if containsGridSpiceDev == False:
		print(repr(steps) + "] Development security group not found. Creating one.\n");
		steps += 1;
		gridspice_dev = conn_ec2.create_security_group('gridspice_dev', 'GridSpice development')
		gridspice_dev.authorize('tcp', 80, 80, '0.0.0.0/0')
		gridspice_dev.authorize('tcp', 22, 22, '0.0.0.0/0')

	# Retrieves GridSpiceModelServer Image
	imageObject = conn_ec2.get_image('ami-bc3b12f9');

	# Creates a new keypair & stores private key.
	key_pairs = conn_ec2.get_all_key_pairs();
	found = False;
	for x in key_pairs:
		if (x.name == key_name):
			found = True;
	if found == False:
		print(repr(steps) + "] Key pair not found. Creating key-pair: \n");
		steps += 1;
		key_pair = conn_ec2.create_key_pair(key_name);
		file_name = key_name;
		f = open(file_name, 'w');
		f.write(key_pair.material);
		f.close();
		os.system("chmod 600 " + file_name);
		os.system("mv " + file_name + " ~/.ssh/");
		print("    ~/.ssh/" + file_name + "\n");

	# Creates buckets
	print(repr(steps) + "] Setting up buckets\n");
	steps += 1;
	char_set = string.ascii_lowercase + string.digits;
	buckets = conn_s3.get_all_buckets();
	randString = ''.join(random.sample(char_set, 30));
	bucket1 = 'org.gridspice.glm.' + randString;
	bucket2 = 'org.gridspice.models.' + randString;
	bucket3 = 'org.gridspice.results.' + randString;
	buckets_to_generate = [bucket1, bucket2, bucket3];
	for bucket_check in buckets_to_generate:
		exists = False;
		for bucket in buckets:
			if (bucket.name == bucket_check):
				exists = True;
		if (exists == False):
			conn_s3.create_bucket(bucket_check);     

	# Creates instance from the image.
	reservation = imageObject.run(key_name=key_name, security_groups = ['gridspice_dev']);
	instance = reservation.instances[0];
	count = 0;
	numBars = 50;
	while True:
		status = instance.update();
		sys.stdout.flush();
		if status == 'running':
			break;
		progress = repr(steps) + '] Starting instance: |';
		bars = count % numBars;
		for x in range(0, bars):
			progress += '>';
		for x in range(0, numBars - bars):
			progress += ' ';
		progress += '|';
		sys.stdout.write(progress + "\r");
		count += 1;

	# Wait for 60 seconds to allow set-up to complete.
	for i in range(0, 240):
		time.sleep(0.75);
		bars = count % numBars;
		progress = repr(steps) + '] Starting instance: |';
		for x in range(0, bars):
			progress += '>';
		for x in range(0, numBars - bars):
			progress += ' ';
		progress += '|';
		sys.stdout.write(progress + "\r");
		sys.stdout.flush();
		count += 1;    

	print(repr(steps) + "] Done starting instance.                                                  \n");
	sys.stdout.flush();

	# Generating Master API Key 
	steps += 1;
	print(repr(steps) + "] Generating master api key:\n");
	char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits;
	masterKey = ''.join(random.sample(char_set,50));
	print("    " + masterKey + "\n");

	# Create config files on instance
	steps += 1;
	print(repr(steps) + "] Loading config files on remote server:\n");
	steps += 1;
	command = "ssh -t -i ~/.ssh/" + key_name + " ec2-user@" + instance.public_dns_name + \
				" python /home/ec2-user/.gridspice/setup.py " + accessKey + " " + \
				secretKey + " " + masterKey + " " + key_name + " " + \
				"http://" + instance.public_dns_name + "/" + " " + bucket1 + " " + \
				bucket2 + " " + bucket3;
	os.system(command); 
	print('\n');

	# Creating local config file
	print("\n");
	print(repr(steps) + "] Writing URL to configuration file.\n");
	steps += 1;
	with open('gridspice/config_template', 'r') as file:
	  data = file.readlines();
	  data += 'URL = ' + '"http://' + instance.public_dns_name + '/" \n';
	  data += 'ACCESS_KEY = ' + '"' + accessKey + '"\n';
	  data += 'SECRET_KEY = ' + '"' + secretKey + '"\n';
	  data += 'IMAGE_ID = ' + '"' + imageObject.name + '"\n';
	  data += 'MASTER_KEY = ' + '"' + masterKey + '"\n';
	  data += 'SSH_LOCATION = ' + '"' + '~/.ssh/' + key_name + '"\n';

	with open('gridspice/config.py', 'w') as file:
	  file.writelines(data);

	print(repr(steps) + "] Installation Complete! Your public domain name is:\n");
	print('    http://' + instance.public_dns_name + '/\n');

# User installation
def user_install(url, username, password):
	steps = 1;  
	print(repr(steps) + "] Creating configuration file.\n");
	steps += 1;

	with open('gridspice/config_template', 'r') as file:
		data = file.readlines();
		data += 'URL = "' + url + '"\n';
		data += 'MASTER_KEY = None\n';
		data += 'SSH_LOCATION = None\n';
		data += 'USER_NAME = "' + username + '"\n';
		data += 'PASSWORD = "' + password + '"\n';		
 
	with open('gridspice/config.py', 'w') as file:
		file.writelines(data);

	print(repr(steps) + "] Installation Complete! Your public domain name is:\n");
	print("    " + url +"\n");


if __name__ == '__main__':
  print("\n");
  print(" =========================== \n");
  print("== GridSpice Installation: == \n");
  print(" =========================== \n");

  # Asks whether user wants to install as root
  key = raw_input("Please input your AWS Access Key: ");
  value = getpass("Please input your AWS Secret Key: ");
  key_pair_name = raw_input("Please input the name of your desired key_pair: ");
  print("\n");
  root_install(key, value, key_pair_name); 

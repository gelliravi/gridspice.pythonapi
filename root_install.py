#!/usr/bin/env python
from boto.ec2.connection import EC2Connection
import boto.ec2, os, math, sys, time, random, string

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

# Retrieves access key and secret key.
if len(sys.argv) != 4:
    sys.exit("Need three arguments");

accessKey = sys.argv[1];
secretKey = sys.argv[2];
key_name = sys.argv[3];

steps = 1; 

print("\n");
print(" ================================ \n");
print("== GridSpice Root Installation: == \n");
print(" ================================ \n");

# Sets up connection.
print(repr(steps) + "] Retrieving connection.\n");
steps += 1;
regionName = boto.ec2.get_region(region_name = 'us-west-1');
conn = EC2Connection(accessKey, secretKey, region = regionName);

# Creates Security Group
security_groups = conn.get_all_security_groups();
containsGridSpiceDev = False;
for group in security_groups:
    if group.name == 'gridspice_dev':
        containsGridSpiceDev = True;

if containsGridSpiceDev == False:
    print(repr(steps) + "] Development security group not found. Creating one.\n");
    steps += 1;
    gridspice_dev = conn.create_security_group('gridspice_dev', 'GridSpice development')
    gridspice_dev.authorize('tcp', 80, 80, '0.0.0.0/0')
    gridspice_dev.authorize('tcp', 22, 22, '0.0.0.0/0')

# Retrieves GridSpiceModelServer Image
imageObject = conn.get_image('ami-5e93b01b');

# Creates a new keypair & stores private key.
key_pairs = conn.get_all_key_pairs();
found = False;
for x in key_pairs:
    if (x.name == key_name):
        found = True;
if found == False:
    print(repr(steps) + "] Key pair not found. Creating key-pair: \n");
    steps += 1;
    key_pair = conn.create_key_pair(key_name);
    file_name = 'id_rsa-' + key_name;
    f = open(file_name, 'w');
    f.write(key_pair.material);
    f.close();
    os.system("chmod 600 " + file_name);
    os.system("mv " + file_name + " ~/.ssh/");
    print("    ~/.ssh/" + file_name + "\n");

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

# Wait for 45 seconds to allow set-up to complete.
for i in range(0, 120):
    time.sleep(0.5);
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
print(repr(steps) + "] Loading config files on remote server.\n");
steps += 1;
command = "ssh -i ~/.ssh/id_rsa-" + key_name + " ec2-user@" + instance.public_dns_name + " python /home/ec2-user/.gridspice/setup.py " + accessKey + " " + secretKey + " " + masterKey;
os.system(command);

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

with open('gridspice/config.py', 'w') as file:
  file.writelines(data);

print(repr(steps) + "] Installation Complete! Your public domain name is:\n");
print('    http://' + instance.public_dns_name + '/\n');

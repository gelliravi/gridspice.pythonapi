#!/usr/bin/env python
import sys, math

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

print("\n");
print(" ================================ \n");
print("== GridSpice User Installation: == \n");
print(" ================================ \n");

if len(sys.argv) != 2:
   sys.exit("Please enter URL of GridSpice server, beginning with 'http://'");

steps = 1; 
print(repr(steps) + "] Creating configuration file.\n");
steps += 1;
url = sys.argv[1];

with open('gridspice/config_template', 'r') as file:
    data = file.readlines();
    data += 'URL = ' + url + '\n';
 
with open('gridspice/config.py', 'w') as file:
    file.writelines(data);

print(repr(steps) + "] Installation Complete! Your public domain name is:\n");
print("    " + url +"\n");

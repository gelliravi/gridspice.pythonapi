#!/usr/bin/python

from gridspice.model import Model
from gridspice import element

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

mod = Model('test');
file_1 = 'samplefeeders/R1-12.47-1.glm';
file_2 = 'samplefeeders/R1-12.47-2.glm';
output_1 = 'samplefeeders/output_1.glm';
output_2 = 'samplefeeders/output_2.glm';


# Parse and Edit file_1's name attribute and write to output_1
mod.load(file_1);
node_obj = mod.elementDict[0];
node_obj.name = 'new_name';
mod.sync(output_1);

# Parse file_2 and write to output_2 (Does not parse recorders, because there is no existing recorder class)
mod.load(file_2);
mod.sync(output_2);

#!/usr/local/bin/python

from gridspice import account, project, model, simulation, result, element, config
import sys, time

__author__ = "Jimmy Du and Kyle Anderson"
__copyright__ = "Copyright 2013, The GridSpice Project"
__license__ = "BSD"
__version__ = "1.0"
__maintainer__ = ["Kyle Anderson", "Jimmy Du"]
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"]
__status__ = "Development"

account_name = 'test@example.com'
acc = account.Account(config.MASTER_KEY, account_name)
projs = acc.getProjects()
proj = None
if (len(projs) < 2):
	proj = project.Project("Generated Project", acc)
	proj.save()
else:
	proj = projs[1]

mods = proj.getModels()
if (len(mods) == 0):
	mod = model.Model("Generated Distribution", proj)
	lat = 37.449
	long = -122.1960
	for x in range(1, 4):
		nod = element.powerflow.powerflow_object.node()
		nod.latitude = repr(lat + x*0.001)
		nod.longitude = repr(long + x*0.001)
		nod.name = 'node-' + repr(x)
		mod.add(nod)
	mod.save()

sim = proj.runSimulation()

while (True):
	time.sleep(3)
	sim.load()
	print(sim.status)
	if (sim.status == 'COMPLETE'):
		break

results = sim.getResults()
res = results[0]
res.load()
print (res.content)

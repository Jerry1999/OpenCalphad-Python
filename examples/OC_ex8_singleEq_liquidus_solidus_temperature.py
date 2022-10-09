"""
This example shows how to use intermediate module for single equilibrium calculation plus liquidus and solidus temperatures.
To calculate the liquidus and solidus temperature fixed phase conditions for the liquid phase is utilized.
HSS steel is used as an example.

author: Chunhui Luo, 2022
"""

import copy
from math import ceil
import numpy as np

# import ocpython from python/Lib/site-packages/ocpython
from ocpython.OCPython_utility import OCPython_utility
import ocpython
from ocpython.OCPython import SingleEquilibriumCalculation
from ocpython.OCPython import Verbosity
from ocpython.OCPython import PhaseStatus as phStat
from ocpython.OCPython import GridMinimizerStatus as gmStat
from ocpython.OCPython import MassUnit as massUnit

# set verbosity (True or False (default))
vs = Verbosity(newlogfile=True,process_name='SingleEquilibriumCalculation')
isVerbosity = False
vs.setVerbosity(isVerbosity)

# Initiate SingleEquilibriumCalculation module
oc = SingleEquilibriumCalculation(vs)

# reading database (.tdb file)
tdbFile=r'steel1.TDB'
elements = ['FE','C','CR','MO','SI','V']
oc.readtdb(tdbFile,elements)

# get all phases in the system
nPhase = oc.getNumberPhase()
phases = []
for index in range(nPhase):
	phases.append(oc.getPhaseName(index))

try:
	comp = oc.getComponentNames()
	print('components list from database:', comp)
	print('')
except:
	pass

if (0):	# change o to 1 to activate print
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15}".format(phase_list[i], status[i]), '{:10.4f}'.format(amdgm[i]))
	print('')

# set pressure and temperature
oc.setPressure(1E5)
oc.setTemperature(1600)
oc.setTotalMolarAmount(1)

elementMassFractions = {
	'C' : 0.009,
	'CR' : 0.045,
	'MO': 0.1,
	'SI': 0.001,
	'V': 0.009,
    'FE': -1
	}
oc.setElementMassFraction(elementMassFractions)

# calculate equilibrium with grid-minimizer
oc.calculateEquilibrium(gmStat.On)

stablePhaseAndFraction = OCPython_utility.getStablePhase(oc)
for phase, fraction in stablePhaseAndFraction.items():
        print("Amount of " + phase + " = {0:.4f}".format(fraction))

# for liquidsus temperature
oc.setTemperature(None)
phaseNames = ['LIQUID']
phaseStatus = 2	# fixed

oc.setPhasesStatus(phaseNames, phaseStatus, phaseAmount=1.0)
oc.listConditions()

if (0):	# change o to 1 to activate print
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15}".format(phase_list[i], status[i]), '{:10.4f}'.format(amdgm[i]))
	print('')

# eqilibrium calculation
oc.calculateEquilibrium(gmStat.On)
oc.listEqResults()

# show result
Temp = oc.getScalarResult('T')
print('Liquidus temperature is ',"{:.2f}".format(Temp), 'K')

stablePhaseAndFraction = OCPython_utility.getStablePhase(oc)
for phase, fraction in stablePhaseAndFraction.items():
        print("Amount of " + phase + " = {0:.4f}".format(fraction))

# for solidius temperature
oc.setPhasesStatus(phaseNames, phaseStatus, phaseAmount=0.0)
oc.listConditions()

if (0):	# change o to 1 to activate print
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print ("{:<20} {:<15} {:<6}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15}".format(phase_list[i], status[i]), '{:10.4f}'.format(amdgm[i]))
	print('')

# eqilibrium calculation
oc.calculateEquilibrium(gmStat.On)
oc.listEqResults()

# show result
Temp = oc.getScalarResult('T')
print('Solidus temperature is ',"{:.2f}".format(Temp), 'K')

stablePhaseAndFraction = OCPython_utility.getStablePhase(oc)
for phase, fraction in stablePhaseAndFraction.items():
	print("Amount of " + phase + " = {0:.4f}".format(fraction))
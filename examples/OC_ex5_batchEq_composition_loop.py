"""
This example shows how to create a 3D diagram using TC-Python.
Composition step varible is used for batch equlibria computation.
Two composition axes are defined.
Two alloys (HSS steel and AlMgZn alloy) are optional to use.

author: Chunhui Luo, 2022
"""

import timeit
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
vs.setVerbosity(False)

# Initiate SingleEquilibriumCalculation module
oc = SingleEquilibriumCalculation(vs)

# please use # to not set alloy No or remove # to set alloy No
alloy = 1	# HSS(FeCCrMoSiV)
#alloy = 2	# AlMgZn

# reading database (.tdb file)
if alloy == 1:
	tdbFile = r'steel1.TDB'
	elements = ['FE','C','CR','MO','SI','V']
elif alloy == 2:
	tdbFile = r'cost507R.TDB'
	elements = ['AL','MG','ZN']	
oc.readtdb(tdbFile,elements)

comp = oc.getComponentNames()

nPhase = oc.getNumberPhase()
phases = []
for index in range(nPhase):
	phases.append(oc.getPhaseName(index))

# set phase status
if alloy == 1:
	phaseNames=['FCC_A1','M23C6','M6C']
	#phaseNames=[]
elif alloy == 2:
	phaseNames=[]

if (0):	# change o to 1 to activate print
	nPhase = oc.getNumberPhase()
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

if phaseNames:
	oc.setPhasesStatus(('* ',),phStat.Suspended)
	oc.setPhasesStatus(phaseNames,phStat.Entered)

# after possible phase status change
if (0):	# change o to 1 to activate print
	nPhase = oc.getNumberPhase()
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print('')
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

# set pressure and temperature
oc.setPressure(1E5)
oc.setTotalMolarAmount(1)
if alloy == 1:
	oc.setTemperature(1173.15)
elif alloy == 2:
	oc.setTemperature(873.15)

# set element molar fraction
if alloy == 1:
	elementMoleFractions = {
		'C' : 0.042,
		'CR' : 0.048,
		'MO': 0.058,
		'SI': 0.002,
		'V': 0.01,
		'FE': -1
		}
elif alloy == 2:
	elementMoleFractions = {
		'MG' : 0.01,
		'ZN' : 0.02,
		'AL': -1
		}

oc.setElementMolarFraction(elementMoleFractions)

# calculate equilibrium with or without the grid-minimizer
oc.calculateEquilibrium(gmStat.On)
G_On=oc.getGibbsEnergy() # a scalar

if (0):	# change o to 1 to activate print
	nPhase = oc.getNumberPhase()
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

if alloy == 1:
	elem_1 = 'CR'
	elem_2 = 'MO'
	xlabel = 'X(Cr)'
	ylabel = 'X(Mo)'
	x_elem1_list = np.linspace(1e-4,5e-2,20)	#molar fraction for composition axis 1
	x_elem2_list = np.linspace(1e-4,6e-2,20)	#molar fraction for composition axis 2
	temp = 1073.15	#unit: K

elif alloy == 2:
	elem_1 = 'MG'
	elem_2 = 'ZN'
	xlabel = 'X(Mg)'
	ylabel = 'X(Zn)'
	x_elem1_list = np.linspace(1e-4,5e-2,20)	#molar fraction for composition axis 1
	x_elem2_list = np.linspace(1e-4,6e-2,20)	#molar fraction for composition axis 2
	temp = 873.15	#unit: K

# create xfrac_matrix
xfrac_matrix = []
for i,x_elem1 in enumerate(x_elem1_list):
	for j,x_elem2 in enumerate(x_elem2_list):
		elementMoleFractions[elem_1] = x_elem1
		elementMoleFractions[elem_2] = x_elem2
		x = np.array(list(elementMoleFractions.values())).flatten()
		xfrac_matrix.append(x)
n_xfrac = len(x_elem1_list) * len(x_elem2_list)

starttime = timeit.default_timer()
stavar = 'G'
G = oc.batchEquilibriaComp(n_xfrac,elementMoleFractions,xfrac_matrix,temp,stavar)
print("The time for performing batch Equilibria is :", "{:.3f}".format(timeit.default_timer() - starttime), '[s]')

OCPython_utility.plotContour(x_elem1_list, x_elem2_list, G, xlabel, ylabel, 
			"Gibbs free energy contour at "+str(temp)+" K (unit: J)")

OCPython_utility.plot3D(x_elem1_list, x_elem2_list, G, xlabel, ylabel, 'Gibbs free energy [J]',
			"Gibbs free energy surfaces at "+str(temp)+" K")
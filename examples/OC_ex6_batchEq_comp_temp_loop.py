"""
This example shows how to create a 3D diagram using TC-Python.
One step varible is temperature, another step variable is composition
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
vs.setVerbosity(True)

# Initiate SingleEquilibriumCalculation module
oc = SingleEquilibriumCalculation(vs)

# please use # to not set alloy No or remove # to set alloy No
#alloy = 1	# HSS(FeCCrMoSiV)
alloy = 2	# AlMgZn

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

# set phase status
if alloy == 1:
	phaseNames=['BCC_A2','FCC_A1','M23C6','M6C']
	#phaseNames=[]
elif alloy == 2:
	phaseNames=[]

if phaseNames:
	oc.setPhasesStatus(('* ',),phStat.Suspended)
	oc.setPhasesStatus(phaseNames,phStat.Entered)

nPhase = oc.getNumberPhase()

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

# calculate equilibrium with or without the grid-minimizer
oc.calculateEquilibrium(gmStat.Off)
G_Off = oc.getGibbsEnergy() # a scalar

if alloy == 1:
	elem = 'CR'
	x_elem_list = np.linspace(1e-4,5e-2,10)
	temp_list = np.linspace(773,1273,40)
	xlabel = 'Temperature, K'
	ylabel = 'X(Cr)'

elif alloy == 2:
	elem = 'MG'
	x_elem_list = np.linspace(1e-4,5e-2,10)
	temp_list = np.linspace(473.15,873.15,40)
	xlabel = 'Temperature, K'
	ylabel = 'X(Mg)'

# create xfrac matrix
xfrac_matrix = []
for i,x_elem in enumerate(x_elem_list):
		elementMoleFractions[elem] = x_elem
		x = np.array(list(elementMoleFractions.values())).flatten()
		xfrac_matrix.append(x)

n_xfrac = len(x_elem_list)

starttime = timeit.default_timer()
stavar = 'G'

G = []
for temp_ in temp_list:
	temp_list_ = [temp_]

	try:
		G_ = oc.batchEquilibriaComp(n_xfrac,elementMoleFractions,xfrac_matrix,temp_list_,stavar)
		G.extend(G_)
	except Exception as e:
		print (e.message, e.args)
print("The time for performing batch Equilibria is :", "{0:.3f}".format(timeit.default_timer() - starttime), '[s]')

try:
	OCPython_utility.plotContour(temp_list, x_elem_list, G, xlabel, ylabel, 
			"Gibbs free energy contour (unit: J)")

	OCPython_utility.plot3D(temp_list,x_elem_list, G, xlabel, ylabel, 'Gibbs free energy [J]',
			"Gibbs free energy surfaces")

except Exception as e:
	pass
	#print (e.message, e.args)
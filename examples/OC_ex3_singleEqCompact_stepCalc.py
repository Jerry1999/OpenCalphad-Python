"""
This example shows how to use intermediate module for single equilibrium calculation with compact mode and temperature step calculation.
HSS steel is used as an example.

author: Chunhui Luo, 2022
"""

import json
import timeit
import numpy as np
import matplotlib.pyplot as plt

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

# Initiate SingleEquilibriumCalculationCompact module
oc = SingleEquilibriumCalculation(vs)

tdbFile=r'steel1.TDB'
elements = ['FE','C','CR','MO','SI','V']

# HSS steel
# mass_unit: Mass_Fraction
elementFractions = {
	'C' : 0.009,
	'CR' : 0.045,
	'MO': 0.1,
	'SI': 0.001,
	'V': 0.009,
    'FE': -1
}
tpn = {
	'T' : 1200.0,
	'P' : 1E5,
	'N' : 1.0
}

starttime = timeit.default_timer()

# perform single equilibrium Calculation with compact mode
oc.singleEquilibriumCalculation_Compact(tdbFile,	# tdb database
					elements,						# element list
                    massUnit.MassFraction,
					tpn,							# values for temperature, pressure and molar amount
					elementFractions,			# compostions for alloy
					#phaseNames = phaseNames,			# specified phase list, as option
					#elementReferencePhase=elementReferencePhase	# set reference phase for element, as option
					)
# the current problem: if phaseNames = phasenames is activated in the above compact mode, G = 0	, exit code, to be solved

print("The time for performing singleEquilibriumCalculation_Compact is :", timeit.default_timer() - starttime)
print('')

oc.listEqResults()
print('')

print('Gibbs energy [J]: ', "{0:.3f}".format(oc.getGibbsEnergy()))
print('')

H_dict = oc.getValuePhase('H')
print('Enthalpy values for all phases [J]')
print('H = ',json.dumps(json.loads(json.dumps(H_dict), parse_float=lambda x: round(float(x), 3))))

print('')

T_list = np.arange(600,1800,10)
print('total loops for setting temperature and preforming calculate equilibrium are:', len(T_list))
print('')

starttime = timeit.default_timer()

Eq_str = []
TK_list = []
H_list = []
for T in T_list:
	oc.setTemperature(T)
	oc.calculateEquilibrium(gmStat.Off)
	TK_list.append(T)
	H_list.append(oc.getScalarResult('H'))

print("The total time for ", len(T_list)," loops is :",  "{0:.3f}".format(timeit.default_timer() - starttime), '[s]')

plt.plot(TK_list, H_list)
plt.xlabel("Temperature [K]")
plt.ylabel("Enthalpy [J]")
plt.tight_layout()
plt.show()
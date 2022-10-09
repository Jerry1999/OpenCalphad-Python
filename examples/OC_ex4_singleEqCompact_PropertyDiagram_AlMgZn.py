"""
This example shows how to create a property (step) diagram using OC-Python.
AL-Cu-Mg-Zn alloy is used as an example. 
The step variable is temperature.

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

# Initiate SingleEquilibriumCalculation module
oc = SingleEquilibriumCalculation(vs)

# define system
tdbFile = r'cost507R.TDB'
elements = ['AL','CU','MG','ZN']	

# AlMgZn
# mass_unit: Mass_Fraction
elementFractions = {
	'CU' : 0.02,
	'MG' : 0.02,
	'ZN' : 0.06,
	'AL': -1
	}

tpn = {
	'T' : 800.0,
	'P' : 1E5,
	'N' : 1.0
}
starttime = timeit.default_timer()

# perform single equilibrium Calculation with compact mode
oc.singleEquilibriumCalculation_Compact(tdbFile,     # tdb database
                    elements,                        # element list
                    massUnit.MassFraction,
                    tpn,                             # values for temperature, pressure and molar amount
                    elementFractions,            # compostions for alloy
                    #phaseNames = phaseNames,        # specified phase list, as option
                    #elementReferencePhase=elementReferencePhase    # set reference phase for element, as option
                    )
# the current problem: if phaseNames = phasenames is activated in the above compact mode, G = 0	, exit code to be solved

print("The time for performing singleEquilibriumCalculation_Compact is :", timeit.default_timer() - starttime)

oc.listEqResults()

comp = oc.getComponentNames()

starttime = timeit.default_timer()

T_list = np.arange(300,1000,10)

starttime = timeit.default_timer()

stateVar = 'NP'     # currently only 'NP' and 'NPM' were tested.
values_dict, T_K = OCPython_utility.calc_phasefrac_temploop_nonewphase(oc,gmStat,T_list,stateVar)

print("The total time for above loops is :", "{0:.3f}".format(timeit.default_timer() - starttime), '[s]')
print('')

for key,value in values_dict.items():
	if not all(v == 0 for v in values_dict[key]):
		plt.plot(T_K, values_dict[key],'-',label = str(key))

plt.xlabel("Temperature [K]")
plt.ylabel("Moles of phases [Mole]")
plt.tight_layout()
plt.legend()
plt.show()
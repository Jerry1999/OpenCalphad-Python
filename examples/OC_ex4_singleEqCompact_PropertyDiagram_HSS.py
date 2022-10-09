"""
This example shows how to create a property (step) diagram using OC-Python.
HSS steel steel is used as an example. 
The step variable is temperature.

author: Chunhui Luo, 2022
"""
import json
import timeit
import numpy as np
import matplotlib.pyplot as plt

# import ocpython from python/Lib/site-packages/ocpython
from ocpython.OCPython_utility import OCPython_utility
#from OCPython_utility import OCPython_utility
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
# the current problem: if phaseNames = phasenames is activated in the above compact mode, G = 0	, exit code, to be solved

print("The time for performing singleEquilibriumCalculation_Compact is :","{0:.3f}".format(timeit.default_timer() - starttime), '[s]')

oc.listEqResults()

comp = oc.getComponentNames()

starttime = timeit.default_timer()

# segment 1
starttime = timeit.default_timer()

T_list = np.arange(1420,2000,10)

stateVar = 'NPM'     # currently only 'NP' and 'NPM' were tested.
values_dict1, T_K_1, C_comp_in_FCC_A1_1 = OCPython_utility.calc_phasefrac_temploop_newphase(oc,gmStat,T_list,stateVar)

print("The total time for above loops is :", "{0:.3f}".format(timeit.default_timer() - starttime), '[s]')
print('')

# segment 2
starttime = timeit.default_timer()

T_list = np.arange(800,1410,10)

values_dict2, T_K_2, C_comp_in_FCC_A1_2 = OCPython_utility.calc_phasefrac_temploop_newphase(oc,gmStat,T_list,stateVar)

print("The total time for above loops is :", "{0:.3f}".format(timeit.default_timer() - starttime), '[s]')
print('')

key1 = list(values_dict1.keys())
key2 = list(values_dict2.keys())
key3 = list(set(key1) ^ set(key2))
key4 = list(set(key1) & set(key2))

keys12 = [*key3, *key4]

values_dict = {}
for key_ in keys12:

	if key_ in key1:
		value1_ = values_dict1[key_]
	else:
		value1_ = np.zeros(len(values_dict1[key1[0]]))
	if key_ in key2:
		value2_ = values_dict2[key_]
	else:
		value2_ = np.zeros(len(values_dict2[key2[0]]))
 
	values_dict[key_] = [*value2_, *value1_]

NewList = [sum(n) for n in zip(values_dict['FCC_A1#1'],values_dict['FCC_A1'])]
values_dict['FCC_A1#1'] = NewList

index1 = [i for i,v in enumerate(C_comp_in_FCC_A1_1) if v > 0.1]

index2 = [i for i,v in enumerate(C_comp_in_FCC_A1_2) if v > 0.1]

a = []
b = []
for i in index2:
	a.append(values_dict['FCC_A1#1'][i])
	b.append(values_dict['FCC_A1_AUTO#2'][i])

for i,v in enumerate(values_dict['FCC_A1#1']):
	if i > index2[-1]:
		a.append(values_dict['FCC_A1_AUTO#2'][i])
		b.append(values_dict['FCC_A1#1'][i])

values_dict['FCC_A1#1'] = b
values_dict['FCC_A1_AUTO#2'] = a

try:
	del values_dict['FCC_A1']
except KeyError as ex:
	print("No such key: '%s'" % ex.message)

T_K = [*T_K_2, *T_K_1]
for key,value in values_dict.items():
	if not all(v == 0 for v in values_dict[key]):
		try:
			plt.plot(T_K, values_dict[key],'-',label = str(key))
		except:
			print('key is: ', key)

plt.xlabel("Temperature [K]")
plt.ylabel("Moles of phases [Mole]")
plt.tight_layout()
plt.legend()
plt.show()
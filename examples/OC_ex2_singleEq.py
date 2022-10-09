"""
This example shows how to use itermediate module for single equlibrium calculation.
HSS steel is used as an example. 

author: Chunhui Luo, 2022
"""
import json

# import ocpython from python/Lib/site-packages/ocpython
from ocpython.OCPython_utility import OCPython_utility
import ocpython
from ocpython.OCPython import SingleEquilibriumCalculation
from ocpython.OCPython import Verbosity
from ocpython.OCPython import PhaseStatus as phStat
from ocpython.OCPython import GridMinimizerStatus as gmStat

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
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

# set phase status
phaseNames=['BCC_A2','FCC_A1','M23C6','M6C']
oc.setPhasesStatus(('*',),phStat.Suspended)	# suspend all phases
oc.setPhasesStatus(phaseNames,phStat.Entered)	# enter the specified phases

if (0):	# change o to 1 to activate print
	phase_list,status,amdgm = oc.getPhasesStatus(nPhase)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

# set pressure and temperature
oc.setPressure(1E5)
oc.setTemperature(800)
oc.setTotalMolarAmount(1)

# set element mass fraction
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
oc.changeEquilibriumRecord('eq_gmOn')
oc.calculateEquilibrium(gmStat.On)
print('')

# list stable phases

stablePhaseAndFraction = OCPython_utility.getStablePhase(oc)
print('Stable phases at T =', oc.getScalarResult('T'),'K:')
for phase, fraction in stablePhaseAndFraction.items():
	print("Amount of " + phase + " = {0:.5f}".format(fraction))
print('')

# get results in general form
x1 = oc.getValuePhase('G')	# Gibbs energy values for all phases
print('Gibbs energy values for all phases [J]:')
print(json.dumps(json.loads(json.dumps(x1), parse_float=lambda x: round(float(x), 3))))
print('')
x2 = oc.getScalarResult('G')  # Gibbs energy of the system
print('Gibbs energy of the system [J]:', "{0:.3f}".format(x2))
print('')
x3 = oc.getValueComponent('W') # mass fraction values for all components
print('Mass fraction values for all components:')
print(json.dumps(json.loads(json.dumps(x3), parse_float=lambda x: round(float(x), 5))))
print('')
x4 = oc.getValueComponent('MU') # chemical potential values for all components
print('Chemical potential values for all components (J/mol]):')
print(json.dumps(json.loads(json.dumps(x4), parse_float=lambda x: round(float(x), 3))))
print('')

# calculate equilibrium without the grid-minimizer
oc.changeEquilibriumRecord('eq_gmOff')
oc.calculateEquilibrium(gmStat.Off)

# retrieve Gibbs energies and watch variation of the G values
oc.changeEquilibriumRecord('eq_gmOn')
G_gmOn=oc.getGibbsEnergy() # a scalar
print('')
print('Gibbs energy with grid-minimizer:',"{0:.3f}".format(G_gmOn), '[J]')
oc.changeEquilibriumRecord('eq_gmOff')
G_gmOff=oc.getGibbsEnergy() # a scalar
print('Gibbs energy without grid-minimizer:',"{0:.3f}".format(G_gmOff), '[J]')
print('')

# retrieve chemical potentials
mu=oc.getChemicalPotentials()
print('Chemical potential [J/mol]:\n','mu_FE= ',"{0:.3f}".format(mu['FE']))
print('')

# retrieve element composition in phases
phaseElementComposition = oc.getPhaseElementComposition()
if not isVerbosity: print('phase element composition:\n'+json.dumps(json.loads(json.dumps(phaseElementComposition), parse_float=lambda x: round(float(x), 6)),indent=4))
try:
	print('n_C in FCC_A1#1 = ', "{0:.5f}".format(phaseElementComposition['FCC_A1#1']['C']))
except:
	print('n_C in FCC_A1 = ',"{0:.5f}".format(phaseElementComposition['FCC_A1']['C']))
print('')

# retrieve sites in phases
phaseSites = oc.getPhaseSites()
if not isVerbosity: print('phase sites:\n'+json.dumps(json.loads(json.dumps(phaseSites), parse_float=lambda x: round(float(x), 6)),indent=4))
try:
	print('a_i in FCC_A1#1 = ',phaseSites['FCC_A1#1'])
except KeyError:
	print('a_i in FCC_A1 = ',phaseSites['FCC_A1'])
print('')

# retrieve constituent compositionn in phases
phaseConstituentComposition = oc.getPhaseConstituentComposition()
if not isVerbosity: print('phase constituent composition:\n'+json.dumps(json.loads(json.dumps(phaseConstituentComposition), parse_float=lambda x: round(float(x), 6)),indent=4))
try:
	print('y_V^0 in liquid = ', "{0:.5f}".format(phaseConstituentComposition['FCC_A1#1']['sublattice 0']['V']))
except:
	print('y_V^0 in liquid = ',  "{0:.5f}".format(phaseConstituentComposition['FCC_A1']['sublattice 0']['V']))
print('')

# retrieve constituents description
constituentsDescription = oc.getConstituentsDescription()
print('m_V = ',constituentsDescription['V']['mass'])
print('q_V = ',constituentsDescription['V']['charge'])
print('stoi^V_V = ',constituentsDescription['V']['elements']['V'])
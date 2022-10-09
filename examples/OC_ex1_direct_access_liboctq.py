"""
This example shows how to use directly subroutines in liboctq.f90.
HSS steel is used as an example. 
Only single equlibrium is calculated.

author: Chunhui Luo, 2022
"""

import numpy as np
#from ocpython.OCPython_utility import OCPython_utility
from ocpython.OCPython_utility import OCPython_utility
try:
	from ocpython import liboctq_f90wrap as oc
except:
	import liboctq_f90wrap as oc

# initiate tq
eq = oc.f90wrap_pytqini(0)

tdbFile=r'steel1.TDB'
elements = ['FE','C','CR','MO','SI','V']
xstring = OCPython_utility.comp_new_order(elements)

# reading database (.tdb file)
oc.f90wrap_pytqrpfil(tdbFile,len(elements),xstring,eq)
n,comp_ = oc.f90wrap_pytqgcom(eq)
comp = OCPython_utility.getcomp(n,comp_)

# list the whole database (tdb)
#oc.f90wrap_pytqltdb()

if (0):	# change o to 1 to activate print
	nPhase = oc.f90wrap_pytqgnp(eq)
	status = np.zeros((nPhase,), dtype=int)
	amdgm = np.zeros(nPhase)
	phasenames_bytes= oc.f90wrap_pytqgpsm(nPhase,status,amdgm,eq)
	phase_list = OCPython_utility.phase_parsing_bytes_string(nPhase,phasenames_bytes)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

oc.f90wrap_pytqphsts2('*',-3,0,eq)	# suspend all phases
phaseNames='FCC_A1;M23C6;M6C'
oc.f90wrap_pytqphsts2(phaseNames,0,0.0,eq)	# enter the specified phases

if (0):	# change o to 1 to activate print
	status = np.zeros((nPhase,), dtype=int)
	amdgm = np.zeros(nPhase)
	phase_names = oc.f90wrap_pytqgpsm(nPhase,status,amdgm,eq)
	phasenames_bytes= oc.f90wrap_pytqgpsm(nPhase,status,amdgm,eq)
	phase_list = OCPython_utility.phase_parsing_bytes_string(nPhase,phasenames_bytes)
	print ("{:<20} {:<15} {:<15}".format('Phase','Status','Driving force'))
	for i in range(nPhase):
		print ("{:<20} {:<15} {:<15}".format(phase_list[i], status[i],amdgm[i]))
	print('')

# set conditions
temperature = 1173
oc.f90wrap_pytqsetc('T',0,0,temperature,eq)

pressure = 1E5
oc.f90wrap_pytqsetc('P',0,0,pressure,eq)

moles = 1
oc.f90wrap_pytqsetc('N',0,0,moles,eq)

i=comp.index('C')
x_C = 0.042
oc.f90wrap_pytqsetc('X',i+1,0,x_C,eq)

i=comp.index('CR')
x_CR = 0.048
oc.f90wrap_pytqsetc('X',i+1,0,x_CR,eq)

i=comp.index('MO')
x_MO = 0.058
oc.f90wrap_pytqsetc('X',i+1,0,x_MO,eq)

i=comp.index('SI')
x_SI = 0.002
oc.f90wrap_pytqsetc('X',i+1,0,x_SI,eq)

i=comp.index('V')
x_V = 0.01
oc.f90wrap_pytqsetc('X',i+1,0,x_V,eq)

# list conditions
oc.f90wrap_pytqlc(6,eq)

# calculate equilibrium
gridMinimizerStatus = 0	# with global Minimizer
oc.f90wrap_pytqce('',gridMinimizerStatus,0,0.0,eq)

oc.f90wrap_pytqlr(6,eq)

value=np.empty(1)
symbol='G'
oc.f90wrap_pytqgetv(symbol,0,0,1,value,eq)
print('G =',  "{:.3f}".format(value[0]), ' [J]')
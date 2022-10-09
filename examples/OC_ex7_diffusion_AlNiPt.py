"""
This example is same as fortran example (https://github.com/sundmanbo/opencalphad/tree/master/examples/TQ4lib/F90/parallel-alnipt).
It simulates diffusion in 1D using OC Ternary system Al-Ni-Pt coating of superallys
This python code can dynamically illustrate the evolution of compositions and chemical potentials with elapsed time.

author: Chunhui Luo, 2022
"""

import os
import copy,timeit
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

# reading database (.tdb file)
tdbFile=r'ALNIPT2005.TDB'
elements = ['AL','NI','PT']
oc.readtdb(tdbFile,elements)

comp = oc.getComponentNames()

# set phase status
phaseNames=['FCC_4SL#1']
oc.setPhasesStatus(('* ',),phStat.Suspended)
oc.setPhasesStatus(phaseNames,phStat.Entered)

# set pressure and temperature
oc.setPressure(1E5)
oc.setTemperature(1073)
oc.setTotalMolarAmount(1)

# set element molar fraction
elementMoleFractions_left = {
		'AL' : 0.1,
		'NI' : 0.89,
		'PT': 0.01}
elementMoleFractions_left = {i:elementMoleFractions_left[i] for i in sorted(elementMoleFractions_left.keys())}
elementMoleFractions_right = {
		'AL' : 0.1,
		'NI' : 0.05,
		'PT': 0.85}
elementMoleFractions_right = {i:elementMoleFractions_right[i] for i in sorted(elementMoleFractions_right.keys())}
oc.setElementMolarFraction(elementMoleFractions_left)

oc.calculateEquilibrium(gmStat.On)

oc.listEqResults()

mu=oc.getChemicalPotentials()

gpcur = 40	#gpcur number_of_gridpoints

mobi = [0.001, 0.001, 0.001]

dff = 0.001

# set time steps fot the current calculation
maxloop = 50000

modmod=1
plut=30

# create grid with gpcur equilibria with initial composition
# half the gridpoints has the left hand composition, the other the right hand
gpname='GP_001'
half=gpcur/2

gp = 0
gpp = {}
gpp_mu = {}
gpp_xval = {}
gpp_mu_value = {}
gpp_xval_value = {}
gpp_mu_value_new = {}
gpp_xval_value_new = {}

for comp_ in comp:
	gpp_mu_value[comp_] = 0.0
	gpp_xval_value[comp_] = 0.0
#gpp_mu['mu'] = gpp_mu_value
for i in range(gpcur):
	gpp_mu[i] = gpp_mu_value
	gpp_xval[i] = gpp_xval_value

# adds element with key 3

for i in range(gpcur):
	gp = gp + 1

	#call tqsetc('T ',0,0,tpval(1),cnum(1),gpp(gp)%eqp)
	oc.setTemperature(1073)
	#call tqsetc('P ',0,0,tpval(2),cnum(2),gpp(gp)%eqp)
	oc.setPressure(1E5)
	#call tqsetc('N ',0,0,nval,cnum(3),gpp(gp)%eqp)
	oc.setTotalMolarAmount(1)
	if gp<=half:
		elementMoleFractions = copy.deepcopy(elementMoleFractions_left)
	else:
		elementMoleFractions = copy.deepcopy(elementMoleFractions_right)
	
	oc.setElementMolarFraction(elementMoleFractions)

	#call tqce(' ',-1,0,zero,gpp(gp)%eqp)
	oc.calculateEquilibrium(gmStat.Off)
	mu=oc.getChemicalPotentials()
	for comp_ in comp:
		gpp_mu_value_new[comp_] = mu[comp_]/8.31451/1073
		gpp_xval_value_new[comp_] =elementMoleFractions[comp_]
	x = {i:gpp_mu_value_new}
	y = copy.deepcopy(x)
	gpp_mu.update(y)
	#gpp(gp)%xval(iel)=xval(iel)

	x = {i:gpp_xval_value_new}
	y = copy.deepcopy(x)
	gpp_xval.update(y)
	#gpp(gp)%xval(iel)=xval(iel)

nt = 0
nrow = 1
dx = []
dx.append(0.0)
dx.append(0.0)
dx.append(0.0)

# to run GUI event loop
plt.ion()

# here we are creating sub plots
#figure, ax = plt.subplots(figsize=(10, 8))
figure, (ax1,ax2) = plt.subplots(2,figsize=(8, 8))

line = {}
line1 = {}

for jj, comp_ in enumerate(comp):
	x_list = []
	y_list = []
	y_list1 = []
	for i in range(gpcur):
		x_list.append(i)

		y_list.append(gpp_xval[i][comp_])
		y_list1.append(gpp_mu[i][comp_])
	
	line[jj], = ax1.plot(x_list, y_list,'-o',markersize=3,label=comp_)
	line1[jj], = ax2.plot(x_list, y_list1,'-o',markersize=3,label=comp_)

# setting title
figure.suptitle("Diffusion simulation\nTime step: 0", fontsize=20)

figure.supxlabel("Grid point")
# setting x-axis label and y-axis label
#plt.xlabel("Grid point")
ax1.set_ylabel("Composition")
ax2.set_ylabel("Chemical potential/RT")

ax1.legend(loc="center right")
ax2.legend(loc="center right")
ax1.grid(True)
ax2.grid(True)

#plt.legend()

starttime = timeit.default_timer()

# simulate
ii = 1
while ii > 0:
	nt = nt + 1
	dxmax = 0.0

	gp1 = 0
	# start diff
	for i in range(gpcur-1):
		gp2 = gp1 + 1

		sumneg=0.0
		sumpos=0.0
		if (gp1==19):
			xxxx=0

		for jj, comp_ in enumerate(comp):
			dmu = gpp_mu[gp2][comp_] - gpp_mu[gp1][comp_]
			if abs(dmu) < 1e-14:
				dmu = 0.0
			dx[jj] = mobi[jj]*dmu

			# dxmax is used to check convergence, if max dxmax small then terminate
			if abs(dx[jj]) > dxmax:
				dxmax=abs(dx[jj])
			if dx[jj] > 0.0:
				sumpos=sumpos+dx[jj]
			else:
				sumneg=sumneg-dx[jj]

		# The sum of the fractions should always be unity, make the sum of all
		if sumpos <= 1.0e-12 or sumneg <=  1.0e-12:
		# There is no diffusion
			sdxp=0.0
			sdxn=0.0
		elif sumpos > sumneg:
		# scale the maximal flow to be the same as the minimal
			sdxp=sumneg/sumpos
			sdxn=1.0
		else:
			sdxp=1.0
			sdxn=sumpos/sumneg

		# move the atoms!!
		for jj, comp_ in enumerate(comp):
			if dx[jj] >= 0.0:
				gpp_xval[gp1][comp_] = gpp_xval[gp1][comp_] + dx[jj]*sdxp
				gpp_xval[gp2][comp_] = gpp_xval[gp2][comp_] - dx[jj]*sdxp
			else:
				gpp_xval[gp1][comp_] = gpp_xval[gp1][comp_] + dx[jj]*sdxn
				gpp_xval[gp2][comp_] = gpp_xval[gp2][comp_] - dx[jj]*sdxn

		# Check fractions are in range and sum is unity
		sum = 0.0
		for jj, comp_ in enumerate(comp):
			if gpp_xval[gp1][comp_] >= 1 or gpp_xval[gp1][comp_] <= 0.0:
				if gpp_xval[gp1][comp_] >= 1.0: gpp_xval[gp1][comp_] = 1.0-1.0e-8
				if gpp_xval[gp1][comp_] <= 0.0: gpp_xval[gp1][comp_] = 1.0e-8
			sum = sum + gpp_xval[gp1][comp_]
		if abs(sum-1.0) > 1.0e-7:
			print('Sum of fractions not unity at gridpoint ',gp1,sum)
			#print('Fractions: ', gpxval)
			print('Fractions: ',gpp_xval[gp1])
			exit()

		gp1 = gp1 + 1

	# end diff

	# modmod controls output
	# initially write each profile, then every 10, then every 100, then 1000
	if nt == 10:
		modmod = 10
	elif nt == 100:
		modmod = 100
	elif nt == 1000:
		modmod = 1000
	elif nt == 10000:
		modmod = 10000

	if modmod >  maxloop:
		modmod = maxloop
	# if nt % modmod == 0:
	# 	if plut > 0:
	# 		modmod=2*modmod
	# 		nrow=nrow+1
	# 		print('nt, nrow',nt,nrow)
	# 		print('Done ',nt,' timesteps')

	# start newx
	for i in range(gpcur):
		#print('current time step and grid point: ',str(nt),str(i))

		elementMoleFractions = gpp_xval[i]

		oc.setElementMolarFraction(elementMoleFractions)

		oc.calculateEquilibrium(gmStat.Off)
		#oc.listEqResults_lr1()
		
		mu=oc.getChemicalPotentials()
		for comp_ in comp:
			gpp_mu_value_new[comp_] = mu[comp_]/8.31451/1073
			if abs(mu[comp_]/8.31451/1073) < 1e-10:
				os.system("pause")

		x = {i:gpp_mu_value_new}
		y = copy.deepcopy(x)
		gpp_mu.update(y)

	# updating data values
	if nt%100 == 0:
		for jj, comp_ in enumerate(comp):
		
			x_list = []
			y_list = []
			y_list1 = []

			for i in range(gpcur):
				x_list.append(i)
				y_list.append(gpp_xval[i][comp_])
				y_list1.append(gpp_mu[i][comp_])

			line[jj].set_xdata(x_list)
			line[jj].set_ydata(y_list)
			line1[jj].set_xdata(x_list)
			line1[jj].set_ydata(y_list1)

		figure.suptitle("Diffusion simulation\nTime step: "+str(nt), fontsize=20)

		# drawing updated values
		figure.canvas.draw()

		# This will run the GUI event
		# loop until all UI events
		# currently waiting have been processed
		figure.canvas.flush_events()

	if nt % 1000 == 0:
		print("The time for performing SingleEquilibriumCalculation is :", "{0:.3f}".format(timeit.default_timer() - starttime), '[s]')

# loop back until simulation timestep exceeded or no change in composition
	if abs(dxmax) < 1.0e-5 or  nt > maxloop-1:
		os.system("pause")
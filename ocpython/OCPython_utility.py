"""
This is the auxiliary part of OC-Python (under development)

author: Chunhui Luo, 2022
"""

import copy
from math import ceil
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib import interactive

class OCPython_utility(object):

	def __init__(self):
		pass

	@staticmethod
	def comp_new_order(elements):
		"""
		get component associated result
		
		To pass array of strings to Fortran in Python, one must create an array of chars with shape (<number of strings>, <string length>), fill its content, and then pass the char array to f2py generated function.
		
		Here xstring is used for this purpose. The input is element list, the output is numpy string array, which is dedicated for use in reading tdb withe element names. 

		Parameters
		----------
		param1
			elements

		Returns
		-------
		numpy string array
			names of components
		"""
		sorted_elements = copy.deepcopy(elements)
		sorted_elements.sort()

		elements_new = []
		for el in elements:
			if len(el) < 2:
				elements_new.append(el+' ')
			else:
				elements_new.append(el)
		elements = elements_new

		nobstot = len(elements)
		xstring = np.empty((nobstot, 2), dtype='c')
		for i in range(nobstot):
			k = ceil((i+1)/2)-1
			l = i%2	#remainder
			if nobstot%2==0:	#even number
				m = ceil((nobstot+1)/2)-1+ceil((i+1)/2)-1
				n = i%2
			else:	#odd number
				m = ceil((nobstot+1)/2)-1+ceil((i)/2)
				n = i%2+1
				if n==2:
					n=0
			xstring[i] = elements[k][l]+elements[m][n]

		return xstring

	@staticmethod
	def phase_parsing_bytes_string(nPhase,phasename_bytes):
		"""
		get component associated result
		
		To pass array of strings to Fortran in Python, one must create an array of chars with shape (<number of strings>, <string length>), fill its content, and then pass the char array to f2py generated function.
		
		Here xstring is used for this purpose. The input is element list, the output is numpy string array, which is dedicated for use in reading tdb withe element names. 

		Parameters
		----------
		param1
			elements

		Returns
		-------
		numpy string array
			names of components
		"""
		a = np.char.decode(phasename_bytes)

		nn = 20
		phase_list = []
		for i in range(nPhase):
			el = a[nn*(i+1)-nn:nn*(i+1)]
			el_ = ''.join(el)
			if len(el_) > 0:
				phase_list.append(el_.strip())
			else:
				break
		return phase_list

	@staticmethod
	def getcomp(n,comp):
		"""
		get component list

		Convert string array from Fortran -> component string list in Python

		Parameters
		----------
		param1
			n
		param2
			comp

		Returns
		-------
		list
			names of components
		"""
		a = np.char.decode(comp)
		new_comp = []
		for i in range(n):
			el = a[2*(i+1)-2]+a[2*(i+1)-1]
			new_comp.append(el.strip())
		return new_comp

	@staticmethod
	def getPhaseFraction(oc):
		"""
		get phase fraction (only non-zero values)

		Parameters
		----------
		param1
			oc

		Returns
		-------
		list
			phase fraction
		"""
		phasefraction_ = oc.getValuePhase('NPM')
		phasefraction = dict((k, v) for k, v in phasefraction_.items() if v > 0.0)
		return phasefraction

	@staticmethod
	def getStablePhase(oc):
		"""
		get stable phases and its fractions ((i.e. the phases present in the current equilibrium))
		"""
		phase_dict = oc.getValuePhase('NP')

		return {k:v for k,v in phase_dict.items() if v>0.0}

	@staticmethod
	def plotContour(x_list, y_list, result_list, xlabel, ylabel, title):
		"""
		Plot a contour.

		Parameters
		----------
		param1
			x_list: data for the x-axis
		param2
			y_list: data for the y-axis
		param3
			result_list: data for the z-axis
		param4
			xlabel: label for the x-axis
		param5
			ylabel: label for the y-axis
		param6
			title: title of the figure
		"""
		plt.rcParams["figure.figsize"] = [8.50, 5.50]
		plt.rcParams["figure.autolayout"] = True
		fig = plt.figure()
		try:
			fig.canvas.manager.window.move(100,200)
		except:
			pass
		ax = plt.axes()
		zz = np.empty([len(y_list), len(x_list)])
		k = 0
		for ix, x in enumerate(x_list):
			for iy, y in enumerate(y_list):
				zz[iy, ix] = result_list[k]
				k = k + 1
		xx, yy = np.meshgrid(x_list, y_list)

		cp = plt.contourf(xx, yy, zz)
		plt.colorbar(cp)

		ax.set_xlabel(xlabel,fontsize=12)
		ax.set_ylabel(ylabel,fontsize=12)
	
		ax.set_title(title,fontsize=14, fontweight='bold')
		interactive(True)
		plt.show()
	
	@staticmethod
	def plot3D(x_list, y_list, result_list, xlabel, ylabel, zlabel, title):
		"""
		Plot a 3D surface.

		Parameters
		----------
		param1
			x_list: data for the x-axis
		param2
			y_list: data for the y-axis
		param3
			result_list: data for the z-axis
		param4
			xlabel: label for the x-axis
		param5
			ylabel: label for the y-axis
		param6
			zlabel: label for the z-axis
		param7
			title: title of the figure
		"""
		plt.rcParams["figure.figsize"] = [8.50, 5.50]
		plt.rcParams["figure.autolayout"] = True
		fig = plt.figure()
		try:
			fig.canvas.manager.window.move(960,200)
		except:
			pass
		ax = plt.axes(projection='3d')
		zz = np.empty([len(y_list), len(x_list)])
		k = 0
		for ix, x in enumerate(x_list):
			for iy, y in enumerate(y_list):
				zz[iy, ix] = result_list[k]
				k = k + 1
		xx, yy = np.meshgrid(x_list, y_list)
		surf3D = ax.plot_surface(xx, yy, zz, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
		ax.set_xlabel(xlabel,fontsize=12)
		ax.set_ylabel(ylabel,fontsize=12)
		ax.set_zlabel(zlabel,fontsize=12,labelpad=20)
	
		ax.zaxis.set_major_formatter(FormatStrFormatter('%.2e'))
		ax.zaxis.set_tick_params(pad=10)

		ax.set_title(title,fontsize=14, fontweight='bold')
		fig.colorbar(surf3D, location = 'left', format='%.2e')
		interactive(False)
		plt.show()

	@staticmethod
	def calc_phasefrac_temploop_nonewphase(oc,gmStat,T_list,stateVar):
		"""
		Calculate phase fraction with temperature loop (don't allow new phase creation)

		Parameters
		----------
		param1
			oc
		param1
			gmStat
		param1
			T_list

		Returns
		-------
		dict
			values_dict
		list
			T_K
		"""
		print('total loops for setting temperature and preforming calculate equilibrium are:', len(T_list))

		Eq_str = []
		T_K = []
		nPhase = oc.getNumberPhase()
		phases_list = []
		for index in range(nPhase):
			phases_list.append(oc.getPhaseName(index))

		k=0
		for i,T in enumerate(T_list):
			oc.setTemperature(T)
			Eq_str.append('eq_'+str(T))
			oc.setquiet
			oc.calculateEquilibrium(gmStat.Off)
			error =  oc.getErrorCode()
			if not error == 0:
				oc.resetErrorCode()
			T_K.append(T)

			value_calc = oc.getValuePhase(stateVar)

			if i==0:
				values_dict = value_calc
				nph = len(value_calc)
				for key,value in values_dict.items():
					values_dict[key] = np.array([value])

			else:
				for key,value in values_dict.items():
					try:
						values_dict[key] = np.append(value, value_calc[key])
					except KeyError: # in value_calc[key]
						pass
						#values_dict[key] = np.append(value, 0.0)

		return values_dict, T_K

	@staticmethod
	def calc_phasefrac_temploop_newphase(oc,gmStat,T_list,stateVar):
		"""
		Calculate phase fraction with temperature loop (allow new phase creation from FCC_A1)

		Parameters
		----------
		param1
			oc
		param1
			gmStat
		param1
			T_list

		Returns
		-------
		dict
			values_dict
		list
			T_K,C_comp_in_FCC_A1
		"""
		print('total loops for setting temperature and preforming calculate equilibrium are:', len(T_list))

		Eq_str = []
		T_K = []
		nPhase = oc.getNumberPhase()
		phases_list = []
		for index in range(nPhase):
			phases_list.append(oc.getPhaseName(index))

		k=0
		phase_delete = []
		phase_diff = []
		C_comp_in_FCC_A1 = []
		for i,T in enumerate(T_list):
			oc.setTemperature(T)
			Eq_str.append('eq_'+str(T))
			#oc.changeEquilibriumRecord('eq_'+str(T))
			oc.setquiet
			oc.calculateEquilibrium(gmStat.On)
			error =  oc.getErrorCode()
			if not error == 0:
				oc.resetErrorCode()
			T_K.append(T)

			value_calc = oc.getValuePhase(stateVar)

			if i==0:
				values_dict = value_calc
				nph = len(value_calc)
				for key,value in values_dict.items():
					values_dict[key] = np.array([value])

				phaseElementComposition = oc.getPhaseElementComposition()
				try:
					C0 = phaseElementComposition['FCC_A1']['C']
				except KeyError:
					C0 = 0.0
				C_comp_in_FCC_A1.append(C0)

			else:
				if nPhase == len(value_calc):
					for key,value in values_dict.items():
						try:
							values_dict[key] = np.append(value, value_calc[key])
						except KeyError: # in value_calc[key]
							pass
							#values_dict[key] = np.append(value, 0.0)

					phaseElementComposition = oc.getPhaseElementComposition()
					try:
						C0 = phaseElementComposition['FCC_A1']['C']
					except KeyError:
						C0 = 0.0
					C_comp_in_FCC_A1.append(C0)

				else:   # new phase is created
					keys_list = list(value_calc.keys())
					phase_diff = list(set(phases_list) ^ set(keys_list))
					phase_diff1 = list(set(phases_list) & set(phase_diff))
					if not phase_diff1[0] in phase_delete:
						phase_delete.append(phase_diff1[0])
					#print('phase_delete',phase_delete)

					phase_diff2 = list(set(keys_list) & set(phase_diff))
					for key_ in phase_diff2:
						if not key_ in values_dict:
							try:
								x =  values_dict[key_]
							except:
								# first time to add new phase
								if not 'AUTO' in key_:
									values_dict[key_] = values_dict[phase_diff1[0]]
									k =  k + 1
								else:
									values_dict[key_] = np.zeros(len(values_dict[phase_diff1[0]]))
		
					phaseElementComposition = oc.getPhaseElementComposition()

					try:
						C1 = phaseElementComposition['FCC_A1#1']['C']
					except KeyError:
						C1 = 0.0

					try:
						C2 = phaseElementComposition['FCC_A1_AUTO#2']['C']
					except KeyError:
						C2 = 0.0

					C_comp_in_FCC_A1.append(0.0)

					for key,value in values_dict.items():
						try:
							values_dict[key] = np.append(value, value_calc[key])
						except KeyError:
							pass

					if C1>C2 and C1>0.0 and C2>0.0:
						frac1 = value_calc['FCC_A1#1']
						frac2 = value_calc['FCC_A1_AUTO#2']
						f1 = values_dict['FCC_A1#1']
						f1[-1] = frac2
						f2 = values_dict['FCC_A1_AUTO#2']
						f2[-1] = frac1
						values_dict['FCC_A1#1'] = f1
						values_dict['FCC_A1_AUTO#2'] = f2

					if  C1==0.0 and C2>0.0:
						frac1 = value_calc['FCC_A1#1']
						frac2 = value_calc['FCC_A1_AUTO#2']
						f1 = values_dict['FCC_A1#1']
						f1[-1] = frac2
						f2 = values_dict['FCC_A1_AUTO#2']
						f2[-1] = frac1
						values_dict['FCC_A1#1'] = f1
						values_dict['FCC_A1_AUTO#2'] = f2

					if  C2==0.0 and C1>0.0:
						frac1 = value_calc['FCC_A1#1']
						frac2 = value_calc['FCC_A1_AUTO#2']
						f1 = values_dict['FCC_A1#1']
						#f1[-1] = frac2
						f2 = values_dict['FCC_A1_AUTO#2']
						#f2[-1] = frac1
		try:
			try:
				for phase_key in phase_delete:
					del values_dict[phase_key]
			except:
				pass
		except KeyError:
			pass

		return values_dict, T_K,C_comp_in_FCC_A1
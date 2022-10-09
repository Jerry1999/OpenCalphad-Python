"""
This is the main part of OC-Python (under development)

Notes:
1) It must be used together with the library (liboctq_f90wrap.cp38-win_amd64.pyd or liboctq_f90wrap.cp39-win_amd64.pyd)
2) The partial codes are based on the code from OpenCalphad GitHub (https://github.com/sundmanbo/opencalphad/tree/master/OCisoCbinding)

author: Chunhui Luo, 2022
"""

import logging, sys, os, copy
import datetime
import json
import numpy as np

try:
	from ocpython import liboctq_f90wrap as oc
except:
	import liboctq_f90wrap as oc
try:
	from ocpython.OCPython_utility import OCPython_utility
except:
	from OCPython_utility import OCPython_utility

from enum import IntEnum
from typing import List

class Verbosity(object):
	"""
	class: Verbosity
	"""

	def __init__(self,newlogfile,process_name):
		self.logger = logging.getLogger(process_name)
		self.logger.setLevel(logging.INFO)
		ch = logging.StreamHandler()
		ch.setStream(sys.stderr)
		ch.setLevel(logging.INFO)
		formatter = logging.Formatter('(%(name)s): %(message)s')
		ch.setFormatter(formatter)
		self.logger.addHandler(ch)

		if newlogfile:
			logfilepath = os.path.abspath(os.path.dirname(__file__))
			logfilepath = os.path.join(logfilepath,'OC_python.log')
			try:
				if os.path.isfile(logfilepath):
					os.remove(logfilepath)
			except:
				pass
		self.logger.addHandler(logging.FileHandler(filename='OC_python.log'))
		#self.logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	def setVerbosity(self, isVerbose):
		"""
		set Verbosity: True or False.\n
		If Verbosity is True, logging level is set as DEBUG and more detailed information is shown.\n
		If Verbosity is False, logging level is set as INFO and less information is shown.
		"""
		if (isVerbose):
			level= logging.DEBUG
		else:
			level = logging.INFO
		self.logger.setLevel(level)
		for handler in self.logger.handlers:
			handler.setLevel(level)
		if (isVerbose):
			oc.f90wrap_pytqquiet(True)

class PhaseStatus(IntEnum):
	"""
	class: Set phase status (Suspended, Dormant, Entered, Fixed)
	"""
	Suspended = -3
	Dormant   = -2
	Entered   =  0
	Fixed	  =  2

class GridMinimizerStatus(IntEnum):
	"""
	class: set GridMinimizerStatus (On or Off)
	"""
	On  = 0
	Off = -1

class MassUnit(IntEnum):
	"""
	class: set mass unit
	"""
	MoleFraction = 1
	MassFraction = 2

class GetResults(object):
	"""
	class: get results
	"""
	def __init__(self,self_):

		self.eq = self_.eq
		self.logger = self_.logger
		self.comp = self_.components
		try:
			self.constituentsDescription = self_.constituentsDescription
		except:
			pass

	def getScalarResult(self,symbol:str):
		"""
		get scalar result

		Parameters
		----------
		param1
			symbol

		Returns
		-------
		value
			calculated property
		"""
		value=np.empty(1)
		oc.f90wrap_pytqgetv(symbol,0,0,1,value,self.eq)
		#self.logger.debug('retrieve: %s: %e',symbol,value[0])
		return value[0]

	def getComponentAssociatedResult(self, symbol:str):
		"""
		get component associated result

		Parameters
		----------
		param1
			symbol

		Returns
		-------
		dict
			calculated property
		"""
		values={}
		value=np.empty(1)

		for i in range(len(self.comp)):
			oc.f90wrap_pytqgetv(symbol,i+1,0,1,value,self.eq)
			#values[self.__componentNames[i]] = value[0]
			values[self.comp[i]] = value[0]
		#self.logger.debug('retrieve: %s:\n%s',symbol,json.dumps(values, indent=4))
		return values	

	def getPhaseAssociatedResult(self, symbol:str):
		"""
		get phase associated result

		Parameters
		----------
		param1
			symbol

		Returns
		-------
		dict
			calculated property
		"""
		values={}
		value=np.empty(1)
		tmpNPhases=np.empty(SingleEquilibriumCalculation._maxNPhase)
		nPhases=oc.f90wrap_pytqgetv('NP',-1,0,SingleEquilibriumCalculation._maxNPhase,tmpNPhases,self.eq)

		for i in range(nPhases):
			oc.f90wrap_pytqgetv(symbol,i+1,0,1,value,self.eq)
			phaseName=oc.f90wrap_pytqgpn(i+1,self.eq).decode().strip()
			values[phaseName] = value[0]
		self.logger.debug('retrieve: %s:\n%s',symbol,json.dumps(values, indent=4))
		return values

	def getPhaseElementComposition(self):
		"""
		get phase element composition

		Returns
		-------
		dict
			phase element composition
		"""
		tmpNPhases=np.empty(SingleEquilibriumCalculation._maxNPhase)
		tmpNElements=np.empty(SingleEquilibriumCalculation._maxNElement)
		nPhases=oc.f90wrap_pytqgetv('NP',-1,0,SingleEquilibriumCalculation._maxNPhase,tmpNPhases,self.eq)
	
		phaseElementComposition={}
		for i in range(nPhases):
			if (tmpNPhases[i]>0.0):
				phaseName=oc.f90wrap_pytqgpn(i+1,self.eq).decode().strip()
				phaseElementComposition[phaseName] = {}
				nElements=oc.f90wrap_pytqgetv('X',i+1,-1,SingleEquilibriumCalculation._maxNElement,tmpNElements,self.eq)
				for j in range(nElements):
					phaseElementComposition[phaseName][self.comp[j]]=tmpNElements[j]
		self.logger.debug('Phase element composition:\n'+json.dumps(phaseElementComposition, indent=4))
		return phaseElementComposition

	def getPhaseSites(self):
		"""
		get phase sites

		Returns
		-------
		dict
			phase sites
		"""
		tmpNPhases=np.empty(SingleEquilibriumCalculation._maxNPhase)
		tmpiNSublattices=np.empty(SingleEquilibriumCalculation._maxNSublattice, dtype=np.int32)
		tmpNSublattices=np.empty(SingleEquilibriumCalculation._maxNSublattice)
		tmpiNConstituents=np.empty(SingleEquilibriumCalculation._maxNSublattice*SingleEquilibriumCalculation._maxNConstituent, dtype=np.int32)
		tmpNConstituents=np.empty(SingleEquilibriumCalculation._maxNSublattice*SingleEquilibriumCalculation._maxNConstituent)
		tmp5=np.empty(5)
	
		nbPhases=oc.f90wrap_pytqgetv('NP',-1,0,SingleEquilibriumCalculation._maxNPhase,tmpNPhases,self.eq)
		phaseSites={}
		for i in range(nbPhases):
			if (tmpNPhases[i]>0.0):
				phaseName=oc.f90wrap_pytqgpn(i+1,self.eq).decode().strip()
				phaseName=oc.f90wrap_pytqgpn(i+1,self.eq).decode().strip()
				nbSublattices = oc.f90wrap_pytqgphc1(i+1, tmpiNSublattices, tmpiNConstituents, tmpNConstituents, tmpNSublattices, tmp5, self.eq)
				phaseSites[phaseName] = tmpNSublattices[0:nbSublattices].tolist()
		self.logger.debug('Phase sites:\n'+json.dumps(phaseSites, indent=4))
		return phaseSites

	def getPhaseConstituentComposition(self):
		"""
		get phase constituent composition

		Returns
		-------
		dict
			phase constituent composition
		"""
		tmpNPhases = np.empty(SingleEquilibriumCalculation._maxNPhase)
		tmpNElements = np.empty(SingleEquilibriumCalculation._maxNElement)
		tmpiNElements = np.empty(SingleEquilibriumCalculation._maxNElement, dtype=np.int32)
		tmpiNSublattices = np.empty(SingleEquilibriumCalculation._maxNSublattice, dtype=np.int32)
		tmpNSublattices = np.empty(SingleEquilibriumCalculation._maxNSublattice)
		tmpiNConstituents = np.empty(SingleEquilibriumCalculation._maxNSublattice*SingleEquilibriumCalculation._maxNConstituent, dtype=np.int32)
		tmpNConstituents = np.empty(SingleEquilibriumCalculation._maxNSublattice*SingleEquilibriumCalculation._maxNConstituent)
		tmp5=np.empty(5)
	
		nbPhases=oc.f90wrap_pytqgetv('NP',-1,0,SingleEquilibriumCalculation._maxNPhase,tmpNPhases,self.eq)
		phaseConstituentComposition={}
		for i in range(nbPhases):
			if (tmpNPhases[i]>0.0):
	
				phaseName=oc.f90wrap_pytqgpn(i+1,self.eq).decode().strip()
				iph, ics = oc.f90wrap_pytqgpi2(phaseName,self.eq)
	
				phaseConstituentComposition[phaseName]={}
				phaseName=oc.f90wrap_pytqgpn(i+1,self.eq).decode().strip()
				nbSublattices = oc.f90wrap_pytqgphc1(i+1, tmpiNSublattices, tmpiNConstituents, tmpNConstituents, tmpNSublattices, tmp5, self.eq)
				count = 0
				for j in range(nbSublattices):
					sublatticeConstituentComposition = {}
					offset = count
					for k in np.nditer(tmpiNConstituents[offset:offset+tmpiNSublattices[j]]):
						constituentName = oc.f90wrap_pytqgpcn2(iph,count+1).decode().strip()
						sublatticeConstituentComposition[constituentName] = tmpNConstituents[count]
						if not constituentName in self.constituentsDescription:
							nspel, smass, qsp = oc.f90wrap_pytqgpcs(k, tmpiNElements, tmpNElements)
							self.constituentsDescription[constituentName] = {}
							self.constituentsDescription[constituentName]['mass'] = smass
							self.constituentsDescription[constituentName]['charge'] = qsp
							self.constituentsDescription[constituentName]['elements'] = { self.comp[tmpiNElements[l]-1] : tmpNElements[l] for l in range(nspel) if (tmpiNElements[l]>0)}
						count += 1
					if (nbSublattices==1):
						phaseConstituentComposition[phaseName] = sublatticeConstituentComposition
					else:
						phaseConstituentComposition[phaseName]["sublattice {0:d}".format(j)] = sublatticeConstituentComposition
		self.logger.debug('Pase constituent composition:\n'+json.dumps(phaseConstituentComposition, indent=4))
		return phaseConstituentComposition

class SingleEquilibriumCalculation(object):
	"""
	Single Equilibrium Calculation
	"""
	_defaultEquilibriumName='default equilibrium'
	_maxNPhase=200
	_maxNElement=50
	_maxNSublattice=10
	_maxNConstituent=50

	def __init__(self,vs):
		"""
		initiate for Single Equilibrium Calculation
		"""
		self.equilibriumNamesInOC = {}
		self.constituentsDescription = {}
		self.logger = vs.logger

	def eq(self):
		"""
		return self.eq
		"""
		return self.eq

	def readtdb(self,tdbFilePath:str, elements=None):
		"""
		read database

		Parameters
		----------
		param1
			tdbFilePath
		param2
			element
		"""
		# set init
		self.eq = oc.f90wrap_pytqini(1)

		if self.logger.getEffectiveLevel() is not logging.DEBUG:
			oc.f90wrap_pytqquiet(True)
		self.eqName = SingleEquilibriumCalculation._defaultEquilibriumName
		eqNameInOC='%s' % self.eqName.upper().replace(' ','_')
		self.equilibriumNamesInOC[self.eqName]=eqNameInOC
		self.logger.debug('read database: %s', tdbFilePath)

		# read tdb
		if elements is None:
			oc.f90wrap_pytqrfil(tdbFilePath,self.eq)
		else:
			xstring = OCPython_utility.comp_new_order(elements)
			oc.f90wrap_pytqrpfil(tdbFilePath,len(elements),xstring,self.eq)

		# string array from Fortran -> component list in Python
		try:
			n,comp_ = oc.f90wrap_pytqgcom(self.eq)
			components = OCPython_utility.getcomp(n,comp_)
			self.components = components
			self.logger.debug('component (%d) names: %s', len(components), components)
		except:
			self.components = ''
			self.logger.debug('component (%d) names: %s', len(components), components)

	def getComponentNames(self) -> List[str]:
		"""
		Returns the ordered name list of the imported components after reading database.

		Returns
		-------
		list
			names of components
		"""
		return self.components

	def getNumberPhase(self):
		"""
		get total number of phases

		Returns
		-------
		int
			number of phases
		"""

		nPhase = oc.f90wrap_pytqgnp(self.eq)
		self.logger.debug('number of phases: %d',nPhase)

		return nPhase

	def getPhaseName(self, index:int):
		"""
		get name of phase from index

		Parameters
		----------
		param1
			index

		Returns
		-------
		string
			phase name
		"""

		phaseName=oc.f90wrap_pytqgpn(index+1,self.eq).decode().strip()

		return phaseName

	def singleEquilibriumCalculation_Compact(self,tdbFilePath,elements,massunit,tpn,elementFractions,phaseNames=None,elementReferencePhase=None):
		"""
		Single Equilibrium Calculation with compact mode

		Parameters
		----------
		param1
			tdbFilePath 
		param2
			elements
		param3
			tpn 
		param4
			elementMoleFractions
		param5
		   phaseNames
		param6
		   elementReferencePhase
		"""
		if len(elements) > len(elementFractions):
			pass

		self.eq = oc.f90wrap_pytqini(1)
		if self.logger.getEffectiveLevel() is not logging.DEBUG:
			oc.f90wrap_pytqquiet(True)
		self.eqName = SingleEquilibriumCalculation._defaultEquilibriumName
		eqNameInOC='%s' % self.eqName.upper().replace(' ','_')
		self.equilibriumNamesInOC[self.eqName]=eqNameInOC
		self.logger.debug('reading %s', tdbFilePath)

		# create xstring
		sorted_elements = copy.deepcopy(elements)
		sorted_elements.sort()
		xstring = OCPython_utility.comp_new_order(elements)

		i = 0
		index_list = []
		fraction_list = []
		for el_name, value in elementFractions.items():
			i = i + 1
			i=sorted_elements.index(el_name)
			index_list.append(i+1)
			fraction_list.append(value)

		tpn_list = []
		for name, value in tpn.items():
			tpn_list.append(value)

		if phaseNames is None:
			phaseList=''
		else:
			phaseList=';'.join([str(elem) for elem in phaseNames])

		if elementReferencePhase is None:
			elRef=''
			phRef=''
		else:
			elRef_list = list(elementReferencePhase.keys())
			phRef_list = list(elementReferencePhase.values())

			elRef=';'.join([str(elem) for elem in elRef_list])
			phRef=';'.join([str(phase) for phase in phRef_list])

		# call fortran subroutine for single equilibrium calculation in compact mode
		oc.f90wrap_pytqcecompact(tdbFilePath,len(elements),massunit,xstring,tpn_list,index_list,fraction_list,phaseList,elRef,phRef,self.eq)

		try:
			n,comp = oc.f90wrap_pytqgcom(self.eq)
			a = np.char.decode(comp)
			components = []
			for i in range(n):
				el = a[2*(i+1)-2]+a[2*(i+1)-1]
				components.append(el.strip())
			self.components = components
			self.logger.debug('component (%d) names: %s', len(components), components)
		except:
			pass

	def batchEquilibriaComp(self, n_xfrac,elementMoleFractions,xfrac_matrix,temp,stavar):
		"""
		Batch equilibrium calculations with composition loops

		Parameters
		----------
		param1
			n_xfrac: 
		param2
			elementMoleFractions
		param3
			xfrac_matrix: 
		param4
			temp
		param5
		   stavar

		Returns
		-------
		list
			calculated properties
		"""
		elements  = list(elementMoleFractions.keys())
		elements.sort()
		number_element = len(elements)

		# call fortran subroutine for single equilibrium calculation in compact mode
		i = 0
		index_list = []
		xeq = xfrac_matrix
		for el_name, value in elementMoleFractions.items():
			i = i + 1
			i=elements.index(el_name)
			index_list.append(i+1)

		values=np.empty(n_xfrac)

		oc.f90wrap_pytqcompbatch(number_element,n_xfrac,index_list,xeq,temp,stavar,values,self.eq)
		return values

	def batchEquilibriaTemp(self,elementMoleFractions,xfrac_matrix,temp_list,stavar):
		"""
		Batch equilibrium calculations with temperature loops

		Parameters
		----------
		param1
			elementMoleFractions
		param2
			xfrac_matrix: 
		param3
			temp_list
		param4
		   stavar

		Returns
		-------
		list
			calculated properties
		"""
		elements = list(elementMoleFractions.keys())
		elements.sort()
		n_element = len(elements)

		# call fortran subroutine for single equilibrium calculation in compact mode
		i = 0
		index_list = []
		for el_name, value in elementMoleFractions.items():
			i = i + 1
			i=elements.index(el_name)
			index_list.append(i+1)

		n_temp = len(temp_list)
		values = np.empty(n_temp)
	
		oc.f90wrap_pytqtempbatch(n_element,n_temp,index_list,xfrac_matrix,temp_list,stavar,values,self.eq)
		return values

	def setElementMolarFraction(self,elementMoleFractions:dict):
		"""
		set element molar fraction
	
		Parameters
		----------
		param1
			elementMoleFractions
		"""
		ii = 0
		for el, v in elementMoleFractions.items():
			ii = ii + 1
			if len(elementMoleFractions)==1 or ii<len(elementMoleFractions):
				i=self.components.index(el)
				self.logger.debug('set molar fraction %5.4f for element %s (%d)',v,el,i)
				oc.f90wrap_pytqsetc('X',i+1,0,v,self.eq)

	def setSingleElementMolarFraction(self,index,xfrac):
		"""
		set single element molar fraction
	
		Parameters
		----------
		param1
			index
		param2
			xfrac
		"""
		oc.f90wrap_pytqsetc('X',index+1,0,xfrac,self.eq)
		self.logger.debug('set mass amount %5.4f for element index (%d)',xfrac,index)

	def setElementMassFraction(self,elementMassFractions):
		"""
		set element mass fraction
	
		Parameters
		----------
		param1
			elementMoleFractions
		"""
		ii = 0
		for el, n in elementMassFractions.items():
			ii = ii + 1
			if ii<len(elementMassFractions):
				i=self.components.index(el)
				self.logger.debug('set molar amount %5.4f for element %s (%d)',n,el,i)
				oc.f90wrap_pytqsetc('W',i+1,0,n,self.eq)

	def setSingleElementMassFraction(self,index,wfrac):
		"""
		set single element mass fraction
	
		Parameters
		----------
		param1
			index
		param2
			wfrac
		"""
		oc.f90wrap_pytqsetc('W',index+1,0,wfrac,self.eq)
		self.logger.debug('set mass amount %5.4f for element index (%d)',wfrac,index)

	def setPhasesStatus(self, phaseNames, phaseStatus, phaseAmount=0.0):
		"""
		set phase status
	
		Parameters
		----------
		param1
			phaseNames
		param2
			phaseStatus
		param3
			phaseAmount
		"""
		phaseList=';'.join([str(elem) for elem in phaseNames])
		phaseList1 = phaseList 	
		if '*' in phaseList:
			phaseList1 = 'All phases'

		self.logger.debug('change phases status: %s to %s', phaseList1, phaseStatus)
		oc.f90wrap_pytqphsts2(phaseList,phaseStatus,phaseAmount,self.eq)

	def getPhasesStatus(self, nPhase):
		"""
		set phase status
	
		Parameters
		----------
		param1
			phaseNames
		param2
			phaseStatus
		param3
			phaseAmount
		"""
		status = np.zeros((nPhase,), dtype=int)
		amdgm = np.zeros(nPhase)
		phasename_bytes = oc.f90wrap_pytqgpsm(nPhase,status,amdgm,self.eq)

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

		return phase_list,status,amdgm

	def setTemperature(self,temperature:float=None):
		"""
		set temperature

		Parameters
		----------
		param1
			temperature
		"""
		self.logger.debug('set temperature to %5.2f K', temperature)
		if not temperature==None:
			oc.f90wrap_pytqsetc('T',0,0,temperature,self.eq)
		else:
			oc.f90wrap_pytqsetc('T',0,-1,0,self.eq)

	def setPressure(self,pressure:float):
		"""
		set pressure

		Parameters
		----------
		param1
			pressure
		"""
		self.logger.debug('set pressure to %3.2e Pa', pressure)
		oc.f90wrap_pytqsetc('P',0,0,pressure,self.eq)

	def setTotalMolarAmount(self,n:float):
		"""
		set total molar amount

		Parameters
		----------
		param1
			n
		"""
		oc.f90wrap_pytqsetc('N',0,0,n,self.eq)
		self.logger.debug('set total molar amount %5.2f ',n)

	def getScalarResult(self,symbol:str):
		"""
		get scalar result

		Parameters
		----------
		param1
			symbol

		Returns
		-------
		Value
			calculated property
		"""
		x = GetResults(self)
		y = x.getScalarResult(symbol)
		return y

	def getGibbsEnergy(self):
		"""
		get Gibbs energy

		Returns
		-------
		value
			Gibbs energy
		"""
		x = GetResults(self)
		y = x.getScalarResult('G')
		return y

	def getChemicalPotentials(self):
		"""
		get chemical potentials

		Returns
		-------
		dict
			chemical potential
		"""
		x = GetResults(self)
		y = x.getComponentAssociatedResult('MU')
		return y

	def getValueComponent(self,symbol:str):
		"""
		get component associated result

		Parameters
		----------
		param1
			symbol

		Returns
		-------
		dict
			calculated property
		"""

		x = GetResults(self)
		y = x.getComponentAssociatedResult(symbol)
		return y

	def getValuePhase(self,symbol:str):
		"""
		get phase associated result

		Parameters
		----------
		param1
			symbol

		Returns
		-------
		dict
			calculated property
		"""
		x = GetResults(self)
		y = x.getPhaseAssociatedResult(symbol)
		return y

	def getConstituentsDescription(self):
		"""
		get constituents description

		Returns
		-------
		dict
			constituents description
		"""
		self.logger.debug('constituents description:\n'+json.dumps(self.constituentsDescription, indent=4))
		return self.constituentsDescription

	def calculateEquilibrium(self,gridMinimizerStatus=GridMinimizerStatus.On):
		"""
		calculate equilibrium

		Parameters
		----------
		param1
			gridMinimizerStatus
		"""
		self.logger.debug('calculate equilibrium with grid minimizer: %s', gridMinimizerStatus)
		if (self.logger.isEnabledFor(level=logging.DEBUG)):
			oc.f90wrap_pytqlc(6,self.eq)
		oc.f90wrap_pytqce('',gridMinimizerStatus,0,0.0,self.eq)
		if (self.logger.isEnabledFor(level=logging.DEBUG)):
			oc.f90wrap_pytqlr(6,self.eq)

	def listConditions(self):
		"""
		show conditions for equilibrium calculation
		"""
		oc.f90wrap_pytqlc(6,self.eq)

	def listEqResults(self):
		"""
		show result for equilibrium calculation
		"""
		oc.f90wrap_pytqlr(6,self.eq)

	def listEqResults_lr1(self):
		"""
		show result for equilibrium calculation
		"""
		oc.f90wrap_pytqlr1(6,self.eq)

	def getPhaseElementComposition(self):
		"""
		get phase element composition

		Returns
		-------
		dict
			phase element composition
		"""
		x = GetResults(self)
		y = x.getPhaseElementComposition()
		return y

	def getPhaseSites(self):
		"""
		get phase sites

		Returns
		-------
		dict
			phase sites
		"""
		x = GetResults(self)
		y = x.getPhaseSites()
		return y

	def getPhaseConstituentComposition(self):
		"""
		get phase constituent composition

		Returns
		-------
		dict
			phase constituent composition
		"""
		x = GetResults(self)
		y = x.getPhaseConstituentComposition()
		return y

	def changeEquilibriumRecord(self,eqName=None,copiedEqName=None):
		"""
		change equilibrium record
		"""
		if eqName is None:
			eqName=SingleEquilibriumCalculation._defaultEquilibriumName
		if copiedEqName is None:
			copiedEqName=SingleEquilibriumCalculation._defaultEquilibriumName
		eqNameInOC=self.equilibriumNamesInOC.get(eqName,'')
		if (eqNameInOC==''):
			eqNameInOC='%s' % eqName.upper().replace(' ','_')
			self.equilibriumNamesInOC[eqName]=eqNameInOC
			eq=oc.f90wrap_pytqselceq(self.equilibriumNamesInOC[copiedEqName])
			self.logger.debug('create and select new equilibrium record: \'%s\' (\'%s\')', eqName, eqNameInOC)
			iCopiedEq,self.eq=oc.f90wrap_pytqcceq(eqNameInOC,eq)
		else:
			self.logger.debug('select equilibrium record: \'%s\' (\'%s\')', eqName, eqNameInOC)
			self.eq=oc.f90wrap_pytqselceq(eqNameInOC)
		self.eqName = eqName

	def deleteEquilibrium(self,eqName=None):
		"""
		delete equilibrium with name
		"""
		oc.f90wrap_pytqdceq(eqName)

	def getErrorCode(self):
		"""
		get error code
		"""
		return oc.f90wrap_pygeterr()

	def resetErrorCode(self):
		"""
		reset error code
		"""
		return oc.f90wrap_pyseterr(0)
	
	def setquiet():
		"""
		if argument TRUE spurious output should be suppressed
		"""
		oc.f90wrap_pytqquiet(True)
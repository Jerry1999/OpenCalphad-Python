Subroutines in Liboctq.f90
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function::   subroutine tqini(n,ceq)


   ! initiate workspace

       implicit none

       integer n ! Not nused, could be used for some initial allocation

       type(gtp_equilibrium_data), pointer :: ceq ! EXIT: current equilibrium


.. function::   subroutine tqrfil(filename,ceq)


   ! read all elements from a TDB file

       implicit none

       character*(*) filename  ! IN: database filename

       type(gtp_equilibrium_data), pointer :: ceq !IN: current equilibrium


.. function::   subroutine tqrpfil(filename,nsel,selel,ceq)


   ! read TDB file with selection of elements

       implicit none

       character*(*) filename  ! IN: database filename

       integer nsel			! IN: number of elements

       character selel(*)*2  	! IN: elements to be read from the database

       type(gtp_equilibrium_data), pointer :: ceq !IN: current equilibrium


.. function::   subroutine tqcecompact(filename,nsel,massunit,selel,tpn,xi,xf,phnames1,elref,phref,ceq)


   ! single equilibrium calculation with compact mode

   ! It combines reading tdb, setting phase status, setting reference phase of element, setting conditions, performing equilibrium calculation.

       implicit none

       character*(*) filename  ! IN: database filename

       integer nsel  			! IN: number of elements

       integer massunit  		! IN: unit of mass

   	character target*60,selel(*)*2  ! IN: element names

       double precision tpn(3)  	! IN: values of temperature, pressure and moles

   	integer :: xi(maxel)  		! IN: index of element

   	double precision xf(maxel)  ! IN: mole fraction of element

   	character phnames1*60  		! IN: phase names

   	character elref*100  		! IN: reference element

   	character phref*100  		! IN: reference phase


.. function::   subroutine tqcompbatch(nsel,nxfrac,xi,xfrac,temp,stavar,values,ceq)


   ! batch calculation with composition loop

   ! composition matrix is used.

   ! each row in composition matrix: a set of compositions for an alloy

   ! number of rows stands for number of composition variations.

       implicit none

       integer nsel  						! IN: number of element

   	integer nxfrac						! IN: number of fraction vector

   	integer :: xi(nsel)					! IN: index of element

       double precision xfrac(nxfrac,nsel)	! IN: mole fraction of element

   	double precision temp				! IN: temperature

       character stavar*(*)				! IN: name of state variable

       double precision values(*)			! EXIT: calculated state variable

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqtempbatch(nsel,ntemp,xi,xfrac,temp,stavar,values,ceq)


   ! batch calculation with temperature loop

       implicit none

       integer nsel  						! IN: number of element

       integer ntemp						! IN: number of temperature

   	integer :: xi(nsel)					! IN: index of element

       double precision xfrac(nsel)		! IN: mole fraction of element

       double precision temp(ntemp)		! IN: temperature

       character stavar*(*)				! IN: name of state variable

       double precision values(*)			! EXIT: calculated state variable

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqgcom_(n,compnames,ceq)


   ! get system component names. At present the elements

       implicit none

       integer n                               ! EXIT: number of components

       character*24, dimension(*) :: compnames ! EXIT: names of components

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqgcom(n,compnames,ceq)


   ! get system component names. At present the elements

       implicit none

       integer, intent(out) :: n                            ! EXIT: number of components

       character*2, dimension(10), intent(out) :: compnames ! EXIT: names of components

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqgnp(n,ceq)


   ! get total number of phase tuples (phases and composition sets)

   ! A second composition set of a phase is normally placed after all other

   ! phases with one composition set

       implicit none

       integer n    !EXIT: n is number of phases

       type(gtp_equilibrium_data), pointer :: ceq !IN: current equilibrium


.. function::   subroutine tqgpn(phtupx,phasename,ceq)


   ! get name of phase tuple with index phtupx (ceq redundant)

       implicit none

       integer phtupx               !IN: index in phase tuple array

       character phasename*(*)      !EXIT: phase name, max 24+8 for pre/suffix

       type(gtp_equilibrium_data), pointer :: ceq !IN: current equilibrium


.. function::   subroutine tqgpi(phtupx,phasename,ceq)


   ! get phasetuple index of phase phasename (including comp.set (ceq redundant)

       implicit none

       integer phtupx          !EXIT: phase tuple index

       character phasename*(*) !IN: phase name

       type(gtp_equilibrium_data), pointer :: ceq !IN: current equilibrium


.. function::   subroutine tqgpi2(iph,ics,phasename,ceq)


   ! get indices of phase phasename  (ceq redundant)

       implicit none

       integer iph, ics         !EXIT: phase indices 

       character phasename*(*)  !IN: phase name

       type(gtp_equilibrium_data), pointer :: ceq !IN: current equilibrium

       integer phtupx


.. function::   subroutine tqgpcn2(n,c,csname)


   ! get name of constituent with index c in phase with index n

   ! NOTE An identical routine with different constituent index is tqgpcn

       implicit none

       integer n !IN: phase number (not phase tuple)

       integer c !IN: constituent index sequentially over all sublattices

       character csname*(*) !EXIT: constituent name


.. function::   subroutine tqgpci(n,c,constituentname,ceq)


   ! get index of constituent with name in phase n

       implicit none

       integer n !IN: phase index

       integer c !IN: sequential constituent index over all sublattices

       character constituentname*(*)

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqgpcs(c,nspel,ielno,stoi,smass,qsp)


   ! get description of constituent c (stoichiometry, mass, charge) 

       implicit none

       integer c !IN: sequential constituent index over all sublattices

       integer nspel !EXIT: number of elements in species

       integer ielno(*) !EXIT: element indices

       double precision stoi(*) !EXIT: stoichiometry of elements 

       double precision smass !EXIT: mass

       double precision qsp !EXIT: charge of the species


.. function::   subroutine tqgccf(n1,n2,elnames,stoi,mass,ceq)


   ! get stoichiometry of component n1

   ! n2 is number of elements (dimension of elnames and stoi)

       implicit none

       integer n1 !IN: component number

       integer n2 !EXIT: number of elements in component

       character elnames(*)*(2) ! EXIT: element symbols

       double precision stoi(*) ! EXIT: element stoichiometry

       double precision mass    ! EXIT: component mass (sum of element mass)

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqgnpc(n,c,ceq)


   ! get number of constituents of phase n

       implicit none

       integer n !IN: Phase number

       integer c !EXIT: number of constituents

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqphsts(phtupx,newstat,val,ceq)


   ! set status of phase tuple: SUSPEND: newstat=-3;DORMANT: newstat=-2;  ENTERED: newstat=-1/0/1; FIX: newstat=2

       integer phtupx                 	! IN: index in phase tuple array

   	integer newstat					! IN: phase status

       double precision val			! EXIT: 

       type(gtp_equilibrium_data), pointer :: ceq  ! IN: current equilibrium


.. function::   subroutine tqphsts2(phnames,newstat,val,ceq)


   ! set status of many phases: SUSPEND: newstat=-3;DORMANT: newstat=-2;  ENTERED: newstat=-1/0/1; FIX: newstat=2

   ! 1) all phases: phnames = '*',   or 2) several phases: phnames = 'Phase1; ...; Phase n'

       character phnames*(*)	! IN: phase names (character)

       integer newstat			! IN: phase status

       double precision val	! EXIT: 

       type(gtp_equilibrium_data), pointer :: ceq  ! IN: current equilibrium


.. function::   subroutine tqgpsm(nphase,phases,status,amdgm,ceq)


   ! get all phase names and their status

   ! status = 2 fix, 1,0,-1 entered, -2 dormant, -3 suspended

   ! if status 0 or less the phase is not stable, extract DGM

   ! if this phase is stable, extract amount

       integer, intent(in) :: nphase  						!IN: phase number

   	character*20, dimension(*), intent(out) :: phases	!IN: phase name

       integer, dimension(nphase), intent(inout) ::  status	! EXIT: phase status

       double precision, intent(inout) ::  amdgm(*)			! EXIT: DGM or amount

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqsetc(stavar,n1,n2,value,cnum,ceq)


   ! set condition

   ! stavar is state variable as text

   ! n1 and n2 are auxilliary indices

   ! value is the value of the condition

   ! cnum is returned as an index of the condition.

   ! to remove a condition the value sould be equial to RNONE ????

   ! when a phase indesx is needed it should be 10*nph + ics

   ! see TQGETV for doucumentation of stavar etc.

       implicit none

       integer n1             ! IN: 0 or phase tuple index or component number

       integer n2             ! IN: 0 or component number

       integer cnum           ! EXIT: sequential number of this condition

       character stavar*(*)   ! IN: character with state variable symbol

       double precision value ! IN: value of condition

       type(gtp_equilibrium_data), pointer :: ceq  ! IN: current equilibrium


.. function::   subroutine tqtgsw(i)


   ! toggle global status word of index i

       implicit none

       integer i	!IN: global status word of index i


.. function::   subroutine tqce(target,n1,n2,value,ceq)


   ! calculate equilibrium with possible target

   ! Target can be empty or a state variable with indices n1 and n2

   ! value is the calculated value of target

       implicit none

       character target*(*)	! IN: 

       integer n1				! IN: n1 = 0 with grid minimizer; n1 = -1 without grid minimizer

       integer n2				! IN:

       double precision value	! EXIT

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium


.. function::   subroutine tqgetv(stavar,n1,n2,n3,values,ceq)


   ! get equilibrium results using state variables

       implicit none

       character stavar*(*)	! IN: the state variable IN CAPITAL LETTERS with indices n1 and n2 

       integer n1				! IN: phase tuple index

       integer n2				! IN: component index

       integer n3				! IN: the dimension of the array values when be called, changed to number of values on exit

       double precision values(*)	! EXIT: an array with the calculated value(s)

       type(gtp_equilibrium_data), pointer :: ceq  !IN: current equilibrium

   !========================================================

   ! stavar must be a symbol listed below

   ! IMPORTANT: some terms explained after the table

   ! Symbol  index1,index2                     Meaning (unit)

   !.... potentials

   ! T     0,0                                             Temperature (K)

   ! P     0,0                                             Pressure (Pa)

   ! MU    component,0 or ext.phase.index*1,constituent*2  Chemical potential (J)

   ! AC    component,0 or ext.phase.index,constituent      Activity = EXP(MU/RT)

   ! LNAC  component,0 or ext.phase.index,constituent      LN(activity) = MU/RT

   !...... extensive variables

   ! U     0,0 or ext.phase.index,0   Internal energy (J) whole system or phase

   ! UM    0,0 or ext.phase.index,0       same per mole components

   ! UW    0,0 or ext.phase.index,0       same per kg

   ! UV    0,0 or ext.phase.index,0       same per m3

   ! UF    ext.phase.index,0              same per formula unit of phase

   ! S*3   0,0 or ext.phase.index,0   Entropy (J/K) 

   ! V     0,0 or ext.phase.index,0   Volume (m3)

   ! H     0,0 or ext.phase.index,0   Enthalpy (J)

   ! A     0,0 or ext.phase.index,0   Helmholtz energy (J)

   ! G     0,0 or ext.phase.index,0   Gibbs energy (J)

   ! ..... some extra state variables

   ! NP    ext.phase.index,0          Moles of phase

   ! BP    ext.phase.index,0          Mass of moles (kg)

   ! Q     ext.phase.index,0          Internal stability/RT (dimensionless)

   ! DG    ext.phase.index,0          Driving force/RT (dimensionless)

   !....... amounts of components

   ! N     0,0 or component,0 or ext.phase.index,component    Moles of component

   ! X     component,0 or ext.phase.index,component   Mole fraction of component

   ! B     0,0 or component,0 or ext.phase.index,component     Mass of component

   ! W     component,0 or ext.phase.index,component   Mass fraction of component

   ! Y     ext.phase.index,constituent*1                    Constituent fraction

   !........ some parameter identifiers

   ! TC    ext.phase.index,0                Magnetic ordering temperature

   ! BMAG  ext.phase.index,0                Aver. Bohr magneton number

   ! MQ&   ext.phase.index,constituent    Mobility

   ! THET  ext.phase.index,0                Debye temperature

   ! LNX   ext.phase.index,0                Lattice parameter

   ! EC11  ext.phase.index,0                Elastic constant C11

   ! EC12  ext.phase.index,0                Elastic constant C12

   ! EC44  ext.phase.index,0                Elastic constant C44

   !........ NOTES:

   ! 1 The ext.phase.index is   10*phase_number+comp.set_number

   ! 2 The constituent index is 10*species_number + sublattice_number

   ! 3 S, V, H, A, G, NP, BP, N, B and DG can have suffixes M, W, V, F also

   !--------------------------------------------------------------------

   ! special addition for TQ interface: d2G/dyidyj

   ! D2G + phase tuple

   !--------------------------------------------------------------------


.. function::   subroutine tqgdmat(phtupx,tpval,xknown,cpot,tyst,nend,mugrad,mobval,consnames,n1,ceq)


   ! equilibrates the constituent fractions of a phase for mole fractions xknown

   ! and calculates the Darken matrix and unreduced diffusivities

       implicit none

       integer phtupx                  ! IN: index in phase tuple array

   	double precision tpval(*)		! IN: T and P

   	double precision xknown(*)		! IN: phase composition

   	double precision cpot(*)		! EXIT: (calculated) chemical potentials

       logical tyst					! IN: TRUE means no output

       integer nend					! EXIT: number of values returned in mugrad (dG_A/dN_B)

   	double precision mugrad(*)		! EXIT: derivatives of the chemical potentials wrt mole fractions??

   	double precision mobval(*)		! EXIT: mobilities	

       character*24, dimension(*) :: consnames ! EXIT: names of constituents

       integer n1						! EXIT: number of constituents

       TYPE(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqgphc1(n1,nsub,cinsub,spix,yfrac,sites,extra,ceq)


   ! get phase constitution

   ! This subroutine returns the sublattices and constitution of a phase

       implicit none

       integer n1			! IN: phase tuple index

       integer nsub		! IN: number of sublattices (1 if no sublattices)

       integer cinsub(*)	! EXIT: array with the number of constituents in each sublattices

       integer spix(*)		! EXIT: array with the species index of the constituents in all sublattices

       double precision yfrac(*)	! EXIT: constituent fractions in same order as in spix

       double precision sites(*)	! EXIT: array of the site ratios for all sublattices

       double precision extra(*)	! EXIT: array with some extra values: extra(1) is the number of moles of components per formula unit;  extra(2) is the net charge of the phase

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqsphc1(n1,yfra,extra,ceq)


   ! set constitution of a phase

   ! NOTE The constituents fractions are normalized to sum to unity for each

   !      sublattice and extra is calculated by tqsphc1

   ! T and P must be set as conditions.

       implicit none

       integer n1				! IN: phase tuple index

       double precision yfra(*)	! EXIT: array with the constituent fractions in all sublattices in the same order as obtained by tqgphc

       double precision extra(*)	! EXIT: array with returned values with the same meaning as in tqgphc1

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqcph1(n1,n2,n3,gtp,dgdy,d2gdydt,d2gdydp,d2gdy2,ceq)


   ! calculate phase properties and return arrays

   !vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

   ! WARNIG: this is not a subroutine to calculate chemical potentials

   ! those can only be obtained by an equilibrium calculation.

   ! The values returned are partial derivatives of G for the phase at the

   ! current T, P and phase constitution.  The phase constitution has been

   ! obtained by a previous equilibrium calculation or 

   ! set by the subroutine tqsphc

   ! The subroutine is equivalent to the "calculate phase" command.

   !

   ! NOTE that values are per formula unit divided by RT, 

   ! divide also by extra(1) in subroutine tqsphc1 to get them per mole component

   !

   !^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   ! calculate G and some or all derivatives for a phase at current composition

   ! They are returned in the order:  	1,1; 1,2; 1,3; ...           

   !                              		2,2; 2,3; ...

   !                                   3,3; ...

   ! for indexing one can use the integer function ixsym(i1,i2)

       implicit none

       integer n1				! IN: phase tuple index

       integer n2				! IN: = 0 if only G and derivatives wrt T and P

   							!     = 1 also first derivatives wrt compositions

   							!     = 2 if also 2nd derivatives

       integer n3				! EXIT: number of constituents (dimension of returned arrays) 

       double precision gtp(6)		! EXIT: array with G, G.T, G:P, G.T.T, G.T.P and G.P.P

       double precision dgdy(*)	! EXIT: array with G.Yi

       double precision d2gdydt(*)	! EXIT: array with G.T.Yi

       double precision d2gdydp(*)	! EXIT: array with G.P.Yi

       double precision d2gdy2(*)	! EXIT: array with the upper triangle of the symmetrix matrix G.Yi.Yj

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqcph2(n1,n2,n3,n4,ceq)


   ! calculate phase properties and return index

   !vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

   ! WARNIG: this is not a subroutine to calculate chemical potentials

   ! those can only be made by an equilibrium calculation.

   ! The values returned are partial derivatives of G for the phase at the

   ! current T, P and phase constitution.  The phase constitution has been

   ! obtained by a previous equilibrium calculation or 

   ! set by the subroutine tqsphc

   ! It corresponds to the "calculate phase" command.

   !

   ! NOTE that values are per formula unit divided by RT, 

   ! divide also by extra(1) in subroutine tqsphc1 to get them per mole component

   !

   !^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   ! calculate G and some or all derivatives for a phase at current composition

   ! for indexing one can use the integer function ixsym(i1,i2)

       implicit none

       integer n1				! IN: phase tuple index

       integer n2				! IN: type of calculation (0, 1 or 2)

       integer n3				! EXIT: returned as number of constituents

       integer n4				! EXIT: index to ceq%phase_varres(lokres)% with all results

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqcph3(n1,n2,g,ceq)


   ! Calculate phase properties and return single array

   !vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

   ! WARNIG: this is not a subroutine to calculate chemical potentials

   ! those can only be made by an equilibrium calculation.

   ! The values returned are partial derivatives of G for the phase at the

   ! current T, P and phase constitution.  The phase constitution has been

   ! obtained by a previous equilibrium calculation or 

   ! set by the subroutine tqsphc

   ! It corresponds to the "calculate phase" command.

   !

   ! NOTE that values are per formula unit divided by RT, 

   ! divide also by extra(1) in subroutine tqsphc1 to get them per mole component

   !

   !^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   ! calculate G and some or all derivatives for a phase at current composition

   ! g is an array with G derivatives under the form:

   ! G_m^\alpha = G_M^\alpha/N^\alpha, \frac{\partial G_m^\alpha}{\partial T}, \frac{\partial G_m^\alpha}{\partial P}, \frac{\partial^2 G_m^\alpha}{\partial T^2}

   ! 1/N^\alpha * \frac{\partial G_M^\alpha}{\partial y_i} (if n2>=1)

   ! 1/N^\alpha * \frac{\partial^2 G_M^\alpha}{\partial y_i\partial y_j} (if n2>=2)

       implicit none

       integer n1				! IN: phase tuple index

       integer n2				! IN: = 0 if only G and derivatives wrt T and P

   							!     = 1 also first derivatives wrt compositions

   							!     = 2 if also 2nd derivatives

       double precision g(*)	! EXIT: array with G derivatives under the form:

   							! G_m^\alpha = G_M^\alpha/N^\alpha,

   							! \frac{\partial G_m^\alpha}{\partial T},

   							! \frac{\partial G_m^\alpha}{\partial P},

   							! \frac{\partial^2 G_m^\alpha}{\partial T^2}

   							! 1/N^\alpha * \frac{\partial G_M^\alpha}{\partial y_i} (if n2>=1)

   							! 1/N^\alpha * \frac{\partial^2 G_M^\alpha}{\partial y_i\partial y_j} (if n2>=2)

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqdceq(name)


   ! delete equilibrium with name

       implicit none

       character name*24	! IN: name of equilibrium


.. function::   subroutine tqcceq(name,n1,newceq,ceq)


   ! copy current equilibrium to newceq

   ! creates a new equilibrium record with name with values same as ceq

   ! n1 is returned as index

       implicit none

       character name*24	! IN: name of equilibrium

       integer n1			! EXIT: index for equilibrium

       type(gtp_equilibrium_data), pointer :: newceq,ceq	!IN: new and current equilibrium


.. function::   subroutine tqselceq(name,ceq)


   ! select current equilibrium to be that with name.

   ! Note that equilibria can be deleted and change number but not name

       implicit none

       character name*24	! IN: name of equilibrium

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine Change_Status_Phase(myname,nystat,myval,ceq)


       implicit none

       character myname*24	! IN: name of phase

       integer nystat		! IN: phase status

       double precision myval	! IN: amount to be FIX or use as start value

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqcref(ciel,phase,tpref,ceq)


   ! set component reference state

       integer ciel			! IN: element index

       character phase*(*)		! IN: name of phase

       double precision tpref(*)	! IN: T and P values

       type(gtp_equilibrium_data), pointer :: ceq  ! IN: current equilibrium


.. function::   subroutine tqlr(lut,ceq)


   ! list the equilibrium results like in OC

       implicit none

       integer lut	! IN: unit for listing, =6 screen

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqlr1(lut,ceq)


   ! list the equilibrium results like in OC

       implicit none

       integer lut	! IN: unit for listing, =6 screen

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqlc(lut,ceq)


   ! list conditions like in OC

       implicit none

       integer lut	! IN: unit for listing, =6 screen

       type(gtp_equilibrium_data), pointer :: ceq	!IN: current equilibrium


.. function::   subroutine tqltdb


   ! list TDB file elements, phases and parameters on screen

       implicit none


.. function::   subroutine tqquiet(yes)


   ! if argument TRUE spurious output should be suppressed

       implicit none

       logical yes	! IN: .TRUE. (yes)



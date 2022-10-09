# OpenCalphad-Python
OpenCalphad-Python (OC-Python) is a Python-based library that allows users to generate their own applications using the OpenCalphad API.

OpenCalphad (OC) is a free computational thermodynamics software which can be used as a useful tool in materials science (homepage: http://www.opencalphad.org/ , source code: https://github.com/sundmanbo/opencalphad ).

## Installation
#### Windows
**Method A:**
```
python setup.py install
```
**Method B** (for example, for python 3.8):
```
python setup.py bdist_wheel -p win_amd64
cd dist
pip install ocpython-0.0.1-py38-none-win_amd64.whl
```

#### Linux, assumes Ubuntu 20.04

**Method A:**
```
python3 setup.py install
```

**Method B:**
```
python3 setup.py bdist_wheel -p linux_x86_64
cd dist
pip install ocpython-0.0.1-py38-none-linux_x86_64.whl
```

## Uninstallation
```
pip uninstall ocpython
```

## Examples

All examples are in the `examples` folder.

**An example for single equilibrium calculation:**
1. Import
```
import json
from ocpython.OCPython import SingleEquilibriumCalculation
from ocpython.OCPython import Verbosity
from ocpython.OCPython import GridMinimizerStatus as gmStat
from ocpython.OCPython_utility import OCPython_utility
```
2. Initiate SingleEquilibriumCalculation and set verbosity level
```
vs = Verbosity(newlogfile=True,process_name='SingleEquilibriumCalculation')
vs.setVerbosity(False)
oc = SingleEquilibriumCalculation(vs)
```
3. Read tdb database with elements and get all phases in the system
```
oc.readtdb(r'steel1.TDB',['FE','C','CR'])
phases = []
for index in range(oc.getNumberPhase()):
  phases.append(oc.getPhaseName(index))
print('list phases:',phases)
comp = oc.getComponentNames()
print('components list from database:', comp)
```
4. Set conditions
```
oc.setPressure(1E5)
oc.setTemperature(800)
oc.setTotalMolarAmount(1)
elementMassFractions = {
    'C' : 0.009,
    'CR' : 0.045,
    'FE': -1}
oc.setElementMassFraction(elementMassFractions)
```
5. Calculate equilibrium and list results
```
oc.calculateEquilibrium(gmStat.On)
print('Gibbs energy [J]: ',  "{:.2f}".format(oc.getGibbsEnergy()))
phaseElementComposition = oc.getPhaseElementComposition()
if not isVerbosity: print('Phase element composition:\n'+json.dumps(json.loads(json.dumps(phaseElementComposition), parse_float=lambda x: round(float(x), 6)),indent=4))
phasefraction = OCPython_utility.getPhaseFraction(oc)
if not isVerbosity: print('Phase molar fractions:\n'+json.dumps(json.loads(json.dumps(phasefraction), parse_float=lambda x: round(float(x), 6)),indent=4))
```

## Documentation
You can build it yourself from the `docs` folder and enter `make html` in terminal.
You can then view the built documentation in the `docs/build/html` folder.

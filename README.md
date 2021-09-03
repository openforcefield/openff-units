openff-units
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/openforcefield/openff-units/workflows/CI/badge.svg)](https://github.com/openforcefield/openff-units/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/openforcefield/openff-units/branch/main/graph/badge.svg)](https://codecov.io/gh/openforcefield/openff-units/branch/main)


A common units module for the OpenFF software stack

**Please note that this software in an early and experimental state and unsuitable for production.**

This package provides a common unit registry for all OpenFF packages to use in order to ensure consistent unit definitions across the software ecosystem.

The unit definitions are currently sourced from the NIST 2018 [CODATA](https://physics.nist.gov/cuu/Constants/), but may be updated in future versions as new CODATA updates are made.

While this repository is based on [Pint](https://pint.readthedocs.io/en/0.16.1/), the main classes (`Unit`, `Quantity`, and `Measurement`) have been subclassed in order to provide non-dynamic, more readily serialisable representations.

### Installation

Conda packages are coming soon!

### Getting Started

Import the [unit registry](https://pint.readthedocs.io/en/0.16.1/tutorial.html#initializing-a-registry)

```python3
>>> from openff.units import unit
>>> distance = 24.0 * unit.meter
>>> distance
<Quantity(24.0, 'meter')>
>>> print(distance)
24.0 m
```

From here, one can proceed with the rest of the [Pint tutorial](https://pint.readthedocs.io/en/0.16.1/tutorial.html#tutorial), using the `unit` object above as a drop-in replacement for `ureg` in the tutorial.

### Copyright

Copyright (c) 2021, Open Force Field Initiative


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.

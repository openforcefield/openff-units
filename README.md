openff-units
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/openforcefield/openff-units/workflows/CI/badge.svg)](https://github.com/openforcefield/openff-units/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/openforcefield/openff-units/branch/main/graph/badge.svg)](https://codecov.io/gh/openforcefield/openff-units/branch/main)


A common units module for the OpenFF software stack

**Please note that this software in an early and experimental state and unsuitable for production.**

This package provides a common unit registry for all OpenFF packages to use in order to ensure consistent unit definitions across the software ecosystem.

The unit definitions are currently sourced from the NIST 2018 [CODATA](https://physics.nist.gov/cuu/Constants/), but may be updated in future versions as new CODATA updates are made.

While this repository is based on [Pint](https://pint.readthedocs.io/en/0.16.1/), the main classes (`Unit`, `Quantity`, and `Measurement`) have been slightly modified in order to provide non-dynamic, more readily serialisable representations.

### Installation

Install via `conda` or a replacement:

```shell
conda install openff-units -c conda-forge
```

### Getting Started

This example shows how to tag a number with a unit (generating an object called a `Quantity`),
get its magntude with without units, convnert to another unit, and also get its magnnitude after converting to another unit.

```python3
>>> bond_length = 1.4 * unit.angstrom
>>> bond_length
<Quantity(1.4, 'angstrom')>
>>> bond_length.magnitude
1.4
>>> bond_length.to(unit.nanometer)
<Quantity(0.14, 'nanometer')>
>>> bond_length.magnitude_as(unit.nanometer)
0.14
```

From here, one can proceed with the rest of the [Pint tutorial](https://pint.readthedocs.io/en/0.16.1/tutorial.html#tutorial), using the `unit` object above as a drop-in replacement for `ureg` in the tutorial.

### Serialization

Scalar quantities can be serialised to strings unsing the built-in `str()` function and deserialized using the `unit.Quantity` constructor.

```python3
>>> k = 10 * unit.kilocalorie / unit.mol / unit.nanometer**2
>>> k
<Quantity(10.0, 'kilocalorie / mole / nanometer ** 2')>
>>> str(k)
'10.0 kcal / mol / nm ** 2'
>>> unit.Quantity(str(k))
<Quantity(10.0, 'kilocalorie / mole / nanometer ** 2')>
```

### OpenMM Interoperability

For compatibility with [OpenMM units](http://docs.openmm.org/latest/api-python/app.html#units), a submodule (`openff.units.openmm`) with conversion functions (`to_openmm`, `from_openmm`) is also provided.

```python3
>>> from openff.units import unit
>>> from openff.units.openmm import to_openmm, from_openmm
>>> distance = 24.0 * unit.meter
>>> converted = to_openmm(distance)
>>> converted
Quantity(value=24.0, unit=meter)
>>> type(converted)
<class 'openmm.unit.quantity.Quantity'>
>>> roundtripped = from_openmm(converted)
>>> roundtripped
<Quantity(24.0, 'meter')>
>>> type(roundtripped)
<class 'openff.units.units.Quantity'>
```

An effort is made to convert from OpenMM constructs, such as when OpenMM provides array-like data as a list of `Vec3` objects into Pint's wrapped NumPy arrays:

```python3
>>> from openmm import app
>>> positions = app.PDBFile("top.pdb").getPositions()
>>> positions
Quantity(value=[Vec3(x=-0.07890000000000001, y=-0.0198, z=-0.0), Vec3(x=-0.0006000000000000001, y=0.039200000000000006, z=-0.0), Vec3(x=0.07950000000000002, y=-0.0194, z=0.0), Vec3(x=0.9211, y=0.9802, z=1.0), Vec3(x=0.9994000000000001, y=1.0392, z=1.0), Vec3(x=1.0795000000000001, y=0.9805999999999999, z=1.0)], unit=nanometer)
>>> type(positions)
<class 'openmm.unit.quantity.Quantity'>
>>> type(positions._value)
<class 'list'>
>>> type(positions._value[0])
<class 'openmm.vec3.Vec3'>
>>> converted = from_openmm(positions)
>>> converted
<Quantity([[-7.8900e-02 -1.9800e-02 -0.0000e+00]
 [-6.0000e-04  3.9200e-02 -0.0000e+00]
 [ 7.9500e-02 -1.9400e-02  0.0000e+00]
 [ 9.2110e-01  9.8020e-01  1.0000e+00]
 [ 9.9940e-01  1.0392e+00  1.0000e+00]
 [ 1.0795e+00  9.8060e-01  1.0000e+00]], 'nanometer')>
>>> converted.m
array([[-7.8900e-02, -1.9800e-02, -0.0000e+00],
       [-6.0000e-04,  3.9200e-02, -0.0000e+00],
       [ 7.9500e-02, -1.9400e-02,  0.0000e+00],
       [ 9.2110e-01,  9.8020e-01,  1.0000e+00],
       [ 9.9940e-01,  1.0392e+00,  1.0000e+00],
       [ 1.0795e+00,  9.8060e-01,  1.0000e+00]])
>>> type(converted)
<class 'openff.units.units.Quantity'>
>>> type(converted.m)
<class 'numpy.ndarray'>
```

### Copyright

Copyright (c) 2021, Open Force Field Initiative


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.

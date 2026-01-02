openff-units
==============================
[//]: # (Badges)
[![CI Status](https://github.com/openforcefield/openff-units/workflows/CI/badge.svg)](https://github.com/openforcefield/openff-units/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/openforcefield/openff-units/branch/main/graph/badge.svg)](https://codecov.io/gh/openforcefield/openff-units/branch/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/openforcefield/openff-units/main.svg)](https://results.pre-commit.ci/latest/github/openforcefield/openff-units/main)
[![conda](https://img.shields.io/conda/v/conda-forge/openff-units.svg)](https://anaconda.org/conda-forge/openff-units)


A common units module for the OpenFF software stack

**Please note that there may still be some changes to the API prior to a stable 1.0.0 release.**

This package provides a common unit registry for all OpenFF packages to use in order to ensure consistent unit definitions across the software ecosystem.

The unit definitions are currently sourced from the NIST 2018 [CODATA](https://physics.nist.gov/cuu/Constants/), but may be updated in future versions as new CODATA updates are made.

While this repository is based on [Pint](https://pint.readthedocs.io/en/0.16.1/), the main classes (`Unit`, `Quantity`, and `Measurement`) have been slightly modified in order to provide non-dynamic, more readily serialisable representations.

### Installation

Install via `mamba` or a replacement:

```shell
mamba install openff-units -c conda-forge
```

### Getting Started

Below shows how to tag a number with a unit (generating a `Quantity` object),
get its magnitude with and without units, convert to another unit, and also get its magnitude after converting to another unit.

```python3
>>> from openff.units import Quantity
>>> bond_length = Quantity(1.4, "angstrom")
>>> bond_length
<Quantity(1.4, 'angstrom')>
>>> bond_length.magnitude
1.4
>>> bond_length.to("nanometer")
<Quantity(0.14, 'nanometer')>
>>> bond_length.m_as("nanometer")
0.14
```

One could also do the [Pint tutorial](https://pint.readthedocs.io/en/0.16.1/tutorial.html#tutorial) using the `unit` object above as a drop-in replacement for `ureg` in the tutorial.

### Serialization

Scalar quantities can be serialized to strings using the built-in `str()` function and deserialized using the `unit.Quantity` constructor.

```python3
>>> k = Quantity(10, "kilocalorie / mol / nanometer**2")
>>> k
<Quantity(10.0, 'kilocalorie / mole / nanometer ** 2')>
>>> str(k)
'10.0 kcal / mol / nm ** 2'
>>> Quantity(str(k))
<Quantity(10.0, 'kilocalorie / mole / nanometer ** 2')>
```

### OpenMM Interoperability

For compatibility with [OpenMM units](http://docs.openmm.org/latest/api-python/app.html#units), a submodule (`openff.units.openmm`) with conversion functions (`to_openmm`, `from_openmm`) is also provided.

```python3
>>> from openff.units import Quantity
>>> from openff.units.openmm import to_openmm, from_openmm
>>> distance = Quantity(24.0, "meter")
>>> converted = to_openmm(distance)
>>> converted
24.0 m
>>> type(converted)
<class 'openmm.unit.quantity.Quantity'>
>>> roundtripped = from_openmm(converted)
>>> roundtripped
<Quantity(24.0, 'meter')>
>>> type(roundtripped)
pint.Quantity
```

An effort is made to convert from OpenMM constructs, such as when OpenMM provides array-like data as a list of `Vec3` objects:into Pint's wrapped NumPy arrays:

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
#### Dealing with multiple unit packages

You may find yourself needing to normalize a quantity to a particular unit package, while accepting inputs from either `openff.units` or `openmm.unit`. The [`ensure_quantity`] function simplifies this. It takes as arguments a quantity object from either unit solution and a string (`"openff"` or `"openmm"`) indicating the desired unit type, and returns a quantity from that package. If the quantity argument is already the requested type, the function short-circuits, so it should not introduce substantial overhead compared to simply requiring the target quantity type.

[`ensure_quantity`]: https://docs.openforcefield.org/projects/units/en/stable/api/generated/openff.units.ensure_quantity.html

```python3
>>> from openff.units import Quantity, ensure_quantity
>>> ensure_quantity(Quantity(4.0, "angstrom"), "openff")
<Quantity(4.0, 'angstrom')>  # OpenFF
>>> ensure_quantity(Quantity(4.0, "angstrom"), "openmm")
4.0 A
>>>
>>> import openmm.unit
>>> ensure_quantity(openmm.unit.Quantity(4.0, openmm.unit.angstrom), "openmm")
4.0 A
>>> ensure_quantity(openmm.unit.Quantity(4.0, openmm.unit.angstrom), "openff")
<Quantity(4.0, 'angstrom')>  # OpenFF
```

### Known issues

There is a quirk with cached unit registry definitions that could cause issues when running tests in parallel (i.e. with `pytest-xdist`). See [Issue #111](https://github.com/openforcefield/openff-units/issues/111) for more details. This was fixed in version 0.3.1.

### Copyright

Copyright (c) 2021, Open Force Field Initiative


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.

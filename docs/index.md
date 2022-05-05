# OpenFF Units

Units of measure for biomolecular software.

OpenFF Units is based on [Pint]. Its [`Quantity`], [`Unit`], and [`Measurement`] types inherit from Pint's, and add improved support for serialization and deserialization. OpenFF Units improves support for biomolecular software by providing a [system of units] that are compatible with [OpenMM] and [providing functions] to convert to OpenMM units and back. It also provides [atomic masses] with units, as well as some [other useful maps].

[system of units]: openff.units.unit
[OpenMM]: openmm:index
[Pint]: pint:index
[`Quantity`]: openff.units.Quantity
[`Unit`]: openff.units.Unit
[`Measurement`]: openff.units.Measurement 
[providing functions]: openff.units.openmm
[atomic masses]: openff.units.elements.MASSES
[other useful maps]: openff.units.elements

## Installation

We recommend installing OpenFF Units with the [Conda] package manager. If you don't yet have a Conda distribution installed, we recommend [MambaForge] for most users. The `openff-units` package can be installed from Conda Forge:

```shell
conda install -c conda-forge openff-units
```

[Conda]: https://conda.io
[MambaForge]: https://github.com/conda-forge/miniforge#mambaforge

## Using OpenFF Units

OpenFF Units provides the [`Quantity`] class, which represents a numerical value with units. To create a `Quantity`, multiply a value by the appropriate unit:

```python
from openff.units import unit

mass_proton = 1.007 * unit.amu
```

`Quantity` can also wrap NumPy arrays. It's best to wrap an Array of floats in a quantity, rather than have an array of quantities:

```python
import numpy as np
from openff.units import unit

box_vectors = np.array([
    [5.0, 0.0, 0.0],
    [0.0, 5.0, 0.0],
    [0.0, 0.0, 5.0],
]) * unit.nanometer
```

Complex units can be constructed by combining units with the usual arithmetic operations:

```python
boltzmann_constant = 8.314462618e-3 * unit.kilojoule / unit.kelvin / unit.avogadro_number
```

Some common constants are provided as units as well:

```python
boltzmann_constant = 1.0 * unit.boltzmann_constant
```

Adding or subtracting different units with the same dimensions just works:

```pycon
>>> 1.0 * unit.angstrom + 1.0 * unit.nanometer
<Quantity(11.0, 'angstrom')>
```

But quantities with different dimensions raises an exception:

```pycon
>>> 1.0 * unit.angstrom + 1.0 * unit.nanojoule
Traceback (most recent call last):
...
pint.errors.DimensionalityError: Cannot convert from 'angstrom' ([length]) to 'nanojoule' ([length] ** 2 * [mass] / [time] ** 2)
```

Quantities can be converted between units with the [`.to()`] method:

```pycon
>>> (1.0 * unit.nanometer).to(unit.angstrom)
<Quantity(10.0, 'angstrom')>
```

Or with the [`.ito()`] method for in-place transformations:

```pycon
>>> quantity = 10.0 * unit.angstrom
>>> quantity.ito(unit.nanometer)
>>> quantity
<Quantity(1.0, 'nanometer')>
```

The underlying value without units can be retrieved with the [`.m`] or [`.magnitude`] properties. Just make sure it's in the units you expect first:

```pycon
>>> quantity = 1.0 * unit.k_B
>>> quantity.ito_base_units()
>>> assert quantity.units == unit.kilogram * unit.meter**2 / unit.kelvin / unit.second**2
>>> quantity.magnitude
1.380649e-23
```

`Quantity` will pass any attributes it doesn't have through to the inner value. This means that an quantity-wrapped array can be used exactly as though it were an array --- the units are just checked silently in the background:

```python
from numpy.random import rand

trajectory = 10 * rand(10, 10000, 3) * unit.nanometer
centroids = trajectory.mean(axis=1)[..., None]
last_water = trajectory[:, 97:99, :]
last_water_recentered = last_water - centroids
```

[`.to()`]: openff.units.Quantity.to
[`.ito()`]: openff.units.Quantity.ito
[`.m`]: openff.units.Quantity.m
[`.magnitude`]: openff.units.Quantity.magnitude

:::{toctree}
---
hidden: true
---

Overview <self>
:::

<!-- 
:::{toctree}
---
hidden: true
caption: User Guide
---

::: 
-->

<!--
The autosummary directive renders to rST,
so we must use eval-rst here
-->
:::{eval-rst}
.. raw:: html

    <div style="display: None">

.. autosummary::
   :recursive:
   :caption: API Reference
   :toctree: api/generated
   :nosignatures:

   openff.units

.. raw:: html

    </div>
:::

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

We recommend installing OpenFF Units with the [Conda] or [Mamba] package managers. If you don't yet have a Conda distribution installed, we recommend [MambaForge] for most users; see the [OpenFF install docs]. The `openff-units` package can be installed from Conda Forge:

```shell
conda install -c conda-forge openff-units
```

[Conda]: https://conda.io
[Mamba]: https://mamba.readthedocs.io
[OpenFF install docs]: openff.docs:install
[MambaForge]: https://github.com/conda-forge/miniforge#mambaforge

## Using OpenFF Units

OpenFF Units provides the [`Quantity`] class, which represents a numerical value with units. A `Quantity` can be created by providing a value and units:

```pycon
>>> from openff.units import unit, Quantity
>>> 
>>> Quantity(1.007, unit.amu)
<Quantity(1.007, 'unified_atomic_mass_unit')>
```

The `unit` singleton value is a registry of units, but also exposes the `Quantity`, `Unit`, and `Measurement` classes so you don't have to import them individually. Even easier, multiplying a number by the appropriate unit also provides a `Quantity`:

```pycon
>>> mass_proton = 1.007 * unit.amu
>>> mass_proton == unit.Quantity(1.007, unit.amu)
True
```

`Quantity` can also wrap NumPy arrays. It's best to wrap an array of floats in a quantity, rather than have an array of quantities:

```pycon
>>> import numpy as np
>>> 
>>> box_vectors = np.array([
...     [5.0, 0.0, 0.0],
...     [0.0, 5.0, 0.0],
...     [0.0, 0.0, 5.0],
... ]) * unit.nanometer
```

When constructed like this, `Quantity` is transparent; it will pass any attributes it doesn't have through to the inner value. This means that an quantity-wrapped array can be used exactly as though it were an array --- the units are just checked silently in the background:

```pycon
>>> from numpy.random import rand
>>> 
>>> trajectory = 10 * rand(10, 10000, 3) * unit.nanometer
>>> centroids = trajectory.mean(axis=1)[..., None]
>>> last_water = trajectory[:, 97:99, :]
>>> last_water_recentered = last_water - centroids
```

This transparency works with most container types, so it's usually best to have `Quantity` be the outermost wrapper type.

Complex units can be constructed by combining units with the usual arithmetic operations:

```pycon
>>> boltzmann_constant = 8.314462618e-3 * unit.kilojoule / unit.kelvin / unit.avogadro_number
```

Some common constants are provided as units as well:

```pycon
>>> boltzmann_constant = 1.0 * unit.boltzmann_constant
```

Adding or subtracting different units with the same dimensions just works:

```pycon
>>> 1.0 * unit.angstrom + 1.0 * unit.nanometer
<Quantity(11.0, 'angstrom')>
```

But quantities with different dimensions raise an exception:

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
>>> quantity = (1.0 * unit.k_B).to_base_units()
>>> assert quantity.units == unit.kilogram * unit.meter**2 / unit.kelvin / unit.second**2
>>> quantity.magnitude
1.380649e-23
```

Alternatively, specify the target units of the output magnitude with [`.m_as`]:

```pycon
>>> quantity = 1.0 * unit.k_B
>>> quantity.m_as(unit.kilogram * unit.meter**2 / unit.kelvin / unit.second**2)
1.380649e-23
```

OpenFF Units also provides the [`from_openmm`] and [`to_openmm`] functions to convert between OpenFF quantities and OpenMM quantities:

```pycon
>>> from openff.units.openmm import from_openmm, to_openmm
>>>
>>> quantity = 10.0 * unit.angstrom
>>> omm_quant = to_openmm(quantity)
>>> omm_quant
Quantity(value=10.0, unit=angstrom)
>>> type(omm_quant)
<class 'openmm.unit.quantity.Quantity'>
>>> quant_roundtrip = from_openmm(omm_quant)
>>> quant_roundtrip
<Quantity(10.0, 'angstrom')>
>>> type(quant_roundtrip)
<class 'openff.units.units.Quantity'>
```

For more details, see the [API reference].

## Current development

### Behavior changes

* #62 Drops support for Python 3.8, following [NEP 29](https://numpy.org/neps/nep-0029-deprecation_policy.html#support-table).

[`.to()`]: openff.units.Quantity.to
[`.ito()`]: openff.units.Quantity.ito
[`.m`]: openff.units.Quantity.m
[`.magnitude`]: openff.units.Quantity.magnitude
[`.m_as`]: openff.units.Quantity.m_as
[`from_openmm`]: openff.units.openmm.from_openmm
[`to_openmm`]: openff.units.openmm.to_openmm
[API reference]: openff.units

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

"""
Core classes for OpenFF Units
"""
import uuid
import warnings
from typing import TYPE_CHECKING

import pint
from openff.utilities import requires_package
from pint import Measurement as _Measurement
from pint import Quantity as _Quantity
from pint import Unit as _Unit

from openff.units.utilities import get_defaults_path

if TYPE_CHECKING:
    from openmm.unit import Quantity as OpenMMQuantity

__all__ = [
    "DEFAULT_UNIT_REGISTRY",
    "Quantity",
    "Measurement",
    "Unit",
]


class Unit(pint.UnitRegistry.Unit):
    """A unit of measure."""

    pass


class Quantity(pint.UnitRegistry.Quantity):
    """A value with associated units."""

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Quantity(values, units)


@requires_package("openmm")
def _to_openmm(self) -> "OpenMMQuantity":
    """Convert the quantity to an ``openmm.unit.Quantity``.

    Returns
    -------
    openmm_quantity : openmm.unit.quantity.Quantity
        The OpenMM compatible quantity.
    """
    from openff.units.openmm import to_openmm

    return to_openmm(self)


class Measurement(pint.UnitRegistry.Measurement):  # type: ignore
    """A value with associated units and uncertainty."""

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Measurement(values, units)


class UnitRegistry(pint.UnitRegistry):
    _quantity_class = Quantity
    _unit_class = Unit
    _measurement_class = Measurement


DEFAULT_UNIT_REGISTRY = UnitRegistry(get_defaults_path())

Unit: _Unit = DEFAULT_UNIT_REGISTRY.Unit  # type: ignore[no-redef]
Quantity: _Quantity = DEFAULT_UNIT_REGISTRY.Quantity  # type: ignore[no-redef]
Measurement: _Measurement = DEFAULT_UNIT_REGISTRY.Measurement  # type: ignore

pint.set_application_registry(DEFAULT_UNIT_REGISTRY)

Quantity.to_openmm = _to_openmm  # type: ignore[attr-defined]

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

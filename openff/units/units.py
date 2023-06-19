"""
Core classes for OpenFF Units
"""
import uuid
import warnings
from typing import TYPE_CHECKING, Type
from typing_extensions import TypeAlias

import pint
from openff.utilities import requires_package

from openff.units.utilities import get_defaults_path

if TYPE_CHECKING:
    from openmm.unit import Quantity as OpenMMQuantity

__all__ = [
    "DEFAULT_UNIT_REGISTRY",
    "Quantity",
    "Measurement",
    "Unit",
]


class _Unit(pint.UnitRegistry.Unit):
    """A unit of measure."""

    pass


class _Quantity(pint.UnitRegistry.Quantity):
    """A value with associated units."""

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Quantity(values, units)

    @requires_package("openmm")
    def to_openmm(self) -> "OpenMMQuantity":
        """Convert the quantity to an ``openmm.unit.Quantity``.

        Returns
        -------
        openmm_quantity : openmm.unit.quantity.Quantity
            The OpenMM compatible quantity.
        """
        from openff.units.openmm import to_openmm

        return to_openmm(self)


class Measurement(pint.UnitRegistry.Measurement):
    """A value with associated units and uncertainty."""

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Measurement(values, units)


class UnitRegistry(
    pint.UnitRegistry,
    pint.registry.GenericUnitRegistry[_Quantity, _Unit],
):
    Unit: TypeAlias = _Unit
    Quantity: TypeAlias = _Quantity
    Measurement: TypeAlias = Measurement


DEFAULT_UNIT_REGISTRY: UnitRegistry = UnitRegistry(get_defaults_path())

Quantity = UnitRegistry.Quantity
Unit = UnitRegistry.Unit
Measurement = UnitRegistry.Measurement

pint.set_application_registry(DEFAULT_UNIT_REGISTRY)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

q = Quantity(3, None)

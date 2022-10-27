"""
Core classes for OpenFF Units
"""
import uuid
import warnings
from typing import TYPE_CHECKING

import pint
from openff.utilities import requires_package
from pint import UnitRegistry as _UnitRegistry

from openff.units.utilities import get_defaults_path

if TYPE_CHECKING:
    from openmm.unit import Quantity as OpenMMQuantity

__all__ = [
    "DEFAULT_UNIT_REGISTRY",
    "Quantity",
    "Measurement",
    "Unit",
]

# def _unpickle_quantity(cls, *args):
#     """Rebuild quantity upon unpickling using the application registry."""
#     return pint._unpickle(Quantity, *args)
#
#
# def _unpickle_unit(cls, *args):
#     """Rebuild unit upon unpickling using the application registry."""
#     return pint._unpickle(Unit, *args)
#
#
# def _unpickle_measurement(cls, *args):
#     """Rebuild measurement upon unpickling using the application registry."""
#     return pint._unpickle(Measurement, *args)


class Unit:
    pass
    """
    def __reduce__(self):
        return _unpickle_unit, (Unit, self._units)
    """


class Quantity:
    """
    def __reduce__(self):
        return _unpickle_quantity, (Quantity, self.magnitude, self._units)
    """

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


class Measurement:
    """
    def __reduce__(self):
        return _unpickle_measurement, (Measurement, self.magnitude, self._units)
    """

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Measurement(values, units)


class UnitRegistry(_UnitRegistry):
    _quantity_class = Quantity
    _unit_class = Quantity
    _measurement_class = Measurement


DEFAULT_UNIT_REGISTRY = UnitRegistry(get_defaults_path())

Unit = DEFAULT_UNIT_REGISTRY.Unit
Quantity = DEFAULT_UNIT_REGISTRY.Quantity
Measurement = DEFAULT_UNIT_REGISTRY.Measurement

pint.set_application_registry(DEFAULT_UNIT_REGISTRY)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

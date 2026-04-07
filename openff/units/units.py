"""
Core classes for OpenFF Units
"""

import uuid
import warnings
from typing import TYPE_CHECKING

import pint
from openff.utilities import requires_package
from pint import Measurement as _Measurement
from pint import Quantity as PintQuantity
from pint import Unit as _Unit
from pydantic_pint import PydanticPintQuantity

from openff.units.utilities import get_defaults_path

if TYPE_CHECKING:
    import openmm.unit

__all__ = (
    "DEFAULT_UNIT_REGISTRY",
    "Measurement",
    "Quantity",
    "Unit",
    "unit",
)
from typing import Annotated, Any, TypeVar

from pydantic import PlainSerializer


def ser_type(value: type[Any]) -> str:
    return value.__name__


T = TypeVar("T")

JSONSerializableType = Annotated[type[T], PlainSerializer(ser_type, when_used="json-unless-none")]


class Unit(pint.UnitRegistry.Unit):
    """A unit of measure."""


class _Quantity(pint.UnitRegistry.Quantity):
    """A value with associated units."""

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Quantity(values, units)


@requires_package("openmm")
def _to_openmm(self) -> "openmm.unit.Quantity":
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


class UnitRegistry(pint.UnitRegistry):
    _quantity_class = _Quantity
    _unit_class = Unit
    _measurement_class = Measurement


DEFAULT_UNIT_REGISTRY = UnitRegistry(get_defaults_path())

unit = DEFAULT_UNIT_REGISTRY

Unit: type[_Unit] = DEFAULT_UNIT_REGISTRY.Unit
Quantity: type[_Quantity] = DEFAULT_UNIT_REGISTRY.Quantity
Measurement: type[_Measurement] = DEFAULT_UNIT_REGISTRY.Measurement

pint.set_application_registry(DEFAULT_UNIT_REGISTRY)

Quantity = Annotated[
    PintQuantity, PydanticPintQuantity("kilocalories_per_mole", ureg=DEFAULT_UNIT_REGISTRY)
]

DEFAULT_UNIT_REGISTRY._quantity_class = Quantity

Quantity.to_openmm = _to_openmm  # type: ignore[attr-defined]

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

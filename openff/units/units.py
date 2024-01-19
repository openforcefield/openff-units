"""
Core classes for OpenFF Units
"""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Union

import pint
import pydantic.v1 as pydantic
from openff.utilities import requires_package
from pint import Measurement as _Measurement
from pint import Unit as _Unit

from openff.units.utilities import get_defaults_path

if TYPE_CHECKING:
    from openmm.unit import Quantity as OpenMMQuantity
    from openmm.unit import Unit as OpenMMUnit

__all__ = [
    "DEFAULT_UNIT_REGISTRY",
    "Quantity",
    "Measurement",
    "Unit",
]


class Unit(pint.UnitRegistry.Unit):
    """A unit of measure."""

    pass


class Quantity[float_or_array, unit](pydantic.BaseModel):
    pint: Any  # pint.Quantity

    class Config:
        arbitrary_types_allowed = True

    def value_in_unit(self, openmm_unit: Union[str, "OpenMMUnit"]) -> float:
        pass
        return self.to_openmm().value_in_unit(openmm_unit)

    def to_openmm():
        pass
        # keep this implementation

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, value, unit=None, *args, **kwargs):
        super().__init__(
            pint=pint.Quantity(value, unit),
            *args,
            **kwargs,
        )

    def __getattr__(self, name: str):
        return self.pint.__getattribute__(name)

    @classmethod
    def __class_getitem__(cls, item: tuple):
        print(item)
        return super().__class_getitem__(item)


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
Measurement: _Measurement = DEFAULT_UNIT_REGISTRY.Measurement  # type: ignore

pint.set_application_registry(DEFAULT_UNIT_REGISTRY)

Quantity.to_openmm = _to_openmm  # type: ignore[attr-defined]

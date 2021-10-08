import uuid
import warnings

import pint
from openff.utilities.utilities import has_package
from pint.measurement import _Measurement
from pint.quantity import _Quantity
from pint.unit import _Unit

from openff.units.utilities import get_defaults_path

if has_package("openmm"):
    from openmm import unit as openmm_unit
    from openmm.unit import Unit as OpenMMUnit
else:
    OpenMMUnit = type(None)


DEFAULT_UNIT_REGISTRY = pint.UnitRegistry(get_defaults_path())


def _unpickle_quantity(cls, *args):
    """Rebuild quantity upon unpickling using the application registry."""
    return pint._unpickle(DEFAULT_UNIT_REGISTRY.Quantity, *args)


def _unpickle_unit(cls, *args):
    """Rebuild unit upon unpickling using the application registry."""
    return pint._unpickle(DEFAULT_UNIT_REGISTRY.Unit, *args)


def _unpickle_measurement(cls, *args):
    """Rebuild measurement upon unpickling using the application registry."""
    return pint._unpickle(DEFAULT_UNIT_REGISTRY.Measurement, *args)


class Unit(_Unit):
    _REGISTRY = DEFAULT_UNIT_REGISTRY

    def __reduce__(self):
        return _unpickle_unit, (Unit, self._units)


class Quantity(_Quantity):
    _REGISTRY = DEFAULT_UNIT_REGISTRY

    def __init__(self, value=None, unit=None):
        self._pint = False
        self._openmm = False
        if isinstance(unit, pint.Unit) or unit is None:
            quantity = pint.Quantity(value, unit)
            self._magnitude = quantity._magnitude
            self._units = quantity._units
            self._pint = True
        elif isinstance(unit, OpenMMUnit):
            quantity = openmm_unit.Quantity(value, unit)
            self._value = quantity._value
            self._unit = quantity.unit
            self._openmm = True

    def _convert_magnitude_not_inplace(self, other):
        return DEFAULT_UNIT_REGISTRY.convert(self._magnitude, self._units, other)

    def to(self, other):
        other = to_units_container(other, DEFAULT_UNIT_REGISTRY)

        magnitude = self._convert_magnitude_not_inplace(other)

        return self.__class__(magnitude, other)

    @property
    def m(self):
        if self._pint:
            return self._magnitude
        if self._openmm:
            return self._value

    def m_as(self, unit_):
        if self._pint:
            return self._convert_magnitude_not_inplace(_as_pint_unit(unit_))
        if self._openmm:
            return self.value_in_unit(_as_openmm_unit(unit_))

    @property
    def unit(self):
        if self._pint:
            return self._units
        if self._openmm:
            return self._unit

    @property
    def units(self):
        if self._pint:
            return self._units
        if self._openmm:
            return self.unit

    def value_in_unit(self, unit_):
        if self._pint:
            return self.m_as(_as_pint_unit(unit_))
        if self._openmm:
            return openmm_unit.Quantity.value_in_unit(self, _as_openmm_unit(unit_))

    def __reduce__(self):
        return _unpickle_quantity, (Quantity, self.magnitude, self._units)

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Quantity(values, units)


class Measurement(_Measurement):
    _REGISTRY = DEFAULT_UNIT_REGISTRY

    def __reduce__(self):
        return _unpickle_measurement, (Measurement, self.magnitude, self._units)

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Measurement(values, units)


DEFAULT_UNIT_REGISTRY.Unit = Unit
DEFAULT_UNIT_REGISTRY.Quantity = Quantity
DEFAULT_UNIT_REGISTRY.Measurement = Measurement

pint.set_application_registry(DEFAULT_UNIT_REGISTRY)
DEFAULT_UNIT_REGISTRY.default_format = "~"

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     Quantity([])

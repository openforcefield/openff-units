"""
Core classes for OpenFF Units
"""

from __future__ import annotations

import json
import uuid
import warnings
from typing import TYPE_CHECKING, Any

import numpy  # possible to make this optional?
import pint
from openff.utilities import requires_package
from pint import Measurement as _Measurement
from pint import Quantity as _Quantity
from pint import Unit as _Unit
from pint.facets.plain.quantity import PlainQuantity as PintQuantity

from openff.units.utilities import get_defaults_path

if TYPE_CHECKING:
    import openmm.unit

try:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import core_schema

    has_pydantic = True
except ImportError:
    has_pydantic = False

__all__ = (
    "DEFAULT_UNIT_REGISTRY",
    "Measurement",
    "Quantity",
    "Unit",
    "unit",
)


class Unit(pint.UnitRegistry.Unit):
    """A unit of measure."""

    pass


if has_pydantic:

    class _QuantityMixin:
        @classmethod
        def serialize(
            cls,
            v: PintQuantity,
            info: core_schema.SerializationInfo | None = None,
        ) -> dict | str | PintQuantity:
            to_json = info is not None and info.mode_is_json()

            if to_json:
                magnitude = v.magnitude

                # storing numpy arrays natively works fine in memory in Python,
                # but must be list-ified when serializing to JSON.
                if isinstance(magnitude, numpy.ndarray):
                    magnitude = v.magnitude.tolist()

                # TODO: I think this is necessary for handling unit-wrapped arrays, but it is
                #       not so performant. Scalar quantities can be directly serialized to much
                #       shorter strings
                return json.dumps(
                    {
                        "magnitude": magnitude,
                        "units": str(v.units),
                    }
                )

            return {
                "magnitude": v.magnitude,
                "units": str(v.units),
            }

        @classmethod
        def validate(
            cls,
            v: dict | str | PintQuantity,
        ):
            if isinstance(v, Quantity):
                return v
            elif isinstance(v, str):
                # TODO: A significant wart is that we have to try to guess whether the string is a
                #       JSON-serialized quantity or a simple string representation of a quantity.
                #       For example: input of "0.9 nanometer" can be passed directly to the
                #       Quantity constructor, but "{"magnitude": 0.9, "units": "nanometer"}" cannot
                #       as it needs to be unwrapped. A better solution would require a better way
                #       of serializing unit-wrapped arrays to JSON
                if "{" in v:
                    deserialized = json.loads(v)
                    return Quantity(
                        deserialized["magnitude"],
                        deserialized["units"],
                    )
                else:
                    return Quantity(v)
            elif isinstance(v, dict):
                return Quantity(v["magnitude"], v["units"])
            else:
                # this cannot be accessed with the current core_schema definition - the types of the
                # `v` argument to this method **happen** to be identical to the supported types in the
                # core_schema. If **either** is changed, this clause may be hit
                raise ValueError(f"Invalid type {type(v)} for Quantity")

        @classmethod
        def __get_pydantic_core_schema__(
            cls,
            source_type: Any,
            handler: GetCoreSchemaHandler,
        ) -> core_schema.CoreSchema:

            validate_schema = core_schema.chain_schema(
                [
                    core_schema.union_schema(
                        [
                            core_schema.is_instance_schema(PintQuantity),
                            core_schema.str_schema(),
                            core_schema.dict_schema(),
                            # any other types that could be accepted by a quantity field?
                        ]
                    ),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            )

            validate_json_schema = core_schema.chain_schema(
                [
                    core_schema.union_schema(
                        [
                            core_schema.str_schema(coerce_numbers_to_str=True),
                            core_schema.dict_schema(),
                        ]
                    ),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            )

            serialize_schema = core_schema.plain_serializer_function_ser_schema(
                cls.serialize,
                info_arg=True,
            )

            return core_schema.json_or_python_schema(
                json_schema=validate_json_schema,
                python_schema=validate_schema,
                serialization=serialize_schema,
            )
else:

    class _QuantityMixin:
        pass


class Quantity(_QuantityMixin, PintQuantity):
    """A value with associated units."""

    def __dask_tokenize__(self):
        return uuid.uuid4().hex

    @staticmethod
    def _dask_finalize(results, func, args, units):
        values = func(results, *args)
        return Quantity(values, units)


@requires_package("openmm")
def _to_openmm(self) -> openmm.unit.Quantity:
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
    _quantity_class = Quantity
    _unit_class = Unit
    _measurement_class = Measurement


DEFAULT_UNIT_REGISTRY = UnitRegistry(get_defaults_path())

unit = DEFAULT_UNIT_REGISTRY

Unit: type[_Unit] = DEFAULT_UNIT_REGISTRY.Unit
Quantity: type[_Quantity] = DEFAULT_UNIT_REGISTRY.Quantity
Measurement: type[_Measurement] = DEFAULT_UNIT_REGISTRY.Measurement

Quantity.to_openmm = _to_openmm  # type: ignore[attr-defined]

if has_pydantic:
    # Re-attach the Pydantic magic to our new Quantity class, which itself was
    # dynamically created by Pint's magic (and lost these methods in the process).
    Quantity.__get_pydantic_core_schema__ = _QuantityMixin.__get_pydantic_core_schema__  # type: ignore[attr-defined]
    Quantity.validate = _QuantityMixin.validate  # type: ignore[attr-defined]
    Quantity.serialize = _QuantityMixin.serialize  # type: ignore[attr-defined]


pint.set_application_registry(DEFAULT_UNIT_REGISTRY)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

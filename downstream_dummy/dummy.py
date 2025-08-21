"""
See openff/toolkit/utils/utils.py
"""

import functools
from collections.abc import Iterable

from openff.units import Quantity, unit


def string_to_quantity(quantity_string) -> str | int | float | Quantity:
    """Attempt to parse a string into a unit.Quantity.

    Note that dimensionless floats and ints are returns as floats or ints, not Quantity objects.
    """

    from tokenize import TokenError

    from pint import UndefinedUnitError

    try:
        quantity = Quantity(quantity_string)
    except (TokenError, UndefinedUnitError):
        return quantity_string

    # TODO: Should intentionally unitless array-likes be Quantity objects
    #       or their raw representation?
    if (quantity.units == unit.dimensionless) and isinstance(quantity.m, int | float):
        return quantity.m
    else:
        return quantity


def convert_all_strings_to_quantity(
    smirnoff_data: dict,
    ignore_keys: Iterable[str] = tuple(),
):
    """
    Traverses a SMIRNOFF data structure, attempting to convert all
    quantity-defining strings into openff.units.unit.Quantity objects.

    Integers and floats are ignored and not converted into a dimensionless
    ``openff.units.unit.Quantity`` object.

    Parameters
    ----------
    smirnoff_data
        A hierarchical dict structured in compliance with the SMIRNOFF spec
    ignore_keys
        A list of keys to skip when converting strings to quantities

    Returns
    -------
    converted_smirnoff_data
        A hierarchical dict structured in compliance with the SMIRNOFF spec,
        with quantity-defining strings converted to openff.units.unit.Quantity objects
    """
    from pint import DefinitionSyntaxError

    if isinstance(smirnoff_data, dict):
        for key, value in smirnoff_data.items():
            if key in ignore_keys:
                smirnoff_data[key] = value
            else:
                smirnoff_data[key] = convert_all_strings_to_quantity(
                    value,
                    ignore_keys=ignore_keys,
                )
        obj_to_return = smirnoff_data

    elif isinstance(smirnoff_data, list):
        for index, item in enumerate(smirnoff_data):
            smirnoff_data[index] = convert_all_strings_to_quantity(
                item,
                ignore_keys=ignore_keys,
            )
        obj_to_return = smirnoff_data

    elif isinstance(smirnoff_data, int) or isinstance(smirnoff_data, float):
        obj_to_return = smirnoff_data

    else:
        try:
            obj_to_return = object_to_quantity(smirnoff_data)
        except (TypeError, DefinitionSyntaxError):
            obj_to_return = smirnoff_data

    return obj_to_return


@functools.singledispatch
def object_to_quantity(object):
    """
    Attempts to turn the provided object into openmm.unit.Quantity(s).

    Can handle float, int, strings, quantities, or iterators over
    the same. Raises an exception if unable to convert all inputs.

    Parameters
    ----------
    object
        The object to convert to a ``openmm.unit.Quantity`` object.

    Returns
    -------
    converted_object

    """
    # If we can't find a custom type, we treat this as a generic iterator.
    return [object_to_quantity(sub_obj) for sub_obj in object]


@object_to_quantity.register(Quantity)
def _(obj):
    return obj


@object_to_quantity.register(str)
def _(obj):
    import pint

    try:
        return string_to_quantity(obj)
    except pint.errors.UndefinedUnitError:
        raise ValueError


@object_to_quantity.register(int)
@object_to_quantity.register(float)
def _(obj):
    return Quantity(obj)


try:
    import openmm

    from openff.units.openmm import from_openmm

    @object_to_quantity.register(openmm.unit.Quantity)
    def _(obj):
        return from_openmm(obj)

except ImportError:
    pass  # pragma: nocover

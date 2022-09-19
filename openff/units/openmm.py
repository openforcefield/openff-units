"""
Functions for converting between OpenFF and OpenMM units
"""
import ast
import operator as op
from typing import TYPE_CHECKING, List, Literal, Union

from openff.utilities import has_package, requires_package

from openff.units import unit
from openff.units.exceptions import (
    MissingOpenMMUnitError,
    NoneQuantityError,
    NoneUnitError,
)
from openff.units.units import Quantity

__all__ = [
    "from_openmm",
    "to_openmm",
    "openmm_unit_to_string",
    "string_to_openmm_unit",
    "ensure_quantity",
]

if has_package("openmm.unit") or TYPE_CHECKING:
    from openmm import unit as openmm_unit


@requires_package("openmm.unit")
def openmm_unit_to_string(input_unit: "openmm_unit.Unit") -> str:
    """
    Convert a openmm.unit.Unit to a string representation.

    Parameters
    ----------
    input_unit : A openmm.unit
        The unit to serialize

    Returns
    -------
    unit_string : str
        The serialized unit.
    """
    if input_unit is None:
        raise NoneUnitError("Input is None, expected an (OpenMM) Unit object.")

    if input_unit == openmm_unit.dimensionless:
        return "dimensionless"

    if input_unit == openmm_unit.dalton:
        return "g/mol"

    # Decompose output_unit into a tuples of (base_dimension_unit, exponent)
    unit_string = ""

    for unit_component in input_unit.iter_base_or_scaled_units():
        unit_component_name = unit_component[0].name
        # Convert, for example "elementary charge" --> "elementary_charge"
        unit_component_name = unit_component_name.replace(" ", "_")
        if unit_component[1] == 1:
            contribution = "{}".format(unit_component_name)
        else:
            contribution = "{}**{}".format(unit_component_name, int(unit_component[1]))
        if unit_string == "":
            unit_string = contribution
        else:
            unit_string += " * {}".format(contribution)

    return unit_string


def _ast_eval(node):
    """
    Performs an algebraic syntax tree evaluation of a unit.

    Parameters
    ----------
    node : An ast parsing tree node

    Raises
    ------
    openff.units.exceptions.MissingOpenMMUnitError
        if the unit is unavailable in OpenMM.
    """

    operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.BitXor: op.xor,
        ast.USub: op.neg,
    }

    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](_ast_eval(node.left), _ast_eval(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](_ast_eval(node.operand))
    elif isinstance(node, ast.Name):
        # see if this is a openmm unit
        try:
            b = getattr(openmm_unit, node.id)
        except AttributeError:
            raise MissingOpenMMUnitError(node.id)
        return b
    # TODO: This toolkit code that had a hack to cover some edge behavior; not clear which tests trigger it
    elif isinstance(node, ast.List):
        return ast.literal_eval(node)
    else:
        raise TypeError(node)


def string_to_openmm_unit(unit_string: str) -> "openmm_unit.Unit":
    """
    Deserializes a openmm.unit.Quantity from a string representation, for
    example: "kilocalories_per_mole / angstrom ** 2"


    Parameters
    ----------
    unit_string : dict
        Serialized representation of a openmm.unit.Quantity.

    Returns
    -------
    output_unit: openmm.unit.Quantity
        The deserialized unit from the string

    Raises
    ------
    openff.units.exceptions.MissingOpenMMUnitError
        if the unit is unavailable in OpenMM.
    """
    if unit_string == "standard_atmosphere":
        return openmm_unit.atmosphere

    output_unit = _ast_eval(ast.parse(unit_string, mode="eval").body)
    return output_unit


@requires_package("openmm.unit")
def from_openmm(openmm_quantity: "openmm_unit.Quantity") -> Quantity:
    """Convert an OpenMM ``Quantity`` to an OpenFF ``Quantity``

    :class:`openmm.unit.quantity.Quantity` from OpenMM and
    :class:`openff.units.Quantity` from this package both represent a numerical
    value with units.
    """
    if openmm_quantity is None:
        raise NoneQuantityError("Input is None, expected an (OpenMM) Quantity object.")

    if isinstance(openmm_quantity, List):
        openmm_quantity = openmm_unit.Quantity(openmm_quantity)
    openmm_unit_ = openmm_quantity.unit
    openmm_value = openmm_quantity.value_in_unit(openmm_unit_)

    target_unit = openmm_unit_to_string(openmm_unit_)
    target_unit = unit.Unit(target_unit)

    return openmm_value * target_unit


@requires_package("openmm.unit")
def to_openmm(quantity: Quantity) -> "openmm_unit.Quantity":
    """Convert an OpenFF ``Quantity`` to an OpenMM ``Quantity``

    :class:`openmm.unit.quantity.Quantity` from OpenMM and
    :class:`openff.units.Quantity` from this package both represent a numerical
    value with units. The units available in the two packages differ; when a
    unit is missing from the target package, the resulting quantity will be in
    base units (kg/m/s/A/K/mole), which are shared between both packages. This
    may cause the resulting value to be slightly different to the input due to
    the limited precision of floating point numbers.
    """
    if quantity is None:
        raise NoneQuantityError("Input is None, expected an (OpenFF) Quantity object.")

    def to_openmm_inner(quantity) -> "openmm_unit.Quantity":
        value = quantity.m

        unit_string = str(quantity.units._units)
        openmm_unit_ = string_to_openmm_unit(unit_string)

        return value * openmm_unit_

    try:
        return to_openmm_inner(quantity)
    except MissingOpenMMUnitError:
        return to_openmm_inner(quantity.to_base_units())


@requires_package("openmm.unit")
def _ensure_openmm_quantity(
    unknown_quantity: Union[Quantity, "openmm_unit.Quantity"]
) -> "openmm_unit.Quantity":
    if "openmm" in str(type(unknown_quantity)):
        from openmm import unit as openmm_unit

        if isinstance(unknown_quantity, openmm_unit.Quantity):
            return unknown_quantity
        else:
            raise ValueError(
                f"Failed to process input of type {type(unknown_quantity)}."
            )
    elif isinstance(unknown_quantity, Quantity):
        return to_openmm(unknown_quantity)
    else:
        from openmm import unit as openmm_unit

        try:
            return openmm_unit.Quantity(
                unknown_quantity,
                openmm_unit.dimensionless,
            )
        except Exception as e:
            raise ValueError(
                f"Failed to process input of type {type(unknown_quantity)}."
            ) from e


def _ensure_openff_quantity(
    unknown_quantity: Union[Quantity, "openmm_unit.Quantity"]
) -> Quantity:
    if isinstance(unknown_quantity, Quantity):
        return unknown_quantity
    elif "openmm" in str(type(unknown_quantity)):
        from openmm import unit as openmm_unit

        if isinstance(unknown_quantity, openmm_unit.Quantity):
            return from_openmm(unknown_quantity)
        else:
            raise ValueError(
                f"Failed to process input of type {type(unknown_quantity)}."
            )
    else:
        try:
            return unit.Quantity(  # type: ignore
                unknown_quantity,
                unit.dimensionless,
            )
        except Exception as e:
            raise ValueError(
                f"Failed to process input of type {type(unknown_quantity)}."
            ) from e


def ensure_quantity(
    unknown_quantity: Union[Quantity, "openmm_unit.Quantity"],
    type_to_ensure: Literal["openmm", "openff"],
) -> Union[Quantity, "openmm_unit.Quantity"]:
    if type_to_ensure == "openmm":
        return _ensure_openmm_quantity(unknown_quantity)
    elif type_to_ensure == "openff":
        return _ensure_openff_quantity(unknown_quantity)
    else:
        raise ValueError(
            f"Unsupported `type_to_ensure` found. Given {type_to_ensure}, "
            "expected 'openff' or 'openmm'."
        )

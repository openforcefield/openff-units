import ast
import operator as op
import warnings
from typing import TYPE_CHECKING, List

from openff.utilities import has_package, requires_package

from openff.units import unit

if has_package("openmm.unit") or TYPE_CHECKING:
    from openmm import unit as openmm_unit
elif has_package("simtk.unit"):
    warnings.warn(
        "Found units module in simtk namespace, not openmm. Use openff.units.simtk instead."
    )


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
        b = getattr(openmm_unit, node.id)
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
    """
    if unit_string == "standard_atmosphere":
        return openmm_unit.atmosphere

    output_unit = _ast_eval(ast.parse(unit_string, mode="eval").body)  # type: ignore
    return output_unit


@requires_package("openmm.unit")
def from_openmm(openmm_quantity: "openmm_unit.Quantity"):
    if isinstance(openmm_quantity, List):
        openmm_quantity = openmm_unit.Quantity(openmm_quantity)
    openmm_unit_ = openmm_quantity.unit
    openmm_value = openmm_quantity.value_in_unit(openmm_unit_)

    target_unit = openmm_unit_to_string(openmm_unit_)
    target_unit = unit.Unit(target_unit)

    return openmm_value * target_unit


@requires_package("openmm.unit")
def to_openmm(quantity) -> "openmm_unit.Quantity":
    value = quantity.m

    unit_string = str(quantity.units._units)
    openmm_unit_ = string_to_openmm_unit(unit_string)

    return value * openmm_unit_

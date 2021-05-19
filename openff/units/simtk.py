from typing import TYPE_CHECKING, List

from openff.utilities import requires_package

if TYPE_CHECKING:
    from simtk import unit as simtk_unit


@requires_package("simtk.unit")
def unit_to_string(input_unit):
    """
    Serialize a simtk.unit.Unit and return it as a string.

    Parameters
    ----------
    input_unit : A simtk.unit
        The unit to serialize

    Returns
    -------
    unit_string : str
        The serialized unit.
    """
    from simtk import unit as simtk_unit

    if input_unit == simtk_unit.dimensionless:
        return "dimensionless"

    # Decompose output_unit into a tuples of (base_dimension_unit, exponent)
    unit_string = None

    for unit_component in input_unit.iter_base_or_scaled_units():
        unit_component_name = unit_component[0].name
        # Convert, for example "elementary charge" --> "elementary_charge"
        unit_component_name = unit_component_name.replace(" ", "_")
        if unit_component[1] == 1:
            contribution = "{}".format(unit_component_name)
        else:
            contribution = "{}**{}".format(unit_component_name, int(unit_component[1]))
        if unit_string is None:
            unit_string = contribution
        else:
            unit_string += " * {}".format(contribution)

    return unit_string


@requires_package("simtk.unit")
def from_simtk(simtk_quantity: "simtk_unit.Quantity"):
    """
    Convert a SimTK (OpenMM) Quantity to a pint Quantity.

    """
    from simtk import unit as simtk_unit

    from openff.units import unit

    if isinstance(simtk_quantity, List):
        simtk_quantity = simtk_unit.Quantity(simtk_quantity)
    openmm_unit = simtk_quantity.unit
    openmm_value = simtk_quantity.value_in_unit(openmm_unit)

    target_unit = unit_to_string(openmm_unit)
    target_unit = unit.Unit(target_unit)

    return openmm_value * target_unit

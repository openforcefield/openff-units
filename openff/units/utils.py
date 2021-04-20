import os
from typing import TYPE_CHECKING, List

from openff.utilities.utils import requires_package

if TYPE_CHECKING:
    from simtk import unit as simtk_unit


def get_defaults_path():
    """Get the full path to the defaults.txt file"""
    from pkg_resources import resource_filename

    fn = resource_filename("openff.units", os.path.join("data", "defaults.txt"))

    return fn


@requires_package("simtk.unit")
@requires_package("openff.toolkit")
def from_simtk(simtk_quantity: "simtk_unit.Quantity"):
    """
    Convert a SimTK (OpenMM) Quantity to a pint Quantity.

    """
    from openff.toolkit.utils.utils import unit_to_string
    from simtk import unit as simtk_unit

    from openff.units import unit

    if isinstance(simtk_quantity, List):
        simtk_quantity = simtk_unit.Quantity(simtk_quantity)
    openmm_unit = simtk_quantity.unit
    openmm_value = simtk_quantity.value_in_unit(openmm_unit)

    target_unit = unit_to_string(openmm_unit)
    target_unit = unit.Unit(target_unit)

    return openmm_value * target_unit

import pickle

import pytest
from simtk import unit as simtk_unit

from openff.units import unit
from openff.units.simtk import from_simtk

simtk_quantitites = [
    4.0 * simtk_unit.nanometer,
    5.0 * simtk_unit.angstrom,
    1.0 * simtk_unit.elementary_charge,
]

pint_quantities = [
    4.0 * unit.nanometer,
    5.0 * unit.angstrom,
    1.0 * unit.elementary_charge,
]


def test_pickle_type():
    """Test pickle-based serialization

    See:
      * https://github.com/hgrecco/pint/issues/1017
      * https://github.com/openforcefield/openff-evaluator/pull/341

    """

    x = 1.0 * unit.kelvin
    y = pickle.loads(pickle.dumps(x))

    assert x == y


@pytest.mark.parametrize(
    "simtk_quantity,pint_quantity",
    [(s, p) for s, p in zip(simtk_quantitites, pint_quantities)],
)
def test_simtk_to_pint(simtk_quantity, pint_quantity):
    """Test conversion from SimTK Quantity to pint Quantity."""
    converted_pint_quantity = from_simtk(simtk_quantity)

    assert pint_quantity == converted_pint_quantity

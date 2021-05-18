import pickle

import pytest
from openff.utilities.testing import skip_if_missing
from openff.utilities.utilities import has_package

from openff.units import unit
from openff.units.simtk import from_simtk

if has_package("simtk.unit"):
    from simtk import unit as simtk_unit

    simtk_quantitites = [
        4.0 * simtk_unit.nanometer,
        5.0 * simtk_unit.angstrom,
        1.0 * simtk_unit.elementary_charge,
        0.5 * simtk_unit.erg,
        1.0 * simtk_unit.dimensionless,
    ]

    pint_quantities = [
        4.0 * unit.nanometer,
        5.0 * unit.angstrom,
        1.0 * unit.elementary_charge,
        0.5 * unit.erg,
        1.0 * unit.dimensionless,
    ]
else:
    simtk_quantitites = []
    pint_quantities = []


class TestPickle:
    """Test pickle-based serialization of Quantity, Unit, and Measurement objects

    See:
      * https://github.com/hgrecco/pint/issues/1017
      * https://github.com/openforcefield/openff-evaluator/pull/341

    """

    def test_pickle_unit(self):
        x = unit.kelvin
        y = pickle.loads(pickle.dumps(x))

        assert x == y

    def test_pick_quantity(self):
        x = 1.0 * unit.kelvin
        y = pickle.loads(pickle.dumps(x))

        assert x == y

    @skip_if_missing("uncertainties")
    def test_pickle_quantity(self):
        x = (1.0 * unit.kelvin).plus_minus(0.05)
        y = pickle.loads(pickle.dumps(x))

        assert x.value == y.value and x.error == y.error


@skip_if_missing("simtk.unit")
@pytest.mark.parametrize(
    "simtk_quantity,pint_quantity",
    [(s, p) for s, p in zip(simtk_quantitites, pint_quantities)],
)
def test_simtk_to_pint(simtk_quantity, pint_quantity):
    """Test conversion from SimTK Quantity to pint Quantity."""
    converted_pint_quantity = from_simtk(simtk_quantity)

    assert pint_quantity == converted_pint_quantity

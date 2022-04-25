import pickle

import pytest
from openff.utilities.testing import skip_if_missing

from openff.units import unit


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


class TestCompChemUnits:
    """Test some non-standard units used in comp chem stacks."""

    @pytest.mark.parametrize(
        "shorthand_string,full_string",
        [
            (
                "2000.0 * kilocalories_per_mole/angstrom**2",
                "2000.0 * kilocalories/mole/angstrom**2",
            ),
            (
                "2000.0 * kilocalorie_per_mole/angstrom**2",
                "2000.0 * kilocalorie/mole/angstrom**2",
            ),
            (
                "2000.0 * kilojoules_per_mole/angstrom**2",
                "2000.0 * kilojoules/mole/angstrom**2",
            ),
            (
                "2000.0 * kilojoule_per_mole/angstrom**2",
                "2000.0 * kilojoule/mole/angstrom**2",
            ),
        ],
    )
    def test_parse_molar_units_string(self, shorthand_string, full_string):
        assert unit.Quantity(shorthand_string) == unit.Quantity(full_string)

    def test_timestep_creation(self):
        # basic sanity check, can I make the unit and does it serialize
        q = 10 * unit.timestep

        assert q.m == 10
        assert str(q) == "10 timestep"

    def test_timestep_compatibility(self):
        # timesteps aren't a form of time
        q = 20 * unit.timestep

        assert not q.is_compatible_with(10 * unit.picosecond)

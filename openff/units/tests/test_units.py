import pickle

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

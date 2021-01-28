"""
Unit and regression test for the openff package.
"""

import pickle

from openff.units import unit


def test_pickle_type():
    """Test pickle-based serialization

    See:
      * https://github.com/hgrecco/pint/issues/1017
      * https://github.com/openforcefield/openff-evaluator/pull/341

    """

    x = 1.0 * unit.kelvin
    y = pickle.loads(pickle.dumps(x))

    assert x == y

import pytest
from openff.utilities.testing import skip_if_missing

from openff.units.elements import MASSES, SYMBOLS


@skip_if_missing("openmm.unit")
@pytest.mark.parametrize(
    "atomic_number",
    [1, 2],
)
def test_openmm_parity(atomic_number):
    from openmm.app.element import Element

    openmm_element = Element.getByAtomicNumber(atomic_number)

    assert MASSES[atomic_number].m == openmm_element.mass._value
    assert SYMBOLS[atomic_number] == openmm_element.symbol

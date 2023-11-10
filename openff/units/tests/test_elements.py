import random

import pytest
from openff.utilities.testing import skip_if_missing

from openff.units.elements import MASSES, NUMBERS, SYMBOLS


@skip_if_missing("openmm.unit")
@pytest.mark.parametrize("atomic_number", [*range(1, 100)])
def test_openmm_parity(atomic_number):
    from openmm.app.element import Element

    openmm_element = Element.getByAtomicNumber(atomic_number)

    assert MASSES[atomic_number].m == openmm_element.mass._value
    assert SYMBOLS[atomic_number] == openmm_element.symbol


def test_basic():
    assert MASSES[1].m == pytest.approx(1.007947)
    assert MASSES[6].m == pytest.approx(12.01078)

    assert SYMBOLS[1] == "H"
    assert SYMBOLS[6] == "C"

    assert NUMBERS["Cl"] == 17
    assert NUMBERS["Cf"] == 98


def test_symbol_roundtrip():
    number = random.randrange(1, 100)

    assert NUMBERS[SYMBOLS[number]] == number

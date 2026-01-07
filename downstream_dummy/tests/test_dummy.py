import pytest
from dummy import object_to_quantity

from openff.units import Quantity, Unit


def test_function_can_be_defined():
    """
    Just make sure a function can be defined using these classes.

    Safeguard against i.e. https://github.com/openforcefield/openff-toolkit/issues/1632

    Type checkers might not be happy.
    """

    def dummy_function(
        unit: Unit,
        quantity: Quantity,
        extra: Unit | Quantity | str | None = None,
    ):
        return f"{unit} {quantity} {extra}"


@pytest.mark.parametrize(
    "input, output",
    [
        ("1.0 * kilocalories_per_mole", Quantity(1.0, "kilocalories_per_mole")),
        (Quantity("2.0 * angstrom"), Quantity(2.0, "angstrom")),
        (3.0 * Unit("nanometer"), Quantity(3.0, "nanometer")),
        (4, Quantity(4.0)),
        (5.0, Quantity(5.0)),
    ],
)
def test_object_to_quantity(input, output):
    assert object_to_quantity(input) == output

import pytest
from dummy import object_to_quantity
from pint import Quantity as PintQuantity

from openff.units import Quantity, Unit, unit


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


def test_pydantic_model():
    pydantic = pytest.importorskip("pydantic")

    from typing import Annotated

    from pydantic_pint import PydanticPintQuantity

    from openff.units.units import Quantity

    class DummyModel(pydantic.BaseModel):
        quantity: Annotated[PintQuantity, PydanticPintQuantity("kilocalories_per_mole", ureg=unit)]

    model = DummyModel(quantity=Quantity("1.0 * kilocalories_per_mole"))

    assert DummyModel.model_validate(model.model_dump()).quantity == Quantity(
        "1.0 * kilocalories_per_mole"
    )


def test_pydantic_json():
    pydantic = pytest.importorskip("pydantic")

    from typing import Annotated

    from pydantic_pint import PydanticPintQuantity

    class DummyModel(pydantic.BaseModel):
        quantity: Annotated[PintQuantity, PydanticPintQuantity("kilocalories_per_mole", ureg=unit)]

    model = DummyModel(quantity="1.0 * kilocalories_per_mole")

    assert DummyModel.model_validate_json(model.model_dump_json()).quantity == Quantity(
        "1.0 * kilocalories_per_mole"
    )

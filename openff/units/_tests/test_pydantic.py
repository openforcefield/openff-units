import pytest
from pydantic import BaseModel

from openff.units import Quantity, unit


def test_model_definition():
    """Just define a Pydantic model, which will crash if the schema is bad."""

    class MyModel(BaseModel):
        x: Quantity


@pytest.mark.parametrize(
    "value",
    [
        1.0 * unit.angstrom,
        Quantity("1.0 angstrom"),
        "1.0 angstrom",
        {"magnitude": 1.0, "units": "angstrom"},
    ],
)
def test_basic_field_validation(value):
    class MyModel(BaseModel):
        x: Quantity

    stored_value = MyModel(x=value).x

    assert str(stored_value.units) == "angstrom"
    assert stored_value.m_as("angstrom") == 1.0

import numpy
import pytest

from openff.units import Quantity, unit

pydantic = pytest.importorskip("pydantic")


def test_model_definition():
    """Just define a Pydantic model, which will crash if the schema is bad."""

    class MyModel(pydantic.BaseModel):
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
    class MyModel(pydantic.BaseModel):
        x: Quantity

    stored_value = MyModel(x=value).x

    assert str(stored_value.units) == "angstrom"
    assert stored_value.m_as("angstrom") == 1.0


@pytest.mark.parametrize("serialize_with", ["python", "json"])
def test_model_roundtrip(serialize_with):
    """Test that a model can be round-tripped in Python."""

    class MyModel(pydantic.BaseModel):
        x: Quantity
        y: Quantity
        z: Quantity

    model = MyModel(
        x=1.0 * unit.angstrom,
        y=[2, 3] * unit.amu,
        z={"magnitude": 299.99, "units": "kelvin"},
    )

    match serialize_with:
        case "json":
            model_as_json = model.model_dump_json()
            new_model = MyModel.model_validate_json(model_as_json)
        case "python":
            model_as_dict = model.model_dump()
            new_model = MyModel.model_validate(model_as_dict)

    assert new_model.x == Quantity(1.0, unit.angstrom), model.model_dump_json()
    assert (new_model.y == Quantity([2, 3], unit.amu)).all()
    assert type(new_model.y.m) is not list
    assert type(new_model.y.m) is numpy.ndarray
    assert new_model.z == Quantity(299.99, unit.kelvin)


@pytest.mark.parametrize("serialize_with", ["python", "json"])
def test_different_iterables(serialize_with):
    class MyModel(pydantic.BaseModel):
        a: Quantity
        b: Quantity
        c: Quantity

    model = MyModel(
        a=(300.0, 300.1) * unit.kelvin,
        b=[12.011, 1.008, 1.008, 0.0] * unit.amu,
        c=4.0 * numpy.eye(3) * unit.angstrom,
    )

    match serialize_with:
        case "json":
            model_as_json = model.model_dump_json()
            new_model = MyModel.model_validate_json(model_as_json)
        case "python":
            model_as_dict = model.model_dump()
            new_model = MyModel.model_validate(model_as_dict)

    assert new_model.a.shape == (2,)
    assert new_model.b.shape == (4,)
    assert new_model.c.shape == (3, 3)

    assert str(new_model.a.units) == "kelvin"
    assert str(new_model.b.units) == "unified_atomic_mass_unit"
    assert str(new_model.c.units) == "angstrom"

    assert new_model.a[1].m == 300.1
    assert new_model.b[0].m == 12.011
    assert new_model.b[-1].m == 0.0
    assert new_model.c[2, 2].m == 4.0

from pydantic import BaseModel

from openff.units import Quantity


def test_model_definition():
    """Just define a Pydantic model, which will crash if the schema is bad."""

    class MyModel(BaseModel):
        x: Quantity

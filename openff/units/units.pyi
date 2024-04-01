from typing import overload

import numpy

class Unit:
    def __init__(self, *args, **kwargs): ...
    def __mul__(self, other: int | float | numpy.ndarray) -> Quantity: ...

class Quantity:
    def __init__(self, *args, **kwargs): ...
    def to(self, unit: str | Unit = "dimensionless") -> Quantity: ...
    def to_base_units(self, unit: str | Unit = "dimensionless") -> Quantity: ...
    def is_compatible_with(self, unit: str | Unit) -> bool: ...

__all__ = [
    "MissingOpenMMUnitError",
    "NoneQuantityError",
    "NoneUnitError",
]


class MissingOpenMMUnitError(Exception):
    """Raised when a unit cannot be converted to an equivalent OpenMM unit"""


class NoneQuantityError(Exception):
    """Raised when attempting to convert `None` between unit packages as a quantity object"""


class NoneUnitError(Exception):
    """Raised when attempting to convert `None` between unit packages as a unit object"""

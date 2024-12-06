"""
Registry of units provided by OpenFF Units.

``unit`` may be used similarly to a module. It makes constants and units of
measure available as attributes. Available units can be found in the
:download:`constants <../../../openff/units/data/constants.txt>` and
:download:`defaults <../../../openff/units/data/defaults.txt>` data files.
"""

import importlib
from types import ModuleType
from typing import TYPE_CHECKING

from openff.units._version import get_versions

if TYPE_CHECKING:
    # Type checkers can't see lazy-imported objects
    from openff.units.openmm import ensure_quantity
    from openff.units.units import (  # type: ignore[attr-defined]
        DEFAULT_UNIT_REGISTRY,
        Measurement,
        Quantity,
        Unit,
        UnitRegistry,
    )


versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]

__all__ = [
    "Measurement",
    "Quantity",
    "Unit",
    "ensure_quantity",
    "unit",
]

_objects: dict[str, str] = {
    "ensure_quantity": "openff.units.openmm",
    "Measurement": "openff.units.units",
    "Unit": "openff.units.units",
    "UnitRegistry": "openff.units.units",
    "Quantity": "openff.units.units",
    "DEFAULT_UNIT_REGISTRY": "openff.units.units",
    "unit": "openff.units.units",
}


def __getattr__(name) -> ModuleType:
    """
    Lazily import objects from submodules.

    Taken from openff/toolkit/__init__.py
    """
    module = _objects.get(name)
    if module is not None:
        try:
            return importlib.import_module(module).__dict__[name]
        except ImportError as error:
            raise ImportError from error

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Add _objects to dir()."""
    keys = (*globals().keys(), *_objects.keys())
    return sorted(keys)

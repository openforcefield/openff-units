from openff.units._version import get_versions
from openff.units.openmm import ensure_quantity
from openff.units.units import (  # type: ignore[attr-defined]
    DEFAULT_UNIT_REGISTRY,
    Measurement,
    Quantity,
    Unit,
    UnitRegistry,
)

__all__ = [
    "unit",
    "Quantity",
    "Measurement",
    "Unit",
    "ensure_quantity",
]

unit: UnitRegistry = DEFAULT_UNIT_REGISTRY
"""
Registry of units provided by OpenFF Units.

``unit`` may be used similarly to a module. It makes constants and units of
measure available as attributes. Available units can be found in the
:download:`constants <../../../openff/units/data/constants.txt>` and
:download:`defaults <../../../openff/units/data/defaults.txt>` data files.
"""

# Handle versioneer
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions

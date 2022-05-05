from openff.units._version import get_versions  # type: ignore
from openff.units.units import DEFAULT_UNIT_REGISTRY, Measurement, Quantity, Unit

__all__ = [
    "unit",
    "Quantity",
    "Measurement",
    "Unit",
]

unit = DEFAULT_UNIT_REGISTRY
"""
Registry of units provided by OpenFF Units.

``unit`` may be used similarly to a module. It exports
"""

# Handle versioneer
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions

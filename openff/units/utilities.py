"""
Utility methods for OpenFF Units
"""

from openff.utilities import get_data_file_path

__all__ = [
    "get_defaults_path",
]


def get_defaults_path() -> str:
    """Get the full path to the ``defaults.txt`` file"""
    return get_data_file_path("defaults.txt", "openff.units")

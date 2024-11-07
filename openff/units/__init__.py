"""
Registry of units provided by OpenFF Units.

``unit`` may be used similarly to a module. It makes constants and units of
measure available as attributes. Available units can be found in the
:download:`constants <../../../openff/units/data/constants.txt>` and
:download:`defaults <../../../openff/units/data/defaults.txt>` data files.
"""
#
# from openff.units._version import get_versions
#
# versions = get_versions()
# __version__ = versions["version"]
# __git_revision__ = versions["full-revisionid"]

from importlib.metadata import version

__version__ = version("openff.units")

"""
openff-units
A common units module for the OpenFF software stack
"""

# Add imports here
from .units import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

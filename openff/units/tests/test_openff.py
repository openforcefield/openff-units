"""
Unit and regression test for the openff package.
"""

import sys

import pytest

# Import package, test suite, and other packages as needed
import openff


def test_openff_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "openff" in sys.modules

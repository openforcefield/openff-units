"""
Unit and regression test for the openff package.
"""

# Import package, test suite, and other packages as needed
import openff
import pytest
import sys

def test_openff_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "openff" in sys.modules

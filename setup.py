"""
openff-units
A common units module for the OpenFF software stack
"""

from setuptools import find_namespace_packages, setup

import versioneer

short_description = __doc__.split("\n")

long_description = open("README.md").read()


setup(
    name="openff-units",
    author="Open Force Field Initiative",
    author_email="info@openforcefield.org",
    description=short_description[0],
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="MIT",
    packages=find_namespace_packages(include=["openff.*"]),
    package_data={"openff.units": ["py.typed"]},
    include_package_data=True,
    setup_requires=[],
)

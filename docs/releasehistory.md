# Release History

Releases follow versioning as described in
[PEP440](https://www.python.org/dev/peps/pep-0440/#final-releases), where

* `major` increments denote a change that may break API compatibility with previous `major` releases
* `minor` increments add features but do not break API compatibility
* `micro` increments represent bugfix releases or improvements in documentation

Please note that all releases prior to a version 1.0.0 are considered pre-releases and many API changes will come before a stable release.

## 0.3.1

### Behavior changes

* #120 Removes caching of unit registries
* #114 Drops support for Python 3.10

### Behavior changes

* #117 Fixes annotations in a stub file

### Documentation improvements

* #112 Documents quirk when running tests in parallel with `pytest-xdist`


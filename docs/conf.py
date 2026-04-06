# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from importlib.util import find_spec as find_import_spec

sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "OpenFF Units"
copyright = "2022, The Open Force Field Initiative"
author = "The Open Force Field Initiative"


# -- General configuration ---------------------------------------------------


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.doctest",
    "myst_parser",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pint": ("https://pint.readthedocs.io/en/stable/", None),
    "openff.toolkit": (
        "https://docs.openforcefield.org/projects/toolkit/en/stable/",
        None,
    ),
    "openff.fragmenter": (
        "https://docs.openforcefield.org/projects/fragmenter/en/stable/",
        None,
    ),
    "openff.interchange": (
        "https://docs.openforcefield.org/projects/interchange/en/stable/",
        None,
    ),
    "openff.qcsubmit": (
        "https://docs.openforcefield.org/projects/qcsubmit/en/stable/",
        None,
    ),
    "openff.evaluator": (
        "https://docs.openforcefield.org/projects/evaluator/en/stable/",
        None,
    ),
    "mdtraj": ("https://www.mdtraj.org/1.9.5/", None),
    "openmm": ("http://docs.openmm.org/latest/api-python/", None),
    "openff.docs": (
        "https://docs.openforcefield.org/en/latest/",
        None,
    ),
}

autosummary_generate = True
autosummary_imported_members = True
autosummary_ignore_module_all = False
autosummary_context = {
    # Modules to exclude from API docs
    "exclude_modules": [
        "openff.units.tests",
        "openff.units.units",
    ]
}

autodoc_default_options = {
    "member-order": "alphabetical",
    "show-inheritance": True,
}
autodoc_preserve_defaults = True
autodoc_inherit_docstrings = False
autodoc_typehints_format = "short"
# Fold the __init__ or __new__ methods into class documentation
autoclass_content = "both"
autodoc_class_signature = "mixed"
# Workaround for autodoc_typehints_format not working for attributes
# see https://github.com/sphinx-doc/sphinx/issues/10290#issuecomment-1079740009
python_use_unqualified_type_names = True

napoleon_google_docstring = True
napoleon_use_param = False
napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_preprocess_types = True

myst_enable_extensions = [
    "deflist",
    "smartquotes",
    "replacements",
    "dollarmath",
    "colon_fence",
]

# sphinx-notfound-page
# https://github.com/readthedocs/sphinx-notfound-page
# Renders a 404 page with absolute links

if find_import_spec("notfound"):
    extensions.append("notfound.extension")

    notfound_urls_prefix = "/projects/toolkit/en/stable/"
    notfound_context = {
        "title": "404: File Not Found",
        "body": f"""
    <h1>404: File Not Found</h1>
    <p>
        Sorry, we couldn't find that page. This often happens as a result of
        following an outdated link. Please check the
        <a href="{notfound_urls_prefix}">latest stable version</a>
        of the docs, unless you're sure you want an earlier version, and
        try using the search box or the navigation menu on the left.
    </p>
    <p>
    </p>
    """,
    }

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
extensions.append("openff_sphinx_theme")
html_theme = "openff_sphinx_theme"

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
html_sidebars = {
    "**": ["globaltoc.html", "searchbox.html"],
}

# Theme options are theme-specific and customize the look and feel of a
# theme further.
html_theme_options = {
    # Repository integration
    # Set the repo url for the link to appear
    "repo_url": "https://github.com/openforcefield/openff-units",
    # The name of the repo. If must be set if repo_url is set
    "repo_name": "openff-units",
    # Must be one of github, gitlab or bitbucket
    "repo_type": "github",
    # Colour for sidebar captions and other accents. One of
    # openff-blue, openff-toolkit-blue, openff-dataset-yellow,
    # openff-evaluator-orange, aquamarine, lilac, amaranth, grape,
    # violet, pink, pale-green, green, crimson, eggplant, turquoise,
    # or a tuple of three ints in the range [0, 255] corresponding to
    # a position in RGB space.
    "color_accent": "crimson",
    "html_minify": False,
    "html_prettify": False,
    "css_minify": False,
    "globaltoc_depth": 2,
    "globaltoc_include_local": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

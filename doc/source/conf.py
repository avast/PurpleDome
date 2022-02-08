# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('../../app'))
sys.path.insert(0, os.path.abspath('../..'))

print(sys.path)

# -- Project information -----------------------------------------------------

project = 'Purple Dome'
copyright = '2021, Avast'
author = 'Thorsten Sick'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

autodoc_default_options = {
    'member-order': 'bysource',
}

# Sphinx argparse https://sphinx-argparse.readthedocs.io/en/latest/install.html
extensions += ['sphinxarg.ext']

# UML diagrams https://github.com/alendit/sphinx-pyreverse
extensions += ['sphinx_pyreverse']

# YAML config file documentation https://github.com/Jakski/sphinxcontrib-autoyaml
extensions += ['sphinxcontrib.autoyaml']
autoyaml_level = 5

# Graphviz
extensions += [
    "sphinx.ext.graphviz"
]

# -- GraphViz configuration ----------------------------------
graphviz_output_format = 'svg'

# Pydantic plugin for sphinx. Another way to generate config documentation
# extensions += ['sphinx-pydantic']
# This has bugs and is not properly maintained
# But would be awesome: https://sphinx-pydantic.readthedocs.io/en/latest/

# Properly display command line behaviour https://pypi.org/project/sphinxcontrib.asciinema/
# https://github.com/divi255/sphinxcontrib.asciinema/issues/11
extensions += ['sphinxcontrib.asciinema']

sphinxcontrib_asciinema_defaults = {
    # 'theme': 'solarized-dark',
    # 'preload': 1,
    # 'font-size': '15px',
    'path': 'asciinema',
    'autoplay': 1,
    # 'loop': directives.unchanged,
    'speed': 2,
    'idle-time-limit': 1,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from __future__ import annotations

import inspect
import os
import re
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "abqcy"
copyright = "2023, WANG Hailin"
author = "WANG Hailin"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, os.path.abspath(".."))
extensions = [
    "autoclasstoc",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.linkcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_codeautolink",
    "sphinx_design",
    "hoverxref.extension",
    "autoapi.extension",
]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
]

# AutoAPI configuration
autoapi_dirs = ["../abqcy"]
autoapi_ignore = ["*_version.py"]
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    # 'imported-members',
]
autoapi_template_dir = "_autoapi_templates"

# Default behavior for code block concatenation for sphinx_codeautolink
codeautolink_concat_default = False

# Suppress warnings
suppress_warnings = [
    "app.add_directive",
]

intersphinx_mapping = {
    "jinjia2": ("https://jinja.palletsprojects.com/en/3.0.x/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pytest": ("https://pytest.org/en/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "readthedocs": ("https://docs.readthedocs.io/en/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

# Hoverxref configuration
hoverxref_auto_ref = True
hoverxref_domains = ["py"]
hoverxref_roles = [
    "numref",
    "confval",
    "setting",
    "option",
    "doc",  # Documentation pages
    "term",  # Glossary terms
]
hoverxref_role_types = {
    "doc": "modal",  # for whole docs
    "mod": "modal",  # for Python Sphinx Domain
    "class": "tooltip",  # for Python Sphinx Domain
    "func": "tooltip",  # for Python Sphinx Domain
    "meth": "tooltip",  # for Python Sphinx Domain
    "attr": "tooltip",  # for Python Sphinx Domain
    "exc": "tooltip",  # for Python Sphinx Domain
    "obj": "tooltip",  # for Python Sphinx Domain
    "ref": "tooltip",  # for hoverxref_auto_ref config
    "confval": "tooltip",  # for custom object
    "term": "tooltip",  # for glossaries
    "numref": "tooltip",
}
hoverxref_intersphinx = [
    "numpy",
    "pytest",
    "python",
    "readthedocs",
]

# Show short type hints for user-defined classes and defaults for parameters
add_module_names = False
autodoc_default_options = {
    "undoc-members": False,
}
autodoc_typehints_format = "short"
autoclass_content = "both"
typehints_defaults = "comma"
typehints_document_rtype = False
python_use_unqualified_type_names = True

# Figure numbering
numfig = True

# True to convert the type definitions in the docstrings as references. Defaults to False.
napoleon_preprocess_types = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


# linkcode source
def linkcode_resolve(domain: str, info: dict[str, str | list[str]]):
    """Resolve linkcode source

    Parameters
    ----------
    domain : str
        specifies the language domain the object is in
    info : dict[str, str | list[str]]
        a dictionary with the following keys guaranteed to be present (dependent on the domain)

        - py: module (name of the module), fullname (name of the object)
        - c: names (list of names for the object)
        - cpp: names (list of names for the object)
        - javascript: object (name of the object), fullname (name of the item)

    Returns
    -------
    source url of the object
    """
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    filename = modname.replace(".", "/")
    baseurl = f"https://github.com/haiiliin/abqcy/blob/main/{filename}.py"

    submod = sys.modules.get(modname)
    if submod is None:
        return baseurl

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return baseurl
    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        return baseurl

    return baseurl + f"#L{lineno}-L{lineno + len(source) - 1}"

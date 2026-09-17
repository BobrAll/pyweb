import copy
import os
import sys

project = "Результаты исследований"
copyright = "2026, Александр Бобрусь"
author = "Александр Бобрусь"
extensions = [
    "myst_parser",
    "sphinxcontrib.bibtex",
    "sphinx.ext.mathjax",
]
myst_enable_extensions = ["amsmath", "dollarmath", "fieldlist", "html_admonition", "html_image"]
exclude_patterns = ["_build", "stress/plotly.html"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["stress.css"]
language = "ru"
bibtex_bibfiles = ["../assets/references.bib"]

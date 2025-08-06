# Overview

[![PyPI Downloads](https://static.pepy.tech/badge/pbi-parsers)](https://pepy.tech/projects/pbi-parsers)[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdouglassimonsen%2Fpbi_parsers.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdouglassimonsen%2Fpbi_parsers?ref=badge_shield)

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
[![Coverage Status](https://coveralls.io/repos/github/Sulstice/global-chem/badge.svg?branch=master)](https://coveralls.io/github/Sulstice/global-chem?branch=master)

Based on [Crafting Interpreters](https://timothya.com/pdfs/crafting-interpreters.pdf). Library provides lexers, parsers, and formatters for DAX and Power Query (M) languages. Designed to support code introspection and analysis, not execution. This enables developement of [ruff](https://github.com/astral-sh/ruff)-equivalent tools for DAX and Power Query. It also enables extracting metadata from DAX and Power Query code, such PQ source types (Excel, SQL, etc.) and DAX lineage dependencies.

For more information, see the [docs](https://douglassimonsen.github.io/pbi_parsers/)

# Installation

```shell
python -m pip install pbi_parsers
```

# Dev Instructions


## Set Up

```shell
python -m venv venv
venv\Scripts\activate
python -m pip install .
pre-commit install
```


# Running the Documentation Server

```shell
python -m pip install .[docs]
mkdocs serve -f docs/mkdocs.yml
```

## Deploy docs to Github Pages

```shell
mkdocs  gh-deploy --clean -f docs/mkdocs.yml
```

## Testing

```shell

pip install -e .
```

# Build Wheel

```shell
python -m build .
```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdouglassimonsen%2Fpbi_parsers.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdouglassimonsen%2Fpbi_parsers?ref=badge_large)
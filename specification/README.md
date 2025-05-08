zsh: no matches found: xsdata[cli]# SmartGridready Specification

The _specification_ library contains the classes generated from the SGr XML schema.

The actual XML schema files reside in the separate [SGrSpecifications](https://github.com/SmartGridready/SGrSpecifications) repository .


## Contents

- [Directory Structure](#directory-structure)
- [Build Instructions](#build-instructions)


## Directory Structure

- `pyproject.toml` is the main project configuration file.
- `setup.py` is used to build the library package using _setuptools_.
- `src/sgr_specification` contains the generated sources of the specification, with _sgr_specification_ being the root of the namespace.
  The directory is empty, unless the sources are generated from the XML schema.


## Build Instructions

### Prerequisites

Install _xsdata CLI_:

```bash
pip install xsdata[cli]
```

Check out both the [SGrPython](https://github.com/SmartGridready/SGrPython) and
the [SGrSpecifications](https://github.com/SmartGridready/SGrSpecifications) repositories alongside each other,
e.g. in `SGrSpecifications` and `SGrPython`.


### Generate Sources

Generate specification source code from XML schema:

```bash
cd SGrPython/specification/src
rm -rf ./sgr_specification/v0
xsdata generate ../../../SGrSpecifications/SchemaDatabase/SGr -r --package sgr_specification.v0
```

### Build and Use Package

Create and activate virtual environment:

```bash
cd SGrPython
python -m venv .venv

# On Linux call this:
source ./.venv/bin/activate

# On Windows call this:
.\.venv\Scripts\Activate.ps1
```

Build package and install in virtual environment:

```bash
cd SGrPython/specification
pip install -e .
```

You can use the package `sgr-specification` from within the virtual environment now.

**Note:**
The designated package name `sgr-specification` must not be used until the _PyPI_ administrators have
approved a SmartGridready organization account.


### Clean Up

Deactivate the virtual environment after use:

```bash
cd SGrPython
deactivate
```

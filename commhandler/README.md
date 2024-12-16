# SmartGridready CommHandler

The _commhandler_ library provides the interfaces and drivers to access devices.


## Contents

- [Directory Structure](#directory-structure)
- [Build Instructions](#build-instructions)


## Directory Structure

- `pyproject.toml` is the main project configuration file.
- `setup.py` is used to build the library package using _setuptools_.
- `requirements.txt` contains the dependencies required to use the library.
- `requirements-dev.txt` contains the dependencies required to run tests.
- `src/sgr_commhandler` contains the source code of the library, with _sgr_commhandler_ being the root of the namespace.
- `tests` contains unit and integration tests.
- `examples` contains basic examples of using the library.
  See [SGrPythonSamples](https://github.com/SmartGridready/SGrPythonSamples) for more detailed examples.


## Build Instructions

### Prerequisites

Check out the [SGrPython](https://github.com/SmartGridready/SGrPython) repository, e.g. in `SGrPython`.

Create and activate virtual environment:

```bash
cd SGrPython
python -m venv .venv

# On Linux call this:
source ./.venv/bin/activate

# On Windows call this:
.\.venv\Scripts\Activate.ps1
```

Make sure you have the _specification_ library `SGrSpecificationPythontks4r` installed in your virtual environment.
See [specification](../specification/README.md) for instructions.


### Run Tests

You can run tests using `pytest` while in virtual environment.

It is not necessary to install the package locally, if you only want to run tests.

```bash
cd SGrPython/commhandler
pip install -r requirements-dev.txt

pytest
```


### Build and Use Package

Build package and install in virtual environment:

```bash
cd SGrPython/commhandler
pip install -e .
```

You can use the package `SGrPythontks4r` from within the virtual environment now.

**Note:**
The designated package name `sgr-commhandler` must not be used until the _PyPI_ administrators have
approved a SmartGridready organization account!


### Clean Up

Deactivate the virtual environment after use:

```bash
cd SGrPython
deactivate
```

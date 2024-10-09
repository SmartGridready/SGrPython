# SmartGridready Specification

## Build Specification Package

Install _xsdata CLI_:

```bash
pip install xsdata[cli]
```

Generate specification classes from schema:

```bash
cd ./src
rm -rf ./sgr_specification/v0
xsdata generate ../../../SGrSpecifications/SchemaDatabase/SGr -r --package sgr_specification.v0
```

Build package (for local use in virtual environment):

```bash
pip install -e ./specification
```

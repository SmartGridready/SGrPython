from setuptools import find_packages, setup

setup(
    name="sgr-specification",
    version="2.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/SmartGridready/SGrPython/specification#readme",
    project_urls={
        "Issue Tracker": "https://github.com/SmartGridready/SGrSpecifications/issues",
        "Source": "https://github.com/SmartGridready/SGrSpecifications",
        "Docs": "https://smartgridready.github.io/"
    },
    author="Verein SmartGridready",
    description="SGr Specification",
    long_description="Specification classes generated from XML schema",
    long_description_content_type="text/plain",
)

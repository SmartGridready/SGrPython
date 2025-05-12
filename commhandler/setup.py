from setuptools import setup, find_packages

setup(
    name="sgr-commhandler",
    version="0.4.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/SmartGridready/SGrPython/commhandler#readme",
    project_urls={
        "Issue Tracker": "https://github.com/SmartGridready/SGrPython/issues",
        "Source": "https://github.com/SmartGridready/SGrPython",
        "Docs": "https://smartgridready.github.io/SGrPython/docs/commhandler/"
    },
    author="Verein SmartGridready",
    description="SGr Commhandler",
    long_description="Communication Handler Library",
    long_description_content_type="text/plain",
)

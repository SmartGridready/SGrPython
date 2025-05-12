from setuptools import setup, find_packages

def read_requirements() -> list[str]:
    with open("./requirements.txt", "r") as file:
        return file.read().splitlines()

setup(
    name="sgr-commhandler",
    version="0.4.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    url="https://github.com/SmartGridready/SGrPython/commhandler#readme",
    project_urls={
        "Issue Tracker": "https://github.com/SmartGridready/SGrPython/issues",
        "Source": "https://github.com/SmartGridready/SGrPython",
        "Docs": "https://smartgridready.github.io/SGrPython/docs/commhandler/"
    },
    license="BSD-3",
    license_files=["LICENSE.md"],
    author="Verein SmartGridready",
    description="SGr Commhandler",
    long_description="Communication Handler Library",
    long_description_content_type="text/plain",
    python_requires=">=3.9",
)

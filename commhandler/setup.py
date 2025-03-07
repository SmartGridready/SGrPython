from setuptools import setup, find_packages


def read_requirements() -> list[str]:
    with open("./requirements.txt", "r") as file:
        return file.read().splitlines()


setup(
    name="SGrPythontks4r",  # use SGrPythontks4r until organization has been created, then change to sgr-commhandler
    version="0.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    url="https://github.com/SmartGridready/SGrPython#readme",
    project_urls={
        "Issue Tracker": "https://github.com/SmartGridready/SGrPython/issues",
        "Source": "https://github.com/SmartGridready/SGrPython",
    },
    license="BSD-3",
    license_files=["LICENSE.md"],
    author="Robin Schoch",
    author_email="",
    description="SGr Commhandler",
    long_description="SGr Commhandler Library",
    long_description_content_type="text/plain",
    python_requires=">=3.9",
)

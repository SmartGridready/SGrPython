from setuptools import setup


def read_requirements() -> list[str]:
    with open("./requirements.txt", "r") as file:
        return file.read().splitlines()


setup(
    name='SGrPythontks4r',  # SGrPythontks4r
    use_scm_version={"local_scheme": "no-local-version"},
    setup_requires=["setuptools_scm"],
    packages=[
        "sgr_library",
        "sgr_library.api",
        "sgr_library.validators",
        "sgr_library.converters",
    ],
    install_requires=read_requirements(),
    url="https://github.com/SmartGridready/SGrPython",
    license="BSD",
    author="Robin Schoch",
    author_email='',
    description='SGr Commhandler',
    long_description='SGr Commhandler Library',
    long_description_content_type="text/plain",
    python_requires='>=3.9'
)

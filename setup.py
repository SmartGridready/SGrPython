from setuptools import setup


def read_requirements() -> list[str]:
    with open('/Users/robin/Documents/GitHub/SGrPython/requirements.txt', 'r') as file:
        return file.read().splitlines()


setup(
    name='SGrPythontks4r',
    version='0.1.2',
    packages=['sgr_library', 'sgr_library.generated', 'sgr_library.generated.generic',
              'sgr_library.generated.product', 'sgr_library.generated.communicator',
              'sgr_library.generated.functional_profile', 'sgr_library.api', 'sgr_library.validators',
              'sgr_library.converters'],
    url='https://github.com/robin-schoch/SGrPython',
    license='',
    author='robin',
    author_email='',
    description='',
    install_requires=read_requirements()
)

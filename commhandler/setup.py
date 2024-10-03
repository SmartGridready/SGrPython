from setuptools import setup, find_packages


def read_requirements() -> list[str]:
    with open('./requirements.txt', 'r') as file:
        return file.read().splitlines()


setup(
    name='SGrPythontks4r',  # SGrPythontks4r
    version='0.2.0',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    install_requires=read_requirements(),
    url='https://github.com/SmartGridready/SGrPython#readme',
    project_urls={
        'Issue Tracker': 'https://github.com/SmartGridready/SGrPython/issues',
        'Source': 'https://github.com/SmartGridready/SGrPython'
    },
    license='BSD',
    author='Robin Schoch',
    author_email='',
    description='SGr Commhandler',
    long_description='SGr Commhandler Library',
    long_description_content_type='text/plain',
    python_requires='>=3.9'
)

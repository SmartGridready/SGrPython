from setuptools import setup

# do not configure 'packages', so setuptools uses auto-detection
setup(
    name='SGrSpecificationPythontks4r',  # SGrSpecificationPythontks4r
    version='{{tag}}',
    install_requires=[],
    url='https://github.com/SmartGridready/SGrSpecifications#readme',
    project_urls={
        'Issue Tracker': 'https://github.com/SmartGridready/SGrSpecifications/issues',
        'Source': 'https://github.com/SmartGridready/SGrSpecifications'
    },
    license='BSD',
    author='Robin Schoch',
    author_email='',
    description='SGr Specifications',
    long_description='Specification classes generated from XML schema',
    long_description_content_type='text/plain',
    python_requires='>=3.9'
)

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A package to create OpenStudio models using Python'
LONG_DESCRIPTION = 'A package to create OpenStudio models using Python - EnergyPlus is needed to run the models'

# Setting up
setup(
       # the name must match the folder name 'PyOSModel'
        name="PyOSModel",
        version=VERSION,
        author="Bruno Marc J. Adam",
        author_email="<bmjga@p.me>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'pandas', 'openstudio', 'epw', 'subprocess'],
        keywords=['python', 'openstudio', 'model', 'energyplus', 'building', 'simulation', 'energy', 'efficiency', 'comfort', 'thermal', 'comfort', 'lighting', 'electric equipment', 'people', 'ventilation', 'infiltration', 'HVAC', 'heating', 'occupant', 'occupancy', 'schedule', 'geometry', 'construction', 'material', 'cost', 'output', 'internal loads', 'subsurface', 'origin', 'params', 'utils'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS",
        ]
)
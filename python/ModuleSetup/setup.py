#!/usr/bin/env python3
from setuptools import setup, find_packages
setup(
name = 'MasterModule',
version = '0.1.0',
description = 'Classes of master thesis',
long_description = 'Contains all classes needed for programs of master thesis',
keywords = 'radar, master_thesis',
license = 'GPLv3',
author = 'Gregor Möller',
author_email = 'gregor_moeller@live.de',
url = 'https://github.com/GroovyGregor/master_thesis',
classifiers = 
	['License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	'Programming Language :: Python :: 3.5',
	'Operating System :: OS Independent',
	'Topic :: Scientific / Engineering',
	'Topic :: Scientific/Engineering :: Atmospheric Science',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Topic :: Utilities'],
packages = find_packages(),
install_requires = 
	['numpy',
	'h5py',
	'netCDF4']

)

# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

PACKAGE = 'WindAdapter'
NAME = 'WindAdapter'
VERSION = '0.0.10'
DESCRIPTION = 'Windpy data adapter'
AUTHOR = 'iLampard, RoxanneYang'
URL = 'https://github.com/iLampard/WindAdapter'
LICENSE = 'MIT'

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      url=URL,
      packages=find_packages(),
      package_data={'': ['*.csv']},
      install_requires=[
          'pandas',
          'logbook',
          'python-decouple>=3.0'
      ],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'])

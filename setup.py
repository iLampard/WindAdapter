# -*- coding: utf-8 -*-

import io
import sys

import numpy as np
from setuptools import find_packages
from setuptools import setup

PACKAGE = 'WindAdapter'
NAME = 'WindAdapter'
VERSION = '0.3.6'
DESCRIPTION = 'Windpy data adapter'
AUTHOR = 'iLampard, RoxanneYang, bella21'
URL = 'https://github.com/iLampard/WindAdapter'
LICENSE = 'MIT'

if sys.version_info > (3, 0, 0):
    requirements = "requirements/py3.txt"
else:
    requirements = "requirements/py2.txt"

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      url=URL,
      include_package_data=True,
      packages=find_packages(),
      package_data={'': ['*.csv']},
      install_requires=io.open(requirements, encoding='utf8').read(),
      include_dirs=[np.get_include()],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'])

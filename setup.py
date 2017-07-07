# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup
import os
import sys
import io
import numpy as np

PACKAGE = 'WindAdapter'
NAME = 'WindAdapter'
VERSION = '0.0.15'
DESCRIPTION = 'Windpy data adapter'
AUTHOR = 'iLampard, RoxanneYang'
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
      packages=find_packages(),
      package_data={'': ['*.csv']},
      install_requires=io.open(requirements, encoding='utf8').read(),
      include_dirs=[np.get_include()],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'])

# -*- coding: utf-8 -*-


from WindAdapter.api import get_universe
from WindAdapter.api import factor_load
from WindAdapter.api import factor_help
from WindAdapter.api import factor_details_help

__all__ = ['version',
           'get_universe',
           'factor_load',
           'factor_help',
           'factor_details_help']


def version():
    return __version__

__version__ = '0.0.1'

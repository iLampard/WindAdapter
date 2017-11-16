# -*- coding: utf-8 -*-


from WindAdapter.api import get_universe
from WindAdapter.api import factor_load
from WindAdapter.api import factor_help
from WindAdapter.api import factor_details_help
from WindAdapter.api import reset_data_dict_path

__all__ = ['version',
           'get_universe',
           'factor_load',
           'factor_help',
           'factor_details_help',
           'reset_data_dict_path']


def version():
    return __version__


__version__ = '0.3.0'

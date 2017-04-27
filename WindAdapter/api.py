# -*- coding: utf-8 -*-

import os
import datetime
from WindAdapter.factor_loader import FactorLoader
from WindAdapter.utils import save_data_to_file
from WindAdapter.utils import print_table
from WindAdapter.utils import handle_wind_query_exception
from WindAdapter.custom_logger import CustomLogger
from WindAdapter.data_provider import WindDataProvider
from WindAdapter.helper import WindQueryHelper

LOGGER = CustomLogger()
WIND_DATA_PRODIVER = WindDataProvider()
WIND_QUERY_HELPER = WindQueryHelper()


def reset_log_level(log_level):
    LOGGER.set_level(log_level)


def reset_data_dict_path(path, path_type_abs):
    LOGGER.critical('Reset path of data dict to {}'.format(path))
    os.environ['DATA_DICT_PATH'] = path
    os.environ['DATA_DICT_PATH_TYPE_ABS'] = str(path_type_abs)
    return


@handle_wind_query_exception(LOGGER)
def get_universe(index_id, date=None):
    LOGGER.info('Loading the constituent stocks of index {0} at date {1}'.
                format(index_id, datetime.date.today() if date is None else date))
    ret = WindDataProvider.get_universe(index_id, date)
    LOGGER.info('Number of the loaded constituent stocks is {0}'.format(len(ret)))
    return ret


@handle_wind_query_exception(LOGGER)
def factor_load(start_date, end_date, factor_name, save_file=None, **kwargs):
    LOGGER.info('Loading factor data {0}'.format(factor_name))
    factor_loader = FactorLoader(start_date=start_date,
                                 end_date=end_date,
                                 factor_name=factor_name,
                                 **kwargs)
    ret = factor_loader.load_data()
    LOGGER.info('factor data {0} is loaded '.format(factor_name))
    if save_file:
        save_data_to_file(ret, save_file)
        LOGGER.critical('Data saved in {0}'.format(save_file))
    return ret


def factor_help():
    LOGGER.info('Factors that are available to query')
    data_dict = WIND_QUERY_HELPER.data_dict
    print_table(data_dict['explanation'], name='Data_Dict')


def factor_details_help():
    LOGGER.info('Factors(details) that are available to query')
    data_dict = WIND_QUERY_HELPER.data_dict
    print_table(data_dict, name='Data_Dict')

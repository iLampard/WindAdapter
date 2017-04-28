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
    """
    :param log_level: enum, 可选择'info', 'critical'  'notset'
    :return: 设置WindAdapter函数输出信息的等级， 项目默认为'info'等级
    """
    LOGGER.critical('Reset path of data dict to {0}'.format(log_level))
    LOGGER.set_level(log_level)


def reset_data_dict_path(path, path_type_abs):
    """
    :param path: str, 自定义的data_dict 路径
    :param path_type_abs: str, True: 路径为绝对路径, False: 路径为相对路径
    :return: data_dict的路径被修改
    """
    LOGGER.critical('Reset path of data dict to {0}'.format(path))
    os.environ['DATA_DICT_PATH'] = path
    os.environ['DATA_DICT_PATH_TYPE_ABS'] = str(path_type_abs)
    return


@handle_wind_query_exception(LOGGER)
def get_universe(index_id, date=None):
    """
    :param index_id: str, 可以为指数代码或者'fullA'（指全市场股票），不区分大小写
    :param date: str, optional, YYYYMMDD/YYYY-MM-DD，默认为None，即返回最近交易日的成分股列表
    :return: list, 成分股列表
    """
    LOGGER.info('Loading the constituent stocks of index {0} at date {1}'.
                format(index_id, datetime.date.today() if date is None else date))
    ret = WindDataProvider.get_universe(index_id, date)
    LOGGER.info('Number of the loaded constituent stocks is {0}'.format(len(ret)))
    return ret


@handle_wind_query_exception(LOGGER)
def factor_load(start_date, end_date, factor_name, save_file=None, **kwargs):
    """
    :param start_date: str, 读取因子数据的开始日期
    :param end_date: str, 读取因子数据的结束日期
    :param factor_name: str, 因子名称，不区分大小写
    :param save_file: str, optional, 保存数据的文件名，可写成 '*.csv' 或者 '*.pkl'
    :param kwargs: dict, optional

            freq: str, optional, 因子数据的频率， 可选'M', 'W', 'Q', 'S', 'Y'， 参见enums.py - FreqType
            tenor: str, optional, 因子数据的周期， 对于截面数据（如换手率，收益率），需要给定数据区间(向前)， 可选数字+FreqType， 如'1Q'
            sec_id, str/list, optional, 股票代码或者是指数代码
            output_data_format: enum, optional, 参见enums.py - FreqType
                                MULTI_INDEX_DF: multi-index DataFrame, index=[date, secID], value = factor
                                PITVOT_TABLE_DF: DataFrame, index=date, columns = secID
            is_index: bool, optional, True: 输入的sec_id是指数，实际需要读取的是该指数成分股的因子数据，
                                      False: 直接读取sec_id的因子数据
    :return: pd.DataFrame 整理好的因子数据
    """
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
    """
    :return: 返回定义的数据字典（简易版）
    """
    LOGGER.info('Factors that are available to query')
    data_dict = WIND_QUERY_HELPER.data_dict
    print_table(data_dict['explanation'], name='Data_Dict')
    return


def factor_details_help():
    """
    :return: 返回定义的数据字典（详细版）
    """
    LOGGER.info('Factors(details) that are available to query')
    data_dict = WIND_QUERY_HELPER.data_dict
    print_table(data_dict, name='Data_Dict')
    return

# -*- coding: utf-8 -*-

import pickle
import pandas as pd
from IPython.display import display
import functools


def save_data_to_file(data, save_file_name):
    """
    :param data: pd.DataFrame, data to be saved
    :param save_file_name: str, *.*
    :return:
    """

    save_file_type = save_file_name.split('.')[1]
    if save_file_type == 'csv':
        data.to_csv(save_file_name)
    elif save_file_name == 'pkl':
        pkl_dump_data(data, save_file_name)
    else:
        raise NotImplementedError


def pkl_dump_data(data, pkl_file_name, protocol=-1):
    """
    :param data: any type
    :param pkl_file_name: str, *.pkl
    :param protocol: int, optional, protocol in saving pickle
    :return:
    """
    pkl_file = open(pkl_file_name, 'wb')
    pickle.dump(data, pkl_file, protocol)
    pkl_file.close()
    return


def py_assert(condition, exception_type, msg):
    if not condition:
        raise exception_type(msg)


def handle_wind_query_exception(logger):
    """
    :param logger: logging, a logging object
    :return: decorator, wraps exception loggers
    """

    def decorator(query_func):
        @functools.wraps(query_func)
        def wrapper(*args, **kwargs):
            try:
                return query_func(*args, **kwargs)
            except Exception, e:
                logger.critical('Exception in function {0} -- {1}'.format(query_func.__name__, e))

        return wrapper

    return decorator


def print_table(table, name=None, fmt=None):
    """
    Pretty print a pandas DataFrame.
    Uses HTML output if running inside Jupyter Notebook, otherwise
    formatted text output.
    Parameters
    ----------
    table : pandas.Series or pandas.DataFrame
        Table to pretty-print.
    name : str, optional
        Table name to display in upper left corner.
    fmt : str, optional
        Formatter to use for displaying table elements.
        E.g. '{0:.2f}%' for displaying 100 as '100.00%'.
        Restores original setting after displaying.
    """

    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if fmt is not None:
        prev_option = pd.get_option('display.float_format')
        pd.set_option('display.float_format', lambda x: fmt.format(x))

    if name is not None:
        table.columns.name = name

    display(table)

    if fmt is not None:
        pd.set_option('display.float_format', prev_option)

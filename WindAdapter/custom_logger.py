# -*- coding: utf-8 -*-

# ref: https://github.com/iLampard/AlgoTrading/blob/master/AlgoTrading/Utilities/Logger.py

from logbook import (Logger,
                     StreamHandler,
                     FileHandler,
                     set_datetime_format)
import logbook
import sys
from WindAdapter.enums import LogLevel


class CustomLogger(object):
    def __init__(self,
                 log_level=LogLevel.INFO,
                 format_str='[{record.time:%Y-%m-%d %H:%M:%S}] - {record.channel} - {record.level_name} '
                            '- {record.message}'):
        self.logger = Logger('WindAdapter')
        set_datetime_format('local')
        StreamHandler(sys.stdout, format_string=format_str).push_application()
        FileHandler('WindAdapter.log', bubble=True, format_string=format_str).push_application()
        self.set_level(log_level)

    def set_level(self, log_level):
        if log_level.lower() == LogLevel.INFO:
            self.logger.level = logbook.INFO
        elif log_level.lower() == LogLevel.WARNING:
            self.logger.level = logbook.WARNING
        elif log_level.lower() == LogLevel.CRITICAL:
            self.logger.level = logbook.CRITICAL
        elif log_level.lower() == LogLevel.NOTSET:
            self.logger.level = logbook.NOTSET

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)


# -*- coding: utf-8 -*-

# ref: https://github.com/iLampard/AlgoTrading/blob/master/AlgoTrading/Utilities/Logger.py

import logging
from WindAdapter.enums import LogLevel


class CustomLogger(object):
    def __init__(self, log_level=LogLevel.INFO):
        self.logger = logging.getLogger('WindAdapter')
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        sh = logging.FileHandler('WindAdapter.log')
        ch.setLevel(logging.INFO)
        sh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        sh.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(sh)
        self.set_level(log_level)

    def set_level(self, log_level):
        if log_level.lower() == LogLevel.INFO:
            self.logger.setLevel(logging.INFO)
        elif log_level.lower() == LogLevel.WARNING:
            self.logger.setLevel(logging.WARNING)
        elif log_level.lower() == LogLevel.CRITICAL:
            self.logger.setLevel(logging.CRITICAL)
        elif log_level.lower() == LogLevel.NOTSET:
            self.logger.setLevel(logging.NOTSET)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)

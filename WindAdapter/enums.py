# -*- coding: utf-8 -*-


from enum import Enum
from enum import IntEnum


class StrEnum(str, Enum):
    pass


class FreqType(StrEnum):
    MIN1 = '1'
    MIN5 = '5'
    MIN10 = '10'
    EOD = 'D'
    EOW = 'W'
    EOM = 'M'
    EOQ = 'Q'
    EOSY = 'S'
    EOY = 'Y'


class OutputFormat(IntEnum):
    MULTI_INDEX_DF = 0
    PITVOT_TABLE_DF = 1


class Header(StrEnum):
    NAME = 'name'
    TENOR = 'tenor'
    API = 'api'
    INDICATOR = 'indicator'
    FREQ = 'period'
    PRICEADJ = 'priceadj'
    UNIT = 'unit'
    TRADEDATE = 'tradeDate'
    CYCLE = 'cycle'
    EXPLANATION = 'explanation'
    TYPE = 'type'
    REPORTADJ = 'reportadj'


class WindDataType(IntEnum):
    WSS_TYPE = 0
    WSD_TYPE = 1


class LogLevel(StrEnum):
    INFO = 'info'
    WARNING = 'warining'
    CRITICAL = 'critical'
    NOTSET = 'notset'
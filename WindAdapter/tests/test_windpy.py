# -*- coding: utf-8 -*-

import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

try:
    from WindPy import w
except ImportError:
    pass

from WindAdapter.data_provider import WindDataProvider
from WindAdapter.helper import WindQueryHelper
from WindAdapter.factor_loader import FactorLoader
from WindAdapter.enums import Header
from datetime import (datetime,
                      date)

wind_query_helper = WindQueryHelper()
wind_data_provider = WindDataProvider()

"""
该文件用以测试WindPy接口数据结构是否与从前保持一致，以确保WindAdapter数据处理得以照常进行
"""


class WindData(object):
    def __init__(self, data, codes, error_code, fields, times):
        self.Data = data
        self.Codes = codes
        self.ErrorCode = error_code
        self.Fields = fields
        self.Times = times

    def __eq__(self, other):
        if (self.Data == other.Data
            and self.Codes == other.Codes
            and self.ErrorCode == other.ErrorCode
                and self.Fields == other.Fields and self.Times == other.Times):
            return True
        else:
            return False


class TestDataProvider(unittest.TestCase):
    def test_forward_date(self):
        ref_date = '2017-12-04'
        tenor = ['1b', '2d', '3w', '4m', '5y']
        expected = ['2017-12-04', '2017-12-05', '2017-11-14', '2017-08-07', '2012-12-05']
        calculated = [WindDataProvider.forward_date(ref_date, tenor[i]) for i in range(len(tenor))]
        self.assertEqual(calculated, expected)

        ref_date = '20170101'
        tenor = ['1b', '2d', '3w', '4m', '5y']
        expected = ['2017-01-03', '2017-01-03', '2016-12-13', '2016-09-02', '2012-01-05']
        calculated = [WindDataProvider.forward_date(ref_date, tenor[i], date_format='%Y%m%d') for i in
                      range(len(tenor))]
        self.assertEqual(calculated, expected)

    def test_query_data(self):
        # query_data(api, sec_id, indicator, extra_params=None, start_date=None, end_date=None)
        sec_id = ['000001.SZ', '000002.SZ']
        start_date = '2017-01-03'
        end_date = '2017-01-04'

        # w.wsd && factor_name = 'PB'
        api = 'w.wsd'
        indicator = 'pb_lf'
        raw_data = wind_data_provider.query_data(api, sec_id, indicator, start_date=start_date, end_date=end_date)
        calculated = WindData(data=raw_data.Data,
                              codes=raw_data.Codes,
                              error_code=raw_data.ErrorCode,
                              fields=raw_data.Fields,
                              times=raw_data.Times)
        expected = WindData(data=[[0.8822379112243652, 0.8822379112243652], [2.279218912124634, 2.292412519454956]],
                            codes=['000001.SZ', '000002.SZ'],
                            error_code=0,
                            fields=['PB_LF'],
                            times=[date(2017, 1, 3), date(2017, 1, 4)])
        self.assertEqual(calculated, expected)

        # w.wss && factor_name = 'RETURN'
        api = 'w.wss'
        factor_name = 'RETURN'
        indicator = 'pct_chg_per'
        factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id, is_index=False, tenor='3M')
        main_params, extra_params = wind_query_helper.get_query_params(factor_name)
        extra_params[Header.TENOR.value] = factor_loader._get_enum_value(factor_loader.tenor) \
            if factor_loader.tenor is not None else None
        merged_extra_params = factor_loader._merge_query_params(extra_params, start_date)
        raw_data = wind_data_provider.query_data(api, sec_id, indicator,
                                                 extra_params=merged_extra_params,
                                                 start_date=start_date, end_date=start_date)
        calculated = WindData(data=raw_data.Data,
                              codes=raw_data.Codes,
                              error_code=raw_data.ErrorCode,
                              fields=raw_data.Fields,
                              times=len(raw_data.Times))
        expected = WindData(data=[[0.43859649122806044, -20.177127454755485]],
                            codes=['000001.SZ', '000002.SZ'],
                            error_code=0,
                            fields=['PCT_CHG_PER'],
                            times=1)
        self.assertEqual(calculated, expected)

        # w.wsi && factor_name = 'OHLCV_MIN'
        api = 'w.wsi'
        indicator = 'open,high,low,close,volume'
        start_date = '2017-01-03 09:30:00'
        end_date = '2017-01-03 09:32:00'
        factor_name = 'OHLCV_MIN'
        factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id)
        main_params, extra_params = wind_query_helper.get_query_params(factor_name)
        merged_extra_params = factor_loader._merge_query_params(extra_params, start_date)
        raw_data = wind_data_provider.query_data(api, sec_id, indicator, extra_params=merged_extra_params,
                                                 start_date=start_date, end_date=end_date)
        calculated = WindData(data=raw_data.Data,
                              codes=raw_data.Codes,
                              error_code=raw_data.ErrorCode,
                              fields=raw_data.Fields,
                              times=raw_data.Times)
        expected = WindData(data=[[datetime(2017, 1, 3, 9, 30), datetime(2017, 1, 3, 9, 31),
                                   datetime(2017, 1, 3, 9, 30), datetime(2017, 1, 3, 9, 31)],
                                  ['000001.SZ', '000001.SZ', '000002.SZ', '000002.SZ'],
                                  [8.977128569075722, 8.967274421359942, 19.87384420457807, 19.951211967904893],
                                  [8.977128569075722, 8.977128569075722, 19.970553908736598, 19.970553908736598],
                                  [8.967274421359942, 8.967274421359942, 19.87384420457807, 19.922199056657337],
                                  [8.967274421359942, 8.967274421359942, 19.951211967904893, 19.970553908736598],
                                  [673660L, 433800L, 119900L, 146700L]],
                            codes=['MultiCodes'],
                            error_code=0,
                            fields=['time', 'windcode', 'open', 'high', 'low', 'close', 'volume'],
                            times=[datetime(2017, 1, 3, 9, 30), datetime(2017, 1, 3, 9, 31),
                                   datetime(2017, 1, 3, 9, 30), datetime(2017, 1, 3, 9, 31)])
        self.assertEqual(calculated, expected)

        # # w.wsq && factor_name = 'LIVE'
        api = 'w.wsq'
        indicator = 'rt_open,rt_high,rt_low,rt_last,rt_vol,rt_amt,rt_vol_ratio,rt_pct_chg_5min'
        raw_data = wind_data_provider.query_data(api, sec_id, indicator)
        calculated = WindData(data=len(raw_data.Data),
                              codes=raw_data.Codes,
                              error_code=raw_data.ErrorCode,
                              fields=raw_data.Fields,
                              times=len(raw_data.Times))
        expected = WindData(data=8,
                            codes=['000001.SZ', '000002.SZ'],
                            error_code=0,
                            fields=['RT_OPEN', 'RT_HIGH', 'RT_LOW', 'RT_LAST', 'RT_VOL',
                                    'RT_AMT', 'RT_VOL_RATIO', 'RT_PCT_CHG_5MIN'],
                            times=1)
        self.assertEqual(calculated, expected)

        # # w.wset && factor_name = 'INDUSTRY_WEIGHT_C1'
        api = 'w.wset'
        index_id = '000300.SH'
        short_params = 'windcode=' + index_id
        params = short_params if start_date is None else short_params + ';date=' + str(start_date)
        raw_data = w.wset('IndexConstituent', params)
        calculated = WindData(data=len(raw_data.Data),
                              codes=len(raw_data.Codes),
                              error_code=raw_data.ErrorCode,
                              fields=raw_data.Fields,
                              times=len(raw_data.Times))
        expected = WindData(data=4,
                            codes=300,
                            error_code=0,
                            fields=['date', 'wind_code', 'sec_name', 'i_weight'],
                            times=1)
        self.assertEqual(calculated, expected)

        raw_data = w.wset('IndexConstituent', short_params)
        calculated = WindData(data=len(raw_data.Data),
                              codes=len(raw_data.Codes),
                              error_code=raw_data.ErrorCode,
                              fields=raw_data.Fields,
                              times=len(raw_data.Times))
        expected = WindData(data=4,
                            codes=300,
                            error_code=0,
                            fields=['date', 'wind_code', 'sec_name', 'i_weight'],
                            times=1)
        self.assertEqual(calculated, expected)

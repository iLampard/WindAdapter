# -*- coding: utf-8 -*-

import unittest
import mock
from datetime import datetime
import pandas as pd

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from pandas.util.testing import assert_frame_equal
from WindAdapter.api import (factor_load,
                             get_universe)
from WindAdapter.data_provider import WindDataProvider
from WindAdapter.factor_loader import FactorLoader
from WindAdapter.helper import WindQueryHelper
from WindAdapter.enums import (OutputFormat,
                               FreqType,
                               Header)

wind_query_helper = WindQueryHelper()


class MockWindData(object):
    def __init__(self, data, codes, error_code, fields, times):
        self.Data = data
        self.Codes = codes
        self.ErrorCode = error_code
        self.Fields = fields
        self.Times = times


class TestApi(unittest.TestCase):
    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    def test_factor_load_case1(self, mock_query_data):
        start_date = '2016-01-01'
        end_date = '2016-02-01'
        factor_name = 'PB'
        sec_id = ['000001.SZ', '000002.SZ', '000003.SZ']

        mock_data = MockWindData(data=[[1, 3, 5]],
                                 codes=sec_id,
                                 error_code=0,
                                 fields=['PB'],
                                 times=[datetime(2016, 1, 1),
                                        datetime(2016, 2, 1)])
        mock_query_data.return_value = mock_data

        calculated = factor_load(start_date=start_date,
                                 end_date=end_date,
                                 factor_name=factor_name,
                                 sec_id=sec_id,
                                 output_data_format=OutputFormat.MULTI_INDEX_DF,
                                 is_index=False)

        expected = pd.DataFrame(data=[1, 3, 5, 1, 3, 5],
                                index=pd.MultiIndex.from_product([['2016-01-29', '2016-02-01'],
                                                                  ['000001.SZ', '000002.SZ', '000003.SZ']],
                                                                 names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

        calculated = factor_load(start_date=start_date,
                                 end_date=end_date,
                                 factor_name=factor_name,
                                 sec_id=sec_id,
                                 output_data_format=OutputFormat.PIVOT_TABLE_DF,
                                 is_index=False)
        expected = pd.DataFrame(data=[[1, 3, 5], [1, 3, 5]],
                                columns=['000001.SZ', '000002.SZ', '000003.SZ'],
                                index=['2016-01-29', '2016-02-01'])
        assert_frame_equal(calculated, expected)

    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    @patch('WindAdapter.data_provider.WindDataProvider.biz_days_list')
    @patch('WindAdapter.data_provider.WindDataProvider.forward_date')
    def test_factor_load_case2(self, mock_adv_date, mock_days_list, mock_query_data):
        start_date = '2016-01-01'
        end_date = '2016-02-01'
        factor_name = 'STDQ'
        sec_id = ['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ']

        mock_data = MockWindData(data=[[1, 2, 3, 4]],
                                 codes=sec_id,
                                 error_code=0,
                                 fields=['STDQ'],
                                 times=[datetime(2016, 1, 1)])
        mock_query_data.return_value = mock_data
        mock_days_list.return_value = [datetime(2016, 1, 1), datetime(2016, 2, 1)]
        mock_adv_date.return_value = '2015-09-01'

        calculated = factor_load(start_date=start_date,
                                 end_date=end_date,
                                 factor_name=factor_name,
                                 sec_id=sec_id,
                                 tenor='3M',
                                 output_data_format=OutputFormat.MULTI_INDEX_DF,
                                 is_index=False)
        expected = pd.DataFrame(data=[1, 2, 3, 4, 1, 2, 3, 4],
                                index=pd.MultiIndex.from_product([['2016-01-01', '2016-02-01'],
                                                                  ['000001.SZ', '000002.SZ', '000003.SZ',
                                                                   '000004.SZ']],
                                                                 names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

        calculated = factor_load(start_date=start_date,
                                 end_date=end_date,
                                 factor_name=factor_name,
                                 sec_id=sec_id,
                                 tenor='3M',
                                 output_data_format=OutputFormat.PIVOT_TABLE_DF,
                                 is_index=False)
        expected = pd.DataFrame(data=[[1, 2, 3, 4], [1, 2, 3, 4]],
                                index=['2016-01-01', '2016-02-01'],
                                columns=['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ'])
        assert_frame_equal(calculated, expected)

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

    @patch('WindAdapter.data_provider.WindDataProvider.get_universe')
    def test_get_universe(self, mock_get_universe):
        index_id = 'fullA'
        mock_get_universe.return_value = ['000001.SZ', '000002.SZ', '000003.SZ', 'other codes of fullA']
        expected = ['000001.SZ', '000002.SZ', '000003.SZ', 'other codes of fullA']
        calculated = get_universe(index_id)
        self.assertEqual(calculated, expected)

        index_id = '000905.SH'
        mock_get_universe.return_value = pd.DataFrame(data=[0.228, 0.238, 0.164],
                                                      index=['000006.SZ', '000012.SZ', '000021.SZ'],
                                                      columns=['weight'])
        expected = pd.DataFrame(data=[0.228, 0.238, 0.164],
                                index=['000006.SZ', '000012.SZ', '000021.SZ'],
                                columns=['weight'])
        calculated = get_universe(index_id, '2017-12-04', True)
        assert_frame_equal(calculated, expected)

    def test_convert_2_multi_index(self):
        df = pd.DataFrame(data=[[1, 2], [3, 4], [5, 6]],
                          index=['a', 'b', 'c'],
                          columns=['x', 'y'])
        calculated = wind_query_helper.convert_2_multi_index(df)
        expected = pd.DataFrame(data=[1, 2, 3, 4, 5, 6],
                                index=pd.MultiIndex.from_product([['a', 'b', 'c'], ['x', 'y']],
                                                                 names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

    def test_reformat_wind_data(self):
        sec_id = ['000001.SZ', '000002.SZ']
        raw_data = MockWindData(data=[[1, 2]],
                                codes=sec_id,
                                error_code=0,
                                fields=['factor'],
                                times=None)
        date = datetime(2017, 1, 1)
        date_str = '2017-01-01'
        calculated = wind_query_helper.reformat_wind_data(raw_data, date,
                                                          output_data_format=OutputFormat.MULTI_INDEX_DF,
                                                          multi_factors=False)
        expected = pd.DataFrame(data=[1, 2],
                                index=pd.MultiIndex.from_product([[date_str], sec_id], names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

        calculated = wind_query_helper.reformat_wind_data(raw_data, date,
                                                          output_data_format=OutputFormat.PIVOT_TABLE_DF,
                                                          multi_factors=False)
        expected = pd.DataFrame(data=[[1, 2]], index=[date_str], columns=sec_id)
        assert_frame_equal(calculated, expected)

        # raw_data = MockWindData(data=[['000001.SZ', '000002.SZ'], [1, 2], [3, 4], [5, 6], [7, 8]],
        #                         codes=['MultiCodes'],
        #                         error_code=0,
        #                         fields=['code', 'open', 'high', 'low', 'close'],
        #                         times=[datetime(2017, 1, 1),
        #                                datetime(2017, 1, 1)])
        # calculated = wind_query_helper.reformat_wind_data(raw_data, date, multi_factors=True)
        # expected = pd.DataFrame(data=[['000001.SZ', 1, 3, 5, 7], ['000002.SZ', 2, 4, 6, 8]],
        #                         index=pd.MultiIndex.from_product([[datetime(2017, 1, 1)], ['MultiCodes'] * 2],
        #                                                          names=['date', 'secID']),
        #                         columns=['code', 'open', 'high', 'low', 'close'])
        # print calculated, expected
        # assert_frame_equal(calculated, expected)

    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    def test_retrieve_data(self, mock_query_data):
        # api = 'w.wsq'
        sec_id = ['000001.SZ', '000002.SZ']
        factor_name = 'LIVE'
        factor_loader = FactorLoader('', '', factor_name, sec_id=sec_id)
        main_params, extra_params = wind_query_helper.get_query_params(factor_name)

        mock_data = MockWindData(data=[[13.15, 30.6],
                                       [13.35, 30.96],
                                       [13.1, 30.38],
                                       [13.29, 30.45],
                                       [41907453.0, 9939520.0],
                                       [555288048.0, 305155242.0],
                                       [1.1099, 0.6455],
                                       [-0.0008, -0.0059]],
                                 codes=sec_id,
                                 error_code=0,
                                 fields=['LIVE'],
                                 # fields=['RT_OPEN,RT_HIGH,RT_LOW,RT_LAST,RT_VOL,RT_AMT,RT_VOL_RATIO,RT_PCT_CHG_5MIN'],
                                 times=None)
        mock_query_data.return_value = mock_data
        calculated = factor_loader._retrieve_data(main_params, extra_params, '')
        expected = pd.DataFrame(data=[[13.15, 13.35, 13.1, 13.29, 41907453.0, 555288048.0, 1.1099, -0.0008],
                                      [30.6, 30.96, 30.38, 30.45, 9939520.0, 305155242.0, 0.6455, -0.0059]],
                                index=[0, 1],
                                columns=['open', 'high', 'low', 'last', 'vol', 'amt', 'vol_ratio', 'pct_chg_5min'])
        assert_frame_equal(calculated, expected)

        # api = 'w.wsi'
        # start_date = '2017-01-03 09:30:00'
        # end_date = '2017-01-03 09:32:00'
        # sec_id = ['000001.SZ', '000002.SZ']
        # factor_name = 'OHLCV_MIN'
        # factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id)
        # main_params, extra_params = wind_query_helper.get_query_params(factor_name)
        # mock_data = MockWindData(data=[['2017-01-03 09:30:00', '2017-01-03 09:31:00',
        #                                 '2017-01-03 09:30:00', '2017-01-03 09:31:00'],
        #                                ['000001.SZ', '000001.SZ', '000002.SZ', '000002.SZ'],
        #                                [3, 3, 3, 3],
        #                                [4, 4, 4, 4],
        #                                [5, 5, 5, 5],
        #                                [6, 6, 6, 6],
        #                                [7, 7, 7, 7]],
        #                          codes=['MultiCodes'],
        #                          error_code=0,
        #                          fields=['time', 'windcode', 'open', 'high', 'low', 'close', 'volume'],
        #                          times=[datetime(2017, 1, 3, 9, 30, 0),
        #                                 datetime(2017, 1, 3, 9, 31, 0),
        #                                 datetime(2017, 1, 3, 9, 30, 0),
        #                                 datetime(2017, 1, 3, 9, 31, 0)])
        # mock_query_data.return_value = mock_data
        # calculated = factor_loader._retrieve_data(main_params, extra_params, '')
        # expected = pd.DataFrame(data=[['2017-01-03 09:30:00', '000001.SZ', 3, 4, 5, 6, 7],
        #                               ['2017-01-03 09:31:00', '000001.SZ', 3, 4, 5, 6, 7],
        #                               ['2017-01-03 09:30:00', '000002.SZ', 3, 4, 5, 6, 7],
        #                               ['2017-01-03 09:31:00', '000002.SZ', 3, 4, 5, 6, 7]],
        #                         index=pd.MultiIndex.from_arrays([[datetime(2017, 1, 3, 9, 30, 0),
        #                                                           datetime(2017, 1, 3, 9, 31, 0)]*2,
        #                                                          ['MultiCodes']*4],
        #                                                         names=['date', 'secID']),
        #                         columns=['time', 'windcode', 'open', 'high', 'low', 'close', 'volume'])
        # assert_frame_equal(calculated, expected)

        # api = 'w.wsd'
        start_date = '2017-01-03'
        end_date = '2017-01-05'
        sec_id = ['000001.SZ']
        factor_name = 'PB'
        factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id, is_index=False,
                                     freq=FreqType.EOD)
        main_params, extra_params = wind_query_helper.get_query_params(factor_name)
        mock_data = MockWindData(data=[1],
                                 codes=sec_id,
                                 error_code=0,
                                 fields=['PB'],
                                 times=None)
        mock_query_data.return_value = mock_data
        calculated = factor_loader._retrieve_data(main_params, extra_params, OutputFormat.MULTI_INDEX_DF)
        expected = pd.DataFrame(data=[1, 1, 1],
                                index=pd.MultiIndex.from_arrays([['2017-01-03', '2017-01-04', '2017-01-05'],
                                                                 ['000001.SZ'] * 3],
                                                                names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

        calculated = factor_loader._retrieve_data(main_params, extra_params, OutputFormat.PIVOT_TABLE_DF)
        expected = pd.DataFrame(data=[1, 1, 1],
                                index=['2017-01-03', '2017-01-04', '2017-01-05'],
                                columns=sec_id)
        assert_frame_equal(calculated, expected)

        # api = 'w.wss'
        start_date = '2017-01-03'
        end_date = '2017-01-05'
        sec_id = ['000001.SZ', '000002.SZ']
        factor_name = 'RETURN'
        factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id, is_index=False,
                                     freq=FreqType.EOD, tenor='3M', output_data_format=OutputFormat.MULTI_INDEX_DF)
        main_params, extra_params = wind_query_helper.get_query_params(factor_name)
        extra_params[Header.TENOR.value] = factor_loader._get_enum_value(factor_loader.tenor) \
            if factor_loader.tenor is not None else None
        extra_params[Header.FREQ.value] = factor_loader._get_enum_value(factor_loader.freq)
        mock_data = MockWindData(data=[[1, 2]],
                                 codes=sec_id,
                                 error_code=0,
                                 fields=['RETURN'],
                                 times=None)
        mock_query_data.return_value = mock_data

        calculated = factor_loader._retrieve_data(main_params, extra_params, OutputFormat.MULTI_INDEX_DF)
        expected = pd.DataFrame(data=[1, 2, 1, 2, 1, 2],
                                index=pd.MultiIndex.from_product([['2017-01-03', '2017-01-04', '2017-01-05'], sec_id],
                                                                 names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

        calculated = factor_loader._retrieve_data(main_params, extra_params, OutputFormat.PIVOT_TABLE_DF)
        expected = pd.DataFrame(data=[[1, 2], [1, 2], [1, 2]],
                                index=['2017-01-03', '2017-01-04', '2017-01-05'],
                                columns=sec_id)
        assert_frame_equal(calculated, expected)

    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    @patch('WindAdapter.data_provider.WindDataProvider.get_universe')
    def test_load_industry_weight(self, mock_get_universe, mock_query_data):
        start_date = '2017-01-01'
        end_date = '2017-02-28'
        sec_id = '000905.SH'
        factor_name = 'INDUSTRY_WEIGHT_C1'
        mock_get_universe.return_value = pd.DataFrame(data=[0.1, 0.7],
                                                      index=['000001.SZ', '000002.SZ'],
                                                      columns=['weight'])
        mock_data = MockWindData(data=[['801780.SI', '801180.SI']],
                                 codes=['000001.SZ', '000002.SZ'],
                                 error_code=0,
                                 fields=['INDEXCODE_SW'],
                                 times=None)
        mock_query_data.return_value = mock_data

        factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id,
                                     freq=FreqType.EOM, output_data_format=OutputFormat.MULTI_INDEX_DF)
        calculated = factor_loader._load_industry_weight()
        expected = pd.DataFrame(data=[0.7, 0.1, 0.7, 0.1],
                                index=pd.MultiIndex.from_product([['2017-01-26', '2017-02-28'],
                                                                  ['801180.SI', '801780.SI']],
                                                                 names=['date', 'secID']),
                                columns=['factor'])
        assert_frame_equal(calculated, expected)

        factor_loader = FactorLoader(start_date, end_date, factor_name, sec_id=sec_id,
                                     freq=FreqType.EOM, output_data_format=OutputFormat.PIVOT_TABLE_DF)
        calculated = factor_loader._load_industry_weight()
        expected = pd.DataFrame(data=[['2017-01-26', 0.7, 0.1], ['2017-02-28', 0.7, 0.1]],
                                columns=['class_id', '801180.SI', '801780.SI']).set_index('class_id')
        # expected = pd.DataFrame(data=[[0.7, 0.1], [0.7, 0.1]],
        #                         index=['2017-01-26', '2017-02-28'],
        #                         columns=['801180.SI', '801780.SI'])
        assert_frame_equal(calculated, expected)

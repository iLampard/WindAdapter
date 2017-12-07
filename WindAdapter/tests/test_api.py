# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import pandas as pd

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from pandas.util.testing import assert_frame_equal
from WindAdapter.api import (factor_load,
                             get_universe)
from WindAdapter.helper import WindQueryHelper
from WindAdapter.enums import OutputFormat

wind_query_helper = WindQueryHelper()


class MockWindData(object):
    def __init__(self, data, codes, error_code, fields, times):
        self.Data = data
        self.Codes = codes
        self.ErrorCode = error_code
        self.Fields = fields
        self.Times = times


class TestApi(unittest.TestCase):
    @patch('WindAdapter.data_provider.WindDataProvider.biz_days_list')
    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    def test_factor_load_case1(self, mock_query_data, mock_days_list):
        """
        测试没有tenor的情况
        """
        start_date = '2016-01-01'
        end_date = '2016-02-01'
        factor_name = 'PB'
        sec_id = ['000001.SZ', '000002.SZ', '000003.SZ']

        mock_data = MockWindData(data=[[1, 3, 5]],
                                 codes=sec_id,
                                 error_code=0,
                                 fields=['PB'],
                                 times=[datetime(2016, 1, 1),
                                        datetime(2016, 2, 29)])
        mock_query_data.return_value = mock_data
        mock_days_list.return_value = [datetime(2016, 1, 29), datetime(2016, 2, 29)]

        calculated = factor_load(start_date=start_date,
                                 end_date=end_date,
                                 factor_name=factor_name,
                                 sec_id=sec_id,
                                 output_data_format=OutputFormat.MULTI_INDEX_DF,
                                 is_index=False)

        expected = pd.DataFrame(data=[1, 3, 5, 1, 3, 5],
                                index=pd.MultiIndex.from_product([['2016-01-29', '2016-02-29'],
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
                                index=['2016-01-29', '2016-02-29'])
        assert_frame_equal(calculated, expected)

    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    @patch('WindAdapter.data_provider.WindDataProvider.biz_days_list')
    @patch('WindAdapter.data_provider.WindDataProvider.forward_date')
    def test_factor_load_case2(self, mock_adv_date, mock_days_list, mock_query_data):
        """
        测试有tenor的情况
        """
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

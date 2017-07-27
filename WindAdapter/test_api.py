# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import pandas as pd
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from pandas.util.testing import assert_frame_equal
import os
import sys
thisFilePath = os.path.abspath(__file__)
sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-3]))
from WindAdapter.api import factor_load


class MockWindData(object):
    def __init__(self, data, codes, error_code, fields, times):
        self.Data = data
        self.Codes = codes
        self.ErrorCode = error_code
        self.Fields = fields
        self.Times = times


class TestApi(unittest.TestCase):
    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    def testFactorLoad_case1(self, mock_query_data):
        from WindAdapter.enums import OutputFormat
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
                                 output_data_format=OutputFormat.PITVOT_TABLE_DF,
                                 is_index=False)
        expected = pd.DataFrame(data=[[1, 3, 5], [1, 3, 5]],
                                columns=['000001.SZ', '000002.SZ', '000003.SZ'],
                                index=['2016-01-29', '2016-02-01'])
        assert_frame_equal(calculated, expected)

    @patch('WindAdapter.data_provider.WindDataProvider.query_data')
    @patch('WindAdapter.data_provider.WindDataProvider.biz_days_list')
    @patch('WindAdapter.data_provider.WindDataProvider.forward_date')
    def testFactorLoad_case2(self, mock_adv_date, mock_days_list, mock_query_data):
        from WindAdapter.enums import OutputFormat
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
                                 output_data_format=OutputFormat.PITVOT_TABLE_DF,
                                 is_index=False)
        expected = pd.DataFrame(data=[[1, 2, 3, 4], [1, 2, 3, 4]],
                                index=['2016-01-01', '2016-02-01'],
                                columns=['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ'])
        assert_frame_equal(calculated, expected)

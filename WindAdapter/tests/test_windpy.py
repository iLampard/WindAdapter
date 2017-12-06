# -*- coding: utf-8 -*-

import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from WindAdapter.data_provider import WindDataProvider
from WindAdapter.helper import WindQueryHelper

wind_query_helper = WindQueryHelper()


class MockWindData(object):
    def __init__(self, data, codes, error_code, fields, times):
        self.Data = data
        self.Codes = codes
        self.ErrorCode = error_code
        self.Fields = fields
        self.Times = times


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

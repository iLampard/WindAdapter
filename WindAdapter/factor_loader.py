# -*- coding: utf-8 -*-

import re

import pandas as pd
from argcheck import expect_types

from WindAdapter.data_provider import WindDataProvider
from WindAdapter.enums import FreqType
from WindAdapter.enums import Header
from WindAdapter.enums import OutputFormat
from WindAdapter.helper import WindQueryHelper
from WindAdapter.utils import date_convert_2_str
from WindAdapter.utils import py_assert

WIND_QUERY_HELPER = WindQueryHelper()
WIND_DATA_PROVIDER = WindDataProvider()


class FactorLoader:
    def __init__(self, start_date, end_date, factor_name, **kwargs):
        self.start_date = start_date
        self.end_date = end_date
        self.factor_name = factor_name
        self.sec_id = kwargs.get('sec_id', 'fulla')
        self.freq = kwargs.get('freq', FreqType.EOM)
        self.tenor = kwargs.get('tenor', None)
        self.output_data_format = kwargs.get('output_data_format', OutputFormat.MULTI_INDEX_DF)
        self.is_index = kwargs.get('is_index', True)
        self.date_format = kwargs.get('date_format', '%Y-%m-%d')
        self.block_size = kwargs.get('block_size', 400)

    @staticmethod
    def _check_industry_params(factor_name):
        if factor_name[:-1] == 'INDUSTRY_WEIGHT_C' or factor_name[:-1] == 'sw_c' or factor_name[:-1] == 'sw_name_c':
            return ';industryType=' + str(filter(str.isdigit, str(factor_name)))
        else:
            return ''

    def _merge_query_params(self, params, date=None):
        ret = ''
        for key, value in params.iteritems():
            if not pd.isnull(value):
                if key == Header.TENOR:
                    py_assert(date is not None, ValueError, 'date must given if tenor is not None')
                    # unit = ''.join(re.findall('[0-9]+', params[Header.TENOR]))
                    # freq = FreqType(params[Header.TENOR][len(unit):])
                    ret += 'startDate=' + WIND_DATA_PROVIDER.forward_date(date, value,
                                                                          self.date_format) + ';endDate=' + date + ';'
                elif key == Header.FREQ and value[:3] == 'min':
                    ret += ('BarSize=' + value[3:] + ';')
                else:
                    ret += (key + '=' + str(value) + ';')
        ret = ret[:-1] + FactorLoader._check_industry_params(params.name)
        return ret

    @staticmethod
    @expect_types(enum_var=(FreqType, str))
    def _get_enum_value(enum_var):
        if isinstance(enum_var, FreqType):
            return enum_var.value
        elif isinstance(enum_var, str):
            return enum_var

    def _get_sec_id(self, date):
        if isinstance(self.sec_id, str):
            sec_id = WIND_DATA_PROVIDER.get_universe(self.sec_id, date=date) \
                if self.is_index else self.sec_id
        elif isinstance(self.sec_id, list):
            sec_id = self.sec_id
        else:
            raise TypeError('FactorLoader._get_sec_id: sec_id must be either list of string')

        return sec_id

    def _retrieve_data(self, main_params, extra_params, output_data_format):
        output_data = pd.DataFrame()
        api = main_params[Header.API]

        if api == 'w.wsq':
            loop_times = int(len(self.sec_id) / self.block_size) + 1
            for j in range(loop_times):
                code_set = self.sec_id[j * self.block_size: (j + 1) * self.block_size]
                raw_data = WIND_DATA_PROVIDER.query_data(api=api,
                                                         sec_id=code_set,
                                                         indicator=main_params[Header.INDICATOR])
                output_data = pd.concat([output_data, pd.DataFrame(raw_data.Data).T], axis=0)
            output_data.columns = ['open', 'high', 'low', 'last', 'vol', 'amt', 'vol_ratio', 'pct_chg_5min']
        elif api == 'w.wsi':
            merged_extra_params = self._merge_query_params(extra_params, date=self.end_date)
            raw_data = WIND_DATA_PROVIDER.query_data(api=api,
                                                     sec_id=self.sec_id,
                                                     indicator=main_params[Header.INDICATOR],
                                                     extra_params=merged_extra_params,
                                                     start_date=self.start_date,
                                                     end_date=self.end_date)
            multi_factors = True if extra_params[Header.MULTIFACTORS] == 'Y' else False
            output_data = WIND_QUERY_HELPER.reformat_wind_data(raw_data=raw_data, date=self.end_date,
                                                               multi_factors=multi_factors)
        else:
            dates = WIND_DATA_PROVIDER.biz_days_list(start_date=self.start_date,
                                                     end_date=self.end_date,
                                                     freq=self.freq)
            for fetch_date in dates:
                if not pd.isnull(extra_params[Header.REPORTADJ]):
                    date = WIND_QUERY_HELPER.latest_report_date(fetch_date)
                else:
                    date = fetch_date
                date = date_convert_2_str(date)

                sec_id = WIND_DATA_PROVIDER.get_universe(self.sec_id, date=date) \
                    if self.is_index else self.sec_id
                if api == 'w.wsd':
                    merged_extra_params = self._merge_query_params(extra_params, date=date)
                    raw_data = WIND_DATA_PROVIDER.query_data(api=api,
                                                             sec_id=sec_id,
                                                             indicator=main_params[Header.INDICATOR],
                                                             extra_params=merged_extra_params,
                                                             start_date=date,
                                                             end_date=date)
                elif api == 'w.wss':
                    py_assert(not pd.isnull(extra_params[Header.TENOR]), ValueError,
                              'tenor must be given for query factor {0}'.format(self.factor_name))
                    merged_extra_params = self._merge_query_params(extra_params, date=date)
                    raw_data = WIND_DATA_PROVIDER.query_data(api=api,
                                                             sec_id=sec_id,
                                                             indicator=main_params[Header.INDICATOR],
                                                             extra_params=merged_extra_params)
                else:
                    raise ValueError('FactorLoader._retrieve_data: unacceptable value of parameter api')

                multi_factors = True if extra_params[Header.MULTIFACTORS] == 'Y' else False
                tmp = WIND_QUERY_HELPER.reformat_wind_data(raw_data=raw_data,
                                                           date=fetch_date,
                                                           output_data_format=output_data_format,
                                                           multi_factors=multi_factors)
                output_data = pd.concat([output_data, tmp], axis=0)

        return output_data

    def _load_single_factor(self):
        main_params, extra_params = WIND_QUERY_HELPER.get_query_params(self.factor_name)
        extra_params[Header.TENOR.value] = self._get_enum_value(self.tenor) if self.tenor is not None else None
        extra_params[Header.FREQ.value] = self._get_enum_value(self.freq)
        ret = self._retrieve_data(main_params=main_params,
                                  extra_params=extra_params,
                                  output_data_format=self.output_data_format)
        return ret

    def load_data(self):
        if self.factor_name[:-3] == 'INDUSTRY_WEIGHT':
            ret = self._load_industry_weight()
        else:
            ret = self._load_single_factor()
        return ret

    def _load_industry_weight(self):
        ret = pd.DataFrame()
        dates = WIND_DATA_PROVIDER.biz_days_list(start_date=self.start_date,
                                                 end_date=self.end_date,
                                                 freq=self.freq)
        extra_params = self._check_industry_params(self.factor_name)
        for date in dates:
            date = date_convert_2_str(date)
            index_info = WIND_DATA_PROVIDER.get_universe(self.sec_id, date=date, output_weight=True)
            class_info = WIND_DATA_PROVIDER.query_data(api='w.wsd',
                                                       sec_id=index_info[1],
                                                       indicator='indexcode_sw',
                                                       extra_params=extra_params,
                                                       start_date=date,
                                                       end_date=date)
            industry_weight = pd.DataFrame(data={'sec_id': index_info[1],
                                                 'class_id': class_info.Data[0],
                                                 'sec_weight': index_info[3]},
                                           index=index_info[0])

            tmp = industry_weight.groupby('class_id').sum().T
            tmp.index = [date]
            tmp = WIND_QUERY_HELPER.convert_2_multi_index(tmp) \
                if self.output_data_format == OutputFormat.MULTI_INDEX_DF else tmp
            ret = ret.append(tmp)
        return ret



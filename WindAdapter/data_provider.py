# -*- coding: utf-8 -*-

import pandas as pd
from PyFin.DateUtilities import (Calendar,
                                 Date,
                                 Period)

try:
    from WindPy import w
except ImportError:
    pass


class WindRunner:
    def __init__(self):
        try:
            w.start()
        except NameError:
            pass

    def __del__(self):
        try:
            w.stop()
        except AttributeError:
            pass
        except NameError:
            pass


class WindDataProvider:
    WIND_RUNNER = WindRunner()

    def __init__(self):
        pass

    @staticmethod
    def force_throw_err(raw_data, func_name):
        if raw_data.ErrorCode != 0:
            raise ValueError('{0}: {1}'.format(raw_data.Data[0], func_name))
        elif len(raw_data.Data) == 0:
            raise ValueError('{0}: empty data returned'.format(func_name))

    @staticmethod
    def get_universe(index_id, date=None, output_weight=False):
        index_id = index_id.lower()
        try:
            if index_id == 'fulla':
                code = 'a001010100000000'
                params = 'sectorid=' + code + ';field=wind_code' if date is None \
                    else 'date=' + str(date) + ';sectorid=' + code
                raw_data = w.wset('sectorconstituent', params)
            else:
                short_params = 'windcode=' + index_id
                params = short_params if date is None else short_params + ';date=' + str(date)
                raw_data = w.wset('IndexConstituent', params)
            WindDataProvider.force_throw_err(raw_data, 'WindDataProvider.get_universe')
            if output_weight:
                return pd.DataFrame(data=raw_data.Data[3], index=raw_data.Data[1], columns=['weight'])
            else:
                return raw_data.Data[1]
        except NameError:
            pass

    @staticmethod
    def forward_date(date, tenor, date_format='%Y-%m-%d'):
        try:
            # use pyfin instead to get more accurate and flexible date math
            start_date = Date.strptime(date, date_format)
            sseCal = Calendar('China.SSE')
            ret = sseCal.advanceDate(start_date, Period('-' + tenor), endOfMonth=True)
            # 此处返回的是上一期期末日期，再向后调整一天，以避免区间日期重叠
            ret = sseCal.advanceDate(ret, Period('1b'))
            return str(ret)
        except NameError:
            pass

    @staticmethod
    def biz_days_list(start_date, end_date, freq):
        try:
            dates = w.tdays(start_date, end_date, 'period=' + freq)
            WindDataProvider.force_throw_err(dates, 'WindDataProvider.biz_days_list')
            return dates.Data[0]
        except NameError:
            pass

    @staticmethod
    def query_data(api, sec_id, indicator, extra_params=None, start_date=None, end_date=None):
        if api == 'w.wsd':
            ret = eval(api)(sec_id, indicator, start_date, end_date, extra_params)
        elif api == 'w.wss':
            ret = eval(api)(sec_id, indicator, extra_params)
        elif api == 'w.wsi':
            ret = eval(api)(sec_id, indicator, start_date, end_date, extra_params)
        elif api == 'w.wsq':
            ret = eval(api)(sec_id, indicator)
        else:
            raise ValueError('WindDataProvider.query_data: unknown type of api')

        WindDataProvider.force_throw_err(ret, 'WindDataProvider.query_data')
        return ret

# -*- coding: utf-8 -*-

try:
    from WindPy import w
except ImportError:
    raise ValueError('Failed to import WindPy')
import pandas as pd


class WindRunner:
    def __init__(self):
        w.start()

    def __del__(self):
        try:
            w.stop()
        except AttributeError:
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
    def get_universe(index_id, date, output_weight=False):
        index_id = index_id.lower()
        if index_id == 'fulla':
            code = 'a001010100000000'
            params = 'sectorid=' + code + ';field=wind_code' if date is None \
                         else 'date=' + str(date) + ';sectorid=' + code, ';field=wind_code'
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

    @staticmethod
    def advance_date(date, unit, freq):
        ret = w.tdaysoffset(int(unit) * -1, date, 'period=' + freq)
        WindDataProvider.force_throw_err(ret, 'WindDataProvider.advance_date')
        return ret.Data[0][0]

    @staticmethod
    def biz_days_list(start_date, end_date, freq):
        dates = w.tdays(start_date, end_date, 'period=' + freq)
        WindDataProvider.force_throw_err(dates, 'WindDataProvider.biz_days_list')
        return dates.Data[0]

    @staticmethod
    def query_data(api, sec_id, indicator, extra_params, start_date=None, end_date=None):
        if api == 'w.wsd':
            ret = eval(api)(sec_id, indicator, start_date, end_date, extra_params)
        elif api == 'w.wss':
            ret = eval(api)(sec_id, indicator, extra_params)
        else:
            raise ValueError('WindDataProvider.query_data: unknown type of api')

        WindDataProvider.force_throw_err(ret, 'WindDataProvider.query_data')
        return ret



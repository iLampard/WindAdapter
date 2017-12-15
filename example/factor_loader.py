# -*- coding: utf-8 -*-

from WindAdapter import factor_load

ret = factor_load('2014-01-01', '2014-01-15', 'FULL_OHLC_DAY', sec_id='ashare', is_index=True, freq='D', save_file='ashare.csv')


print factor_load('2014-01-01', '2014-01-10', 'close', sec_id='ashare', is_index=True, freq='D', save_file='close.pkl')

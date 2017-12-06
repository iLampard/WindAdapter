# -*- coding: utf-8 -*-

from WindAdapter import factor_load

ret = factor_load('2014-01-01', '2014-07-10', 'PB', sec_id=['000001.SZ', '000002.SZ'], is_index=False, save_file='PB.csv')

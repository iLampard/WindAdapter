from WindAdapter.api import get_universe, factor_help, factor_details_help, reset_data_dict_path, reset_log_level, \
    factor_load
from WindAdapter.enums import OutputFormat

if __name__ == "__main__":
    reset_data_dict_path(path='C:\\data_dict_perso.csv', path_type_abs=True)
    # query.wind_load_factor('2014-01-01', '2016-01-01', 'PB', save_file=True)
    # WindAdapter.api.factor_help()
    # WindAdapter.api.factor_details_help()
    # factor_load('2014-01-01', '2014-05-10', 'PB', sec_id=['000001.SZ', '000002.SZ'], is_index=False, save_file='PB.csv')
    # factor_load('2014-01-01', '2014-01-10', 'close', sec_id='fullA', is_index=True, freq='D', save_file='close.pkl')
    factor_load('2016-01-01', '2016-03-31', 'return', sec_id='000300.SH', is_index=True, freq='M', tenor='1Q',
                output_data_format=OutputFormat.PITVOT_TABLE_DF, save_file='HS300_return_1Q.csv')
    # WindAdapter.api.factor_load('2014-01-01', '2016-01-01', 'STDQ', save_file='STDQ.csv')

    # print get_universe('000301.SH')

    # reset_log_level('critical')
    # factor_details_help()


    # reset_data_dict_path('D:\Workarea\Qinhuangdao\CodeLib\Python\WindAdapter\WindAdapter\data_dict.csv', True)
    # factor_details_help(log_level='notset')

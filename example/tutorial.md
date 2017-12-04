


## 使用

##### factor_load 
``` python
from WindAdapter import factor_load

# def factor_load(start_date, end_date, factor_name, save_file=None, **kwargs):
"""
:param start_date: str, 读取因子数据的开始日期
:param end_date: str, 读取因子数据的结束日期
:param factor_name: str, 因子名称，不区分大小写
:param save_file: str, optional, 保存数据的文件名，可写成 '*.csv' 或者 '*.pkl'
:param kwargs: dict, optional

        freq: str, optional, 因子数据的频率， 可选'M', 'W', 'Q', 'S', 'Y'， 参见enums.py - FreqType
        tenor: str, optional, 因子数据的周期， 对于截面数据（如换手率，收益率），需要给定数据区间(向前)， 可选数字+FreqType， 如'1Q'
        sec_id, str/list, optional, 股票代码或者是指数代码
        output_data_format: enum, optional, 参见enums.py - FreqType
                            MULTI_INDEX_DF: multi-index DataFrame, index=[date, secID], value = factor
                            PIVOT_TABLE_DF: DataFrame, index=date, columns = secID
        is_index: bool, optional, True: 输入的sec_id是指数，实际需要读取的是该指数成分股的因子数据，
                                  False: 直接读取sec_id的因子数据
:return: pd.DataFrame 整理好的因子数据
"""

# 读取 2014年上半年 000001.SZ和000002.SZ的PB数据， 并保存成csv格式（默认数据频率为月频，数据格式为multi-index DataFrame）
factor_load('2014-01-01', '2014-07-10', 'PB', sec_id=['000001.SZ', '000002.SZ'], is_index=False, save_file='PB.csv')

# 读取全市场 2016年1月的每日收盘价，并保存成pickle格式
factor_load('2014-01-01', '2014-07-10', 'close', sec_id='fullA', is_index=True, freq='D', save_file='close.pkl')

# 读取沪深300成分股从2014年1月至3月，频率为每月(freq=M)的季度(tenor='1Q')收益， 并保存成csv格式
factor_load('2014-01-01', '2014-03-31', 'return', sec_id='000300.SH', is_index=True, freq='M', tenor='1Q', save_file='HS300_return_1Q.csv')


```
*Note*: 返回的数据最近的日期等于入参中的end_date，前推的日期为根据频率(freq)和end_date往前推算的交易日

<br />

##### get_universe

``` python
from WindAdapter import get_universe

# def get_universe(index_id, date=None)
"""
:param index_id: str, 可以为指数代码或者'fullA'（指全市场股票），不区分大小写
:param date: str, optional, YYYYMMDD/YYYY-MM-DD，默认为None，即返回最近交易日的成分股列表 
:return: list, 成分股列表
"""

# 读取指数成分股
hs300_comp = get_universe(index_id='000300.SH', date='20170103')

# 读取全市场股票
full_mkt = get_universe(index_id='fullA')
```
<br />

##### reset_data_dict_path

``` python
from WindAdapter import reset_data_dict_path

# def reset_data_dict_path(path, path_type_abs)
"""
:param index_id: str, 可以为指数代码或者'fullA'（指全市场股票），不区分大小写
:param date: str, optional, YYYYMMDD/YYYY-MM-DD，默认为None，即返回最近交易日的成分股列表 
:return: list, 成分股列表
"""
reset_data_dict_path(path='C:\\data_dict_perso.csv', path_type_abs=True)
```
<br />

##### factor_help / factor_details_help

``` python
from WindAdapter import factor_help, factor_details_help

"""
:return: 返回定义的数据字典（简易版和详细版） 
"""
factor_help()

factor_details_help()

```

<br />



##### reset_log_level
``` python
from WindAdapter import reset_log_level

"""
:return: 设置WindAdapter函数输出信息的等级， 项目默认为'info'等级
"""
reset_log_level('critical')

```

<br />

##### version

``` python
from WindAdapter import version

"""
:return: 当前WindAdapter的版本号 
"""
version()

```




## 依赖
``` python
numpy
pandas
python-decouple
WindPy
```

## 安装

``` python
pip install WindAdapter
```

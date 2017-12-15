<table>
<tr>
  <td>Latest Release</td>
  <td><img src="https://img.shields.io/pypi/v/WindAdapter.svg" alt="latest release" /></td>
</tr>


<tr>
  <td>Python version</td>
  <td><img src="https://img.shields.io/badge/python-2.7-blue.svg"/>   <img src="https://img.shields.io/badge/python-3.5-blue.svg"/> <img src="https://img.shields.io/badge/python-3.6-blue.svg"/></td>
  </tr>

<tr>
  <td>Build Status</td>
  <td><img src="https://travis-ci.org/iLampard/WindAdapter.svg?branch=master" alt="build status" /></td>
</tr>
</table>


# WindAdapter

*WindAdapter*是一个从wind网络终端读取和整理因子数据的简单工具: 相比于直接使用wsd/wss等wind函数, *WindAdapter*根据预先定义好的参数字典(用户也可以自行扩展更新), 可以让用户更便捷的读取和整理数据

具体而言, *WindAdapter*的功能有

-  根据用户输入因子名称和读取区间, 以及预定义的数据字典(如本项目默认的‘data_dict.csv’), *自动*拼接参数语句与接口函数, 从wind网络终端读取数据
-  返回因子数据的格式为pandas.DataFrame
可选择MultiIndex(index为date和secID, value=因子值) 或者 PivotTable格式（index=date, col=secID，value=因子值）
-  返回因子数据可在读取完毕后选择保存为csv或者pickle格式
-  还可返回指数成分股列表: 可选择全市场或者某个指数
-  读取市场的实时数据

*Note*

-  只有在数据字典中预定义好的因子才能利用*WindAdpater*读取，目前已整理好约20个因子的参数以及接口列表, 可使用*factor_help*首先进行查询 
-  用户可以在本地自行更新数据字典作为*WindAdpater*引用（方法见下文*reset_data_dict_path*）或者等待本项目后续更新


## Quick Start

##### get_universe

``` python
# 读取2017年1月3日沪深300指数成分股(同时返回对应的权重如果output_weight=True)
hs300_comp = get_universe('000300.SH', date='20170103', output_weight=True)
```

##### factor_help

``` python
from WindAdapter import factor_help

factor_help()

# 将会输出目前可以查询的因子名称列表

```




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

        freq: str, optional, 因子数据的频率， 可选'M', 'W', 'S', 'Y'， 参见enums.py - FreqType
        tenor: str, optional, 因子数据的周期， 对于截面数据（如换手率，收益率），需要给定数据区间(向前)， 可选数字+FreqType， 如'3M'
        sec_id, str/list, optional, 股票代码或者是指数代码
        output_data_format: enum, optional, 参见enums.py - FreqType
                            MULTI_INDEX_DF: multi-index DataFrame, index=[date, secID], value = factor
                            PIVOT_TABLE_DF: DataFrame, index=date, columns = secID
        is_index: bool, optional, True: 输入的sec_id是指数，实际需要读取的是该指数成分股的因子数据，
                                  False: 直接读取sec_id的因子数据
        date_format: str, optional, 日期的格式， 默认'%Y-%m-%d'
:return: pd.DataFrame 整理好的因子数据
"""


# 读取 2014年1月1日 至 1月15日 全部A股个股的日频行情数据，包括开高低收、复权因子、交易状态等，并保存成csv格式
factor_load('2014-01-01', '2014-01-15', 'FULL_OHLC_DAY', sec_id='ashare', is_index=True, freq='D', save_file='ashare.csv')

# 读取 2014年上半年 000001.SZ和000002.SZ的PB数据， 并保存成csv格式（默认数据频率为月频，数据格式为multi-index DataFrame）
factor_load('2014-01-01', '2014-07-10', 'PB', sec_id=['000001.SZ', '000002.SZ'], is_index=False, save_file='PB.csv')

# 读取2016年1月 全部A顾个股的每日收盘价，并保存成pickle格式
factor_load('2014-01-01', '2014-07-10', 'close', sec_id='ashare', is_index=True, freq='D', save_file='close.pkl')

# 读取沪深300成分股从2014年1月至3月，频率为每月(freq=M)的季度(tenor='3M')收益， 并保存成csv格式
factor_load('2014-01-01', '2014-03-31', 'return', sec_id='000300.SH', is_index=True, freq='M', tenor='3M', save_file='HS300_return_1Q.csv')```
```

*Note 1*: 返回的数据最近的日期等于入参中的end_date，前推的日期为根据频率(freq)和end_date往前推算的交易日

*Note 2*: tenor取值需要符合x-utils包的要求，具体请参照其[帮助](https://github.com/iLampard/x-utils)中所举的例子

另外，指数成分股权重也是作为因子，从*factor_loader*读取

``` python
# 读取指数成分股行业权重: 沪深300的申万一级行业权重分布
# 由于申万一级行业于2014年2月进行了调整，而wind的行业代码不可回溯，故2014年2月前的指数成分股权重之和不等于1
factor_load('2014-01-01', '2014-03-31', 'INDUSTRY_WEIGHT_C1', sec_id='000300.SH')


2014-12-31	801010.SI	0.52
            801020.SI	2.79
            801030.SI	2.37
            801040.SI	1.42
            801050.SI	3.28
            801080.SI	1.56
            801110.SI	2.80
            801120.SI	4.23
            801130.SI	0.32
            801150.SI	4.71
            801160.SI	4.06
            801170.SI	2.89
            801180.SI	5.08
            801200.SI	1.98
            801210.SI	0.21
            801230.SI	0.45
            801710.SI	0.73
            801720.SI	4.66
            801730.SI	1.74
            801740.SI	2.19
            801750.SI	2.09
            ...
```

factor_load还可以接受list of factor names 进行数据读取

``` python
factor_load('2014-01-01', '2014-07-10', ['PB', 'MV'], sec_id=['000001.SZ', '000002.SZ'], is_index=False,reset_col_names=True)

```
<br />

##### get_live

读取实时数据(通过wsq接口)


``` python
# def get_live(sec_id, block_size=400):
"""
:param sec_id: list, wind股票代码，如果是全市场，可输入'fulla'或者'ashare' 
:param block_size: 内部调用wsq接口一次提取的数量，默认400支
:return: pd.DataFrame, index=sec id, header = [rt_open,rt_high,rt_low,rt_last,rt_vol,rt_amt,rt_vol_ratio,rt_pct_chg_5min]
"""

```

如果和[Schedule](https://github.com/dbader/schedule)包结合，那么能方便连续读取wind的实时数据进行后续处理
``` python

from WindAdapter import (get_universe,
                         get_live)
import schedule                         
import time

def live_contrib(universe):
    ret = get_live(universe)
    # blabblabal
    return

universe = get_universe('ashare')
schedule.every(1).minutes.do(live_contrib, universe)
    
while True:
    schedule.run_pending()
    time.sleep(1)
  

```





其他细节参见[WindAdapter tutorial](/example/tutorial.ipymd) 


## 依赖
``` python
numpy
pandas
python-decouple
WindPy
x-utils
```

## 安装

``` python
pip install WindAdapter
```

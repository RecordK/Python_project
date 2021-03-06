# -*- coding: utf-8 -*-
"""4. 업종별 주가 분석 + 코스피.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FLjidF30mcLr5--XJbTiMoJSru9YMrzq

### 라이브러리
"""

#!pip install pandas
#!pip install pandas_datareader
#!pip install finance-datareader

"""### import"""

import pandas_datareader as pdr
import seaborn as sns
import pandas_datareader.data as web
from pandas_datareader import wb
import requests
import pandas as pd
import datetime
import FinanceDataReader as fdr

"""## Kospi 지수"""

Kospi= web.DataReader('^KOSPI','stooq')
sns.lineplot(x=Kospi.index, y="Close",data=Kospi)

"""### ex"""

kospi_cd=fdr.StockListing('KRX')
kospi_cd.tail()

kospi_cd.loc[kospi_cd["Industry"].str.find("드라마")>-1]

df= fdr.DataReader("005930",'2021')
sns.lineplot(x=df.index,y=df["Close"])


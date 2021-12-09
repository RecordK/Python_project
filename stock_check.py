# -*- coding: utf-8 -*-
"""stock_check.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sgDjbh0vBO_SMHpeE6dUP_juAvtQCcc7

## 라이브러리
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

"""# 주가데이터"""

TINGO_API_KEY="4a3d440f11fe1e3de3fdef124a769c845bce6e9d"
df=pdr.get_data_tiingo('GOOG',api_key=TINGO_API_KEY)
df.head()

sns.lineplot(x=df.index.levels[1], y="adjClose",data=df)

"""# 주가 지수 데이터"""

Kospi= web.DataReader('^KOSPI','stooq')
sns.lineplot(x=Kospi.index, y="Close",data=Kospi)

"""# 환율 데이터"""

ALPHAVANTAGE_API_KEY="G4F53WGNXCNW21AF"
ex_rate = web.DataReader("USD/KRW", "av-forex", api_key=ALPHAVANTAGE_API_KEY)
ex_rate.head()

"""## 월별 환율데이터"""

url = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=USD&to_symbol=KRW&apikey='+ALPHAVANTAGE_API_KEY
r = requests.get(url)
data = r.json()
df=pd.DataFrame(data['Time Series FX (Monthly)']).T
df.head()

"""### 참고용
 - response = requests.get(url, params=params)
 -  status_code =   response.status_code
 -  print(status_code)
 -  text = response.text
 -  driver=webdriver.Safari()
 -  driver.implicitly_wait(3)
 -  driver.get(url)
 - https://financedata.github.io/posts/finance-data-reader-users-guide.html

## 원자재 가격 데이터
"""

start=datetime.datetime(2020,1,1)
end=datetime.datetime(2021,7,15)

gold=web.DataReader('GOLDAMGBD228NLBM','fred',start,end)
gold.head()

"""### GDP"""

wb.search('gdp,*capita.*const')

code ="NY.GDP.PCAP.PP.KD"
matches=wb.search('gdp,*capita.*const')
data=wb.download(indicator=code, country=['JPN','KOR'],
                start=2011, end=2021)
data=data.reset_index(drop=False)
sns.lineplot(x="year",y=code,hue="country", data=data)

"""## kospi
 - 여기서 조합을 통해서 원하는 종목 추출 후 csv 형태로 저장
"""

kospi_cd=fdr.StockListing('KRX')
kospi_cd.tail()

kospi_cd.loc[kospi_cd["Industry"].str.find("드라마")>-1]

df= fdr.DataReader("253450",'2021')
sns.lineplot(x=df.index,y=df["Close"])

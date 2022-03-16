# !pip install xmltodict
from bs4 import BeautifulSoup as bs
import requests
import xmltodict
import pandas as pd


class JobService:
    def __init__(self):
        self.key = 'zTa2HPaDXF3mBGgFN1l0EkCP%2BOWRPIUmkAoGZeu8oQDco%2FUapbW7xPoDPCHaRGPP9A43rMTBBnljgtcas9rZxA%3D%3D'

    def getCovidinfo(self, busnm):
        url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
        pageNo = '1'
        numOfRows = '10'
        startCreateDt = '20191230'
        endCreateDt = '20220220'
        url += '?serviceKey=' + self.key + "&pageNo=" + pageNo + "&numOfRows=" + numOfRows + "&startCreateDt=" + startCreateDt + "&endCreateDt=" + endCreateDt
        req = requests.get(url).text
        xmlObject = xmltodict.parse(req)
        dict_data = xmlObject['response']['body']['items']['item']
        df = pd.DataFrame(dict_data)
        df = df.astype({'decideCnt': 'int', 'deathCnt': 'int'})
        df = df.drop_duplicates(['stateDt'])  # 중복 일자 제거
        df['date'] = df['stateDt']
        df['date'] = pd.to_datetime(df['date'])  # 날짜
        df_2 = df[['date', 'decideCnt', 'deathCnt']]
        df_2 = df_2.sort_values(by='date')  # 날짜정렬
        df_2['daily_decideCnt'] = df_2['decideCnt'].diff()
        df_2 = df_2.fillna(0)
        df_2 = df_2.astype({'daily_decideCnt': 'int'})
        return df_2
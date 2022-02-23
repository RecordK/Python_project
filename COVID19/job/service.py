# !pip install xmltodict
from bs4 import BeautifulSoup as bs
import requests
import xmltodict
import pandas as pd
import web_hello.bus_info.vo as vo
from web_hello.bus_info.dao_db import BusDao


class JobService:
    def __init__(self):
        self.key = 'zTa2HPaDXF3mBGgFN1l0EkCP%2BOWRPIUmkAoGZeu8oQDco%2FUapbW7xPoDPCHaRGPP9A43rMTBBnljgtcas9rZxA%3D%3D'
        self.dao = BusDao()

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

    def getStationinfo(self, id):  # param:[0, 2]
        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?'
        url += 'ServiceKey=' + self.key
        url += '&busRouteId=' + id
        html = requests.get(url).text  # url로 요청을 보내고 받은 응
        root = bs(html, 'lxml-xml')
        code = root.find('headerCd').get_text()
        if code != '0':
            msg = root.find('headerMsg').text
            print(msg)
            return
        stationList = root.find_all('itemList')
        # 순서 = root.find_all('seq')
        # 정류장명 = root.find_all('stationNm')
        res = []
        for i in stationList:
            a = i.find('seq').text
            b = i.find('stationNm').text
            c = i.find('direction').text
            res.append(vo.Station(id, a, b, c))
        return res

    def getBusinfoByBusid(self, busid):
        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getRouteInfo?'
        url += 'ServiceKey=' + self.key
        url += '&busRouteId=' + busid
        html = requests.get(url).text  # url로 요청을 보내고 받은 응
        root = bs(html, 'lxml-xml')
        code = root.find('headerCd').get_text()
        # 결과코드
        if code != '0':
            msg = root.find('headerMsg').text
            print(msg)
            return
        routeList = root.find_all('itemList')
        res = []
        for route in routeList:
            busRouteId = route.find('busRouteId').text
            busRouteNm = route.find('busRouteNm').text
            stStationNm = route.find('stStationNm').text
            edStationNm = route.find('edStationNm').text
            firstBusTm = route.find('firstBusTm').text
            lastBusTm = route.find('lastBusTm').text
            term = root.find('term').text

            res.append(
                vo.Bus(busid=busRouteId, busnm=busRouteNm, ststat=stStationNm, edstat=edStationNm, sttime=firstBusTm,
                       edtime=lastBusTm, term=term))

        return res

    def addMyBus(self, b: vo.Bus):
        self.dao.insert(b)

    def myBusList(self, id: str):
        data = self.dao.selectAll(id)
        return data

    def delbus(self, busid: str):
        self.dao.delete(busid)

import requests
import xmltodict
import time
import pandas as pd
import pyecharts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Bar, Bar3D, Grid, Line, Liquid, Page, Pie, Timeline, Tab, Map, Grid
from pyecharts import options as opts
serviceKey='zTa2HPaDXF3mBGgFN1l0EkCP%2BOWRPIUmkAoGZeu8oQDco%2FUapbW7xPoDPCHaRGPP9A43rMTBBnljgtcas9rZxA%3D%3D'
pageNo='1'
numOfRows='10'
startCreateDt='20191230'
endCreateDt='20210623'
url ='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
url=url+'?serviceKey='+serviceKey+"&pageNo="+pageNo+"&numOfRows=" +numOfRows+ "&startCreateDt="+startCreateDt + "&endCreateDt=" + endCreateDt
req=requests.get(url).text
#req2=requests.get(url).content
xmlObject=xmltodict.parse(req)
dict_data=xmlObject['response']['body']['items']['item']
df=pd.DataFrame(dict_data)
df = df.astype({'decideCnt' : 'int', 'examCnt' : 'int', 'deathCnt' : 'int'})
df = df.drop_duplicates(['stateDt']) #중복제거
df['date']=df['stateDt']
df['date'] = pd.to_datetime(df['date']) #시계열지정
df_2 = df[['date','decideCnt','examCnt','deathCnt']]
df_2 = df_2.sort_values(by='date') #diff()를 사용하기 위해서 날짜로 오름차순 정렬
df_2['daily_decideCnt'] = df_2['decideCnt'].diff()
test_Covid19= (Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
               .add_xaxis(df_2['date'].unique().astype(str).tolist())
               .add_yaxis('일일 확진자 수', df_2['daily_decideCnt'].tolist())
               ).set_global_opts(title_opts=opts.TitleOpts(title='COVID-19 일일확진자(대한민국)',pos_bottom="60%"),
                                 legend_opts=opts.LegendOpts(pos_bottom="55%",pos_right="10%",legend_icon='pin'),
                                 tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                                 datazoom_opts=[
                                     opts.DataZoomOpts(pos_bottom="65%",xaxis_index=2),
                                     opts.DataZoomOpts(pos_bottom="35%", xaxis_index=1),
                                     opts.DataZoomOpts(pos_bottom="3%", xaxis_index=0)
                                 ]
                                 ).set_series_opts(label_opts=opts.LabelOpts(is_show=False))
test_Covid19.render()
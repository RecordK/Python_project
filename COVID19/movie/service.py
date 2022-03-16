import joblib
import numpy as np
import re
from konlpy.tag import Okt
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.preprocessing import LabelEncoder


def data():
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey=735H810S461EXCLRX81S&'
    url += '&detail=N&listCount=1000'
    start1 = '20120101'
    end1 = '20220315'
    u1 = url + '&releaseDts=' + start1 + '&releaseDte=' + end1
    start2 = '20010101'
    end2 = '20120101'
    u2 = url + '&releaseDts=' + start2 + '&releaseDte=' + end2
    start3 = '19800101'
    end3 = '20010101'
    u3 = url + '&releaseDts=' + start3 + '&releaseDte=' + end3
    req1 = requests.get(u1).text
    req2 = requests.get(u2).text
    req3 = requests.get(u3).text
    d1 = json.loads(req1)
    d2 = json.loads(req2)
    d3 = json.loads(req3)
    # con=d['Data'][0]['Result'][0]['plots']['plot'][0]['plotText']
    # gen=d['Data'][0]['Result'][0]['genre']
    xdata1 = [d1['Data'][0]['Result'][i]['plots']['plot'][0]['plotText'] for i in
              range(len(d1['Data'][0]['Result']))]
    ydata1 = [d1['Data'][0]['Result'][i]['genre'] for i in range(len(d1['Data'][0]['Result']))]
    xdata2 = [d2['Data'][0]['Result'][i]['plots']['plot'][0]['plotText'] for i in
              range(len(d2['Data'][0]['Result']))]
    ydata2 = [d2['Data'][0]['Result'][i]['genre'] for i in range(len(d2['Data'][0]['Result']))]
    xdata3 = [d3['Data'][0]['Result'][i]['plots']['plot'][0]['plotText'] for i in
              range(len(d3['Data'][0]['Result']))]
    ydata3 = [d3['Data'][0]['Result'][i]['genre'] for i in range(len(d3['Data'][0]['Result']))]
    xdata = xdata1 + xdata2 + xdata3
    ydata = ydata1 + ydata2 + ydata3
    df = pd.DataFrame(ydata, xdata)
    df = df.reset_index()
    df.columns = ['줄거리', '장르']
    gen = []
    for i in df['장르'].tolist():
        gen.append(i.split(',')[0])
    df['장르'] = gen
    df.drop(df[df['장르'] == ''].index, inplace=True)
    df.loc[df['장르'] == '멜로드라마', '장르'] = '멜로/로맨스'
    df.loc[df['장르'] == '공포(호러)', '장르'] = '공포'
    df['줄거리'] = df['줄거리'].apply(lambda x: re.sub("^[ㄱ-ㅎ가-힣0-9]*$", " ", x))
    df['줄거리'] = df['줄거리'].apply(lambda x: re.sub(r"\d+", " ", x))
    x_data = df['줄거리']
    y_data = df['장르']
    encoder = LabelEncoder()
    labels = encoder.fit_transform(y_data)
    np.unique(labels)
    X_train, X_test, y_train, y_test = train_test_split(x_data, labels, test_size=0.3, random_state=121)
    return X_train


def data2():
    train_df = pd.read_csv('static/ratings_train.txt', sep='\t')
    train_df = train_df.fillna(' ')
    train_df['document'] = train_df['document'].apply(lambda x: re.sub(r"\d+", " ", x))
    train_df.drop('id', axis=1, inplace=True)

    return train_df['document']


class MovieService:
    def read_predFile(self):
        df = pd.read_excel('static/movie_review.xls', sheet_name='sheet1')
        return df

    def review_test(self):
        model = joblib.load('static/senti.pkl')
        tfidf_vect = TfidfVectorizer(tokenizer=MovieService.tw_tokenizer, ngram_range=(1, 2), min_df=3, max_df=0.9)
        df = data2()
        tfidf_vect.fit(df)
        df2 = self.read_predFile()
        input = df2['review'].apply(lambda x: re.sub("^[ㄱ-ㅎ가-힣0-9]*$", " ", x))
        input = input.apply(lambda x: re.sub(r"\d+", " ", x))
        tfidf_matrix_test = tfidf_vect.transform(input)
        pred = model.predict(tfidf_matrix_test)
        df2['pred'] = pred
        return df2.values

    def read_review(self, da: str):
        model = joblib.load('static/senti.pkl')
        tfidf_vect = TfidfVectorizer(tokenizer=MovieService.tw_tokenizer, ngram_range=(1, 2), min_df=3, max_df=0.9)
        df = data2()
        tfidf_vect.fit(df)
        input = da
        input = re.sub("^[ㄱ-ㅎ가-힣0-9]*$", " ", input)
        input = re.sub(r"\d+", " ", input)
        input = pd.Series(input)
        tfidf_matrix_test = tfidf_vect.transform(input)
        pred = model.predict(tfidf_matrix_test)
        return pred

    def genre_test(self, da: str):
        model = joblib.load('static/genre.pkl')
        df = data()
        twitter = Okt()
        tfidf_vect = TfidfVectorizer(tokenizer=twitter.morphs, ngram_range=(1, 2), min_df=3, max_df=0.9)
        tfidf_vect.fit(df)
        decoder = joblib.load('static/encoder.pkl')
        input = da
        input = re.sub("^[ㄱ-ㅎ가-힣0-9]*$", " ", input)
        input = re.sub(r"\d+", " ", input)
        input = pd.Series(input)
        input=np.array(input)
        tfidf_matrix_test = tfidf_vect.transform(input)
        pred = model.predict(tfidf_matrix_test)
        genre = decoder.inverse_transform(pred)
        return genre

    def tw_tokenizer(text):
        twitter = Okt()
        tokens_ko = twitter.morphs(text)
        return tokens_ko

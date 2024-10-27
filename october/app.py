# pip install flask
from flask import Flask, render_template, request, send_file
import requests
import json
import pandas as pd
import time
from datetime import datetime

import matplotlib.pyplot as plt
import cx_Oracle
# pip install flask-cors
from flask_cors import CORS


app = Flask(__name__)
# 모두 허용
CORS(app)

def oracle_data():
    try:
        # 오라클 연결
        conn = cx_Oracle.connect("october", "october", "localhost:1521/xe")
        cur = conn.cursor()

        # db에서 값 불러오기
        sql_sec = """
            SELECT SUBSTR(detailtime, 12, 8) AS sec
                  ,ROUND(AVG(REGEXP_REPLACE(sleep_g, '[^0-9.-]', ''))) as sleep
            FROM tb_data_241023
            WHERE SUBSTR(detailtime, 12, 8) < '07:00:00 ' 
            AND SUBSTR(detailtime, 1, 10) = '2024-10-24'
            GROUP BY SUBSTR(detailtime, 12, 8)
            ORDER BY SUBSTR(detailtime, 12, 8) ASC
        """
        df1 = pd.read_sql(sql_sec, conn)
        categories = df1['SEC'].tolist()
        series_data = [
            {
                'name': '무게',
                'data': df1['SLEEP'].tolist()  # 첫 번째 선에 해당하는 데이터
            }
        ]

    except Exception as e:
        print('db error :', e)
        conn.rollback() # 문제 발생시 이전 상태 리턴
    finally:
        cur.close()
        conn.close()

    return categories, series_data

def oracle_data_main():
    try:
        # 오라클 연결
        conn = cx_Oracle.connect("october", "october", "localhost:1521/xe")
        cur = conn.cursor()

        # db에서 값 불러오기
        sql_sec = """
            SELECT SUBSTR(detailtime, 12, 7) AS sec
                  ,ROUND(AVG(REGEXP_REPLACE(sleep_g, '[^0-9.-]', ''))) as sleep
            FROM tb_data_241023
            WHERE SUBSTR(detailtime, 12, 8) < '07:00:00 ' 
            AND SUBSTR(detailtime, 1, 10) = '2024-10-24'
            GROUP BY SUBSTR(detailtime, 12, 7)
            ORDER BY SUBSTR(detailtime, 12, 7) ASC
        """
        df1 = pd.read_sql(sql_sec, conn)
        categories_main = df1['SEC'].tolist()
        series_data_main = [
            {
                'name': '무게',
                'data': df1['SLEEP'].tolist()  # 첫 번째 선에 해당하는 데이터
            }
        ]

    except Exception as e:
        print('db error :', e)
        conn.rollback() # 문제 발생시 이전 상태 리턴
    finally:
        cur.close()
        conn.close()

    return categories_main, series_data_main

def oracle_data2():
    try:
        # 오라클 연결
        conn = cx_Oracle.connect("october", "october", "localhost:1521/xe")
        cur = conn.cursor()

        # db에서 값 불러오기
        sql_sec = """
            SELECT SUBSTR(detailtime, 12, 7) AS sec
          ,ROUND(AVG(REGEXP_REPLACE(sleep_g, '[^0-9.-]', ''))) as sleep
    FROM tb_data_241023
    WHERE SUBSTR(detailtime, 1, 10) = '2024-10-27'
    AND  SUBSTR(detailtime, 12, 8) > '03:40:25'
    AND  SUBSTR(detailtime, 12, 8) < '04:30:25'
    AND  ROUND(REGEXP_REPLACE(sleep_g, '[^0-9.-]', '')) > '30'
    GROUP BY SUBSTR(detailtime, 12, 7)
    ORDER BY SUBSTR(detailtime, 12, 7) ASC
        """
        df1 = pd.read_sql(sql_sec, conn)
        categories2 = df1['SEC'].tolist()
        series_data2 = [
            {
                'name': '무게',
                'data': df1['SLEEP'].tolist()  # 첫 번째 선에 해당하는 데이터
            }
        ]

    except Exception as e:
        print('db error :', e)
        conn.rollback() # 문제 발생시 이전 상태 리턴
    finally:
        cur.close()
        conn.close()

    return categories2, series_data2


def oracle_data_bar():

    # 오라클 연결
    conn = cx_Oracle.connect("october", "october", "localhost:1521/xe")
    cur = conn.cursor()

    # db에서 값 불러오기
    sql_sec = """
        SELECT SUBSTR(detailtime, 1, 10) AS day
              ,ROUND(AVG(REGEXP_REPLACE(sleep_g, '[^0-9.-]', ''))) as sleep_day
        FROM tb_data_241023
        GROUP BY SUBSTR(detailtime, 1, 10)
        ORDER BY SUBSTR(detailtime, 1, 10) ASC
    """
    df1 = pd.read_sql(sql_sec, conn)
    categories_day = df1['DAY'].tolist()
    series_data_day = [
        {
            'name': '무게',
            'data': df1['SLEEP_DAY'].tolist(),  # 첫 번째 선에 해당하는 데이터
            'type': 'column'
        }
    ]

    cur.close()
    conn.close()

    return categories_day, series_data_day



@app.route("/")
def index2():
    # 데이터를 읽어서 HTML로 넘겨줌
    categories, series_data = oracle_data2()
    categories_day, series_data_day = oracle_data_bar()
    return render_template('index2.html', categories=categories, series_data=series_data
                           ,categories_day=categories_day, series_data_day=series_data_day)

@app.route("/27")
def index26():
    # 데이터를 읽어서 HTML로 넘겨줌
    categories2, series_data2 = oracle_data2()
    return render_template('ora_graph.html',categories2=categories2, series_data2=series_data2)

@app.route("/24")
def index24():
    # 데이터를 읽어서 HTML로 넘겨줌
    categories, series_data = oracle_data()
    return render_template('ora_graph_test.html',categories=categories, series_data=series_data)

@app.route("/test")
def index3():
    # 데이터를 읽어서 HTML로 넘겨줌
    categories, series_data = oracle_data2()

    # 하드코딩
    categories_day = ['2024-10-21','2024-10-22','2024-10-23','2024-10-24', '2024-10-25', '2024-10-26']  # 원하는 날짜 리스트
    series_data_day = [
        {
            'name': '수면시간',
            'data': [7.7, 7.4, 4.88, 6.17, 3.1, 3.58],  # 원하는 수면시간 데이터 리스트
            'type': 'column'
        }
    ]

    return render_template('index3.html', categories=categories, series_data=series_data
                           ,categories_day=categories_day, series_data_day=series_data_day)


if __name__ == '__main__':
    # app.run(debug=True) 디폴트 포트 지정 5000, 단순로컬호스트
    app.run(debug=True, port=5500, host="0.0.0.0") # 로컬 호스트로도, 휴대폰 ip로도 접근 가능. 즉, 배포가능





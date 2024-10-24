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
    categories, series_data = oracle_data()
    categories_day, series_data_day = oracle_data_bar()
    return render_template('index2.html', categories=categories, series_data=series_data
                           ,categories_day=categories_day, series_data_day=series_data_day)


if __name__ == '__main__':
    # app.run(debug=True) 디폴트 포트 지정 5000, 단순로컬호스트
    app.run(debug=True, port=5500, host="0.0.0.0") # 로컬 호스트로도, 휴대폰 ip로도 접근 가능. 즉, 배포가능





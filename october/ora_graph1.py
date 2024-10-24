import time
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import cx_Oracle

# oracle 접속
conn = cx_Oracle.connect("october", "october", "localhost:1521/xe")
cur = conn.cursor()

# 실행할 쿼리 기입
sql_yearly = """
    SELECT SUBSTR(detailtime, 1, 4) AS year
         , sleep_g 
    FROM tb_data3
    ORDER BY year ASC
"""
sql_monthly = """
    SELECT SUBSTR(detailtime, 1, 7) AS month
         , sleep_g 
    FROM tb_data3
    ORDER BY month ASC
"""
sql_daily = """
    SELECT SUBSTR(detailtime, 1, 10) AS day
         , sleep_g 
    FROM tb_data3
    ORDER BY day ASC
"""

sql_1 = """
    SELECT SUBSTR(detailtime, 12) AS timedata
         , sleep_g as sleep
    FROM tb_data3
    ORDER BY timedata ASC
"""

sql_sec = """
    SELECT SUBSTR(detailtime, 12, 8) AS sec
          ,ROUND(AVG(REGEXP_REPLACE(sleep_g, '[^0-9.-]', ''))) as sleep
    FROM tb_data_241023
    WHERE SUBSTR(detailtime, 12, 8) < '07:00:00 ' 
    GROUP BY SUBSTR(detailtime, 12, 8)
    ORDER BY SUBSTR(detailtime, 12, 8) ASC
"""

# DataFrame에 SQL쿼리 결과 저장
df1 = pd.read_sql(sql_sec, conn)

# 결과 출력
print(df1)

# 차트로 처리할 항목을 Series에 별도로 담는다.
c_sales = df1['SLEEP']
c_sales.index = df1['SEC']
# .sort_values(ascending = True)

plt.figure(figsize=(11,9))
c_sales.plot(label='Weight (g)', title= "sample data")
plt.legend(loc='lower left')
plt.grid(False)
plt.savefig('sample_data_sec.png')
plt.show()









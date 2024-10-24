# pip install cx_Oracle
import time
import serial
import cx_Oracle

conn = cx_Oracle.connect("october", "october", "localhost:1521/xe")
cur = conn.cursor()

sql = """

        INSERT INTO tb_data(data)
        VALUES(:1)

"""

arduino = serial.Serial('COM7', 9600)
time.sleep(2)

while True:
    try:
        a = arduino.readline()
        try:
            a = a.decode('utf-8')  # UTF-8 디코드 시도
        except UnicodeDecodeError:
            a = a.decode('latin1')  # UTF-8 디코드 실패 시 다른 인코딩 시도
        print(a)  # 처리된 데이터 출력

        cur.execute(sql, [a])
        conn.commit()
    except Exception as e:
        print(f"오류 발생: {e}")


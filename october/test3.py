import time
from datetime import datetime
import serial

# 아두이노 보드의 포트 번호와 보드레이트 설정
# 'arduino'변수에 시리얼 통신이 'com3'번에 연결, 보드레이트는 9600
arduino = serial.Serial('COM7', 9600)
time.sleep(2)

while True:
    try:
        a = arduino.readline()

        try:
            a = a.decode('utf-8')  # UTF-8 디코드 시도
        except UnicodeDecodeError:
            a = a.decode('latin1')  # UTF-8 디코드 실패 시 다른 인코딩 시도
        # print(a)  # 처리된 데이터 출력
        sleep_g = a
        now = time.time()  # create timestamp
        dt = datetime.fromtimestamp(now)
        detailtime = str(dt)

        print('측정 무게(g): ' + sleep_g + '측정 시간: ' + str(dt) + '\n')

    except Exception as e:
        print(f"오류 발생: {e}")



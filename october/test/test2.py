# pip install pySerial
# python -m pip install -U pip

import serial  # 'serial' 모듈 설치 / 시리얼 통신 설정
import time  # 'time' 모듈 설치 / 시간 설정

arduino = serial.Serial('com5', 9600)
# 'arduino' 변수에 시리얼 통신이 'com6'번에 연결되어 있고
# 보드레이트가 '9600'이다.
# 'arduino' 변수는 아두이노 보드에 데이터를 보낼 때 사용
time.sleep(1)

print("1을 입력하면 LED ON & '0'을 입력하면 LED OFF")
# python shell에 내보내는 출력문

while 1:  # 참이면 실행해라. 즉, 초기값은 '참'이기 때문에 계속 실행.
          # 아두이노의 loop()와 같은 구조

    var = input()  # 키보드로 입력한 데이터 'var'에 저장

    if (var == '1'):
        # 아두이노에게 'var'값을 보내기 위해 'utf-8'형식으로 인코딩
        var = var.encode('utf-8')
        # 인코드된 'var'의 값을 시리얼 통신을 통해 아두이노 프로그램으로 전송(write)
        # 즉, 파이썬에서 데이터를 입력하면 그 데이터를 아두이노가 받아서 작동
        arduino.write(var)
        # shell에 내보내기 위한 출력문
        print("LED turned ON")
        time.sleep(1)

    if (var == '0'):
        var = var.encode('utf-8')
        arduino.write(var)
        print("LED turned OFF")
        time.sleep(1)
# -*- coding: utf-8 -*-

import serial
import time
import threading

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# シリアルポートをオープン
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
ser.flush()

def send_data(message):
    """指定されたメッセージをシリアルポートに送信する"""
    ser.flush()
    print("NG")
    ser.write(message.encode("utf-8"))
    print("PASS")
    # ser.write(message)
    print(f"Sent: {message}")

def receive_data():
    """シリアルポートからデータを受信する"""
    if ser.in_waiting > 0:  # データが待機中かどうかを確認
        data = ser.read(ser.in_waiting).decode('utf-8').strip()
        if data:
            print(f"Received: {data}")

def count_up(count, command):
    """100msごとにカウントアップした数字をシリアルポートに送信する"""
    message = f"@{command:03d}:{count:06d}\n"
    send_data(message)
    count += 5
    # 次のタイマーをセット
    threading.Timer(0.1, count_up, args=(count, command)).start()

try:
    # 初期値
    initial_count = 0
    command = 0
    
    # カウントアップ処理を開始
    count_up(initial_count, command)
    
    # データ受信処理を実行
    while True:
        receive_data()
        time.sleep(0.01)  # CPU負荷を軽減するために少し待機

except KeyboardInterrupt:
    print("ユーザーによって中断されました")
finally:
    ser.close()  # シリアルポートを閉じる

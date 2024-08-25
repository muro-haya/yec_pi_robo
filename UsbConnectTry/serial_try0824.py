import serial
import time

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# シリアルポートをオープン
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_data(message):
    """指定されたメッセージをシリアルポートに送信する"""
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")

def receive_data():
    """シリアルポートからデータを受信する"""
    data = ser.readline().decode('utf-8').strip()
    if data:
        print(f"Received: {data}")


def count_up():
    """100msごとにカウントアップした数字をシリアルポートに送信する"""
    count = 0
    command = 0
    while True:
        time.sleep(0.1)  # 100ms待機
        message = f"@{command:03d}:{count:06d}\n"
        send_data(message)
        count += 5

try:
    while True:
        receive_data()  # データ受信
        #count_up()  # カウントアップ処理
except KeyboardInterrupt:
    print("ユーザーによって中断されました")
finally:
    ser.close()  # シリアルポートを閉じる

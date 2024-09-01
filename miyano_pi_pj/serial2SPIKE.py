import serial
import time
import threading

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# シリアルポートをオープン
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_data(command,value):
    """指定されたメッセージをシリアルポートに送信する"""
    message = f"@{command:03d}:{value:06d}\n"
    ser.flush()
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")
    # 次のタイマーをセット
    threading.Timer(0.1, send_data, args=(command,value)).start()


def receive_data():
    """シリアルポートからデータを受信する"""
    if ser.in_waiting > 0:  # データが待機中かどうかを確認
        data = ser.read(ser.in_waiting).decode('utf-8').strip()
        if data:
            print(f"Received: {data}")

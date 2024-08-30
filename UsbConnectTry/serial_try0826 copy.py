import serial
import time
import threading

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 9600

# グローバル変数の初期化
count = 0
command = 0

# シリアルポートをオープン
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_data(message):
    """指定されたメッセージをシリアルポートに送信する"""
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")

def receive_data():
    """シリアルポートからデータを受信する"""
    while True:
        if ser.in_waiting > 0:  # データが待機中かどうかを確認
            data = ser.read(ser.in_waiting).decode('utf-8').strip()
            if data:
                print(f"Received: {data}")

def count_up():
    """カウントアップした数字をシリアルポートに送信する"""
    global count
    while True:
        message = f"@{command:03d}:{count:06d}\n"
        send_data(message)
        count += 5
        time.sleep(0.5)

try:
    # シリアル処理を開始
    thread_1 = threading.Thread(target=receive_data)
    thread_2 = threading.Thread(target=count_up)
    thread_1.start()
    thread_2.start()
        
    # メインループを実行
    while True:
        time.sleep(0.01)  # CPU負荷を軽減するために少し待機

except KeyboardInterrupt:
    print("ユーザーによって中断されました")
finally:
    ser.close()  # シリアルポートを閉じる
    print("シリアルポートが閉じられました。")

import serial
import time
import threading

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

# シリアルポートをオープン
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_data(message):
    """指定されたメッセージをシリアルポートに送信する"""
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")

def receive_data():
    """シリアルポートからデータを受信し、条件に応じてレスポンスを送信する"""
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            # if data == "1":
            #     send_data("4")  # 「1」を受信したら「4」を送信
            # elif data == "2":
            #     send_data("5")  # 「2」を受信したら「5」を送信
            # elif data == "3":
            #     send_data("6")  # 「3」を受信したら「6」を送信
            # else:
            #     send_data("100")  # その他のデータを受信したら「100」を送信
            print(f"Received: {data}")

def count_up():
    """100msごとにカウントアップした数字をシリアルポートに送信する"""
    count = 0
    command = 0
    while True:
        # カウントを6桁のゼロ埋め形式でフォーマットする
        message = f"{command:04d}:{count:06d}"
        send_data(message)
        #print(f"Count Sent: {message}")
        count += 1
        time.sleep(0.1)  # 100ms待機

# スレッドを使って受信処理を実行
receive_thread = threading.Thread(target=receive_data, daemon=True)
receive_thread.start()

# メインスレッドでカウントアップ処理を実行
count_up()

import serial
import time
import threading

comm_tx_cnt = 0
comm_rx_cnt = 0
g_s32_comm_rx_jdg_red = 0

comm_rx_dbg = 0

received_param = [0,0,0,0,0,0,0,0,0,0]
received_watch = [0,0,0,0,0,0,0,0,0,0]
send_param     = [0,0,0,0,0,0,0,0,0,0]

received_cmd_buff = []
received_data_buff = []
buffer_num = 0

# 通信データ構造
class CommData:
    def __init__(self, comm_cnt, comm_cyc, comm_cmd, comm_data):
        self.comm_cnt = comm_cnt
        self.comm_cyc = comm_cyc
        self.comm_cmd = comm_cmd
        self.comm_data = comm_data
        
# 送信データ
tx_datas = [
    CommData(0,  10, 0, lambda: comm_rx_cnt),
    CommData(1,  10, 1, lambda: g_s32_comm_rx_jdg_red),

    CommData(0, None, 100, lambda: send_param[0]),
    CommData(0, None, 101, lambda: send_param[1]),
    CommData(0, None, 102, lambda: send_param[2]),
    CommData(0, None, 103, lambda: send_param[3]),
    CommData(0, None, 104, lambda: send_param[4]),
    CommData(0, None, 105, lambda: send_param[5]),
    CommData(0, None, 106, lambda: send_param[6]),
    CommData(0, None, 107, lambda: send_param[7]),
    CommData(0, None, 108, lambda: send_param[8]),
    CommData(0, None, 109, lambda: send_param[9])
]

# 受信データ
rx_datas = [
    CommData(0, 100, 500,  comm_tx_cnt),
    CommData(0, 100, 501,  comm_rx_cnt),
    CommData(0, 100, 502,  comm_rx_dbg),

    CommData(0, 100, 600,  received_watch[0]),
    CommData(0, 100, 601,  received_watch[1]),
    CommData(0, 100, 602,  received_watch[2]),
    CommData(0, 100, 603,  received_watch[3]),
    CommData(0, 100, 604,  received_watch[4]),
    CommData(0, 100, 605,  received_watch[5]),
    CommData(0, 100, 606,  received_watch[6]),
    CommData(0, 100, 607,  received_watch[7]),
    CommData(0, 100, 608,  received_watch[8]),
    CommData(0, 100, 609,  received_watch[9]),

    CommData(0, 100, 700,  received_param[0]),
    CommData(0, 100, 701,  received_param[1]),
    CommData(0, 100, 702,  received_param[2]),
    CommData(0, 100, 703,  received_param[3]),
    CommData(0, 100, 704,  received_param[4]),
    CommData(0, 100, 705,  received_param[5]),
    CommData(0, 100, 706,  received_param[6]),
    CommData(0, 100, 707,  received_param[7]),
    CommData(0, 100, 708,  received_param[8]),
    CommData(0, 100, 709,  received_param[9])
]

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# シリアルポートをオープン
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def set_comm_ui():
    for data_info in rx_datas:
        index = 0
        for cmd in range(600,609):
            if cmd == data_info.comm_cmd:
                received_watch[index] = int(data_info.comm_data)
            index += 1
        index = 0
        for cmd in range(700,709):
            if cmd == data_info.comm_cmd:
                received_param[index] = int(data_info.comm_data)
            index += 1
    return received_watch, received_param

def input_comm():
    return

def send_data(command,value):
    """指定されたメッセージをシリアルポートに送信する"""
    message = f"@{command:03d}:{value:06d}\n"
    ser.flush()
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")
    # 次のタイマーをセット
    # threading.Timer(0.1, send_data, args=(command,value)).start()

def received_data():
    received_cmd_buff.clear()
    received_data_buff.clear()
    data = ser.read(ser.in_waiting).decode('utf-8').strip()
    if data:
        print(f"Received: {data}")
        # split '@'
        if '@' in data:
            split_datas = data.split('\r\n')
        else:
            print("Input string must contain '@'")
            return None,None,None
        buffer_num = len(split_datas)
        for split_data in split_datas:
            # split ':'
            if ':' in split_data:
                cmd, value = split_data.split(':', 1)
                cmd = cmd[1:]
                received_cmd_buff.append(cmd)
                received_data_buff.append(value)
                print(cmd, value)
            else:
                print("Input string must contain ':' after'@'")
                return None,None,None
        return received_cmd_buff,received_data_buff,buffer_num
    return None,None,None

def cyc_tx():
    global comm_rx_cnt
    for data in tx_datas:
        if data.comm_cyc == None:
            continue
        if data.comm_cyc == data.comm_cnt:
            send_data(data.comm_cmd, data.comm_data())
            data.comm_cnt = 0
        data.comm_cnt += 1
    comm_rx_cnt += 1

def cyc_rx():
    global rx_datas
    """シリアルポートからデータを受信する"""
    if ser.in_waiting > 0:  # データが待機中かどうかを確認
        cmd, data, buf_num = received_data()
        if buf_num == None:
            return
        print(cmd)
        print(data)
        for i in range(buf_num):
            for data_info in rx_datas:
                # print(cmd[i])
                # print(data_info.comm_cmd)
                if cmd == None:
                    continue
                if int(cmd[i]) == data_info.comm_cmd:
                    print(int(data[i]))
                    data_info.comm_data = int(data[i])
                    print("inf")
                    print(int(cmd[i]), data_info.comm_data)
                    break

def close():
    ser.close()  # シリアルポートを閉じる
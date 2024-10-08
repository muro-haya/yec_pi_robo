import serial
import time
import camera

comm_tx_cnt = 0
comm_rx_cnt = 0
g_s32_comm_rx_jdg_red   = 0
g_u16_comm_pet_xpos = 0
g_u16_comm_pet_xpos_bl  = 0
g_u16_comm_pet_flg      = 0
g_u16_comm_pet_srt      = 0

comm_rx_dbg = 0

received_cnt = 0

received_datas = [0,0,0,0,0,0,0,0,0,0]
received_param = [0,0,0,0,0,0,0,0,0,0]
received_watch = [0,0,0,0,0,0,0,0,0,0]
send_param     = [0,0,0,0,0,0,0,0,0,0]

received_cmd_buff = []
received_data_buff = []
buffer_num = 0

# 通信データ構造
class CommData:
    def __init__(self, comm_cnt, comm_cyc, comm_cmd, comm_sign, comm_data):
        self.comm_cnt = comm_cnt
        self.comm_cyc = comm_cyc
        self.comm_cmd = comm_cmd
        self.comm_sign = comm_sign # 0:unsign 1:sign
        self.comm_data = comm_data
        
# 送信データ
tx_datas = [
    CommData(0,   10,   0, 0, lambda: comm_rx_cnt            ),
    CommData(1,   10,   1, 0, lambda: g_s32_comm_rx_jdg_red  ),
    CommData(2,   10,   2, 0, lambda: g_u16_comm_pet_xpos    ),
    CommData(2,   10,   3, 0, lambda: g_u16_comm_pet_xpos_bl ),
    CommData(2,   10,   4, 0, lambda: g_u16_comm_pet_flg     ), # pet bottole(0:None 1:red :blue)

    CommData(0, None, 100, 0, lambda: send_param[0]),
    CommData(0, None, 101, 0, lambda: send_param[1]),
    CommData(0, None, 102, 0, lambda: send_param[2]),
    CommData(0, None, 103, 0, lambda: send_param[3]),
    CommData(0, None, 104, 0, lambda: send_param[4]),
    CommData(0, None, 105, 0, lambda: send_param[5]),
    CommData(0, None, 106, 0, lambda: send_param[6]),
    CommData(0, None, 107, 0, lambda: send_param[7]),
    CommData(0, None, 108, 0, lambda: send_param[8]),
    CommData(0, None, 109, 0, lambda: send_param[9])
]

# 受信データ
rx_datas = [
    CommData(0, 100, 500,  0, received_datas[0] ),  # comm_tx_cnt
    CommData(0, 100, 501,  0, received_datas[1] ),  # comm_rx_cnt
    CommData(0, 100, 502,  0, received_datas[2] ),  # comm_rx_dbg
    CommData(0, 100, 503,  0, received_datas[3] ),  # g_u16_comm_pet_srt

    CommData(0, 100, 600,  1, received_watch[0]),
    CommData(0, 100, 601,  1, received_watch[1]),
    CommData(0, 100, 602,  1, received_watch[2]),
    CommData(0, 100, 603,  1, received_watch[3]),
    CommData(0, 100, 604,  1, received_watch[4]),
    CommData(0, 100, 605,  1, received_watch[5]),
    CommData(0, 100, 606,  1, received_watch[6]),
    CommData(0, 100, 607,  1, received_watch[7]),
    CommData(0, 100, 608,  1, received_watch[8]),
    CommData(0, 100, 609,  1, received_watch[9]),

    CommData(0, 100, 700,  1, received_param[0]),
    CommData(0, 100, 701,  1, received_param[1]),
    CommData(0, 100, 702,  1, received_param[2]),
    CommData(0, 100, 703,  1, received_param[3]),
    CommData(0, 100, 704,  1, received_param[4]),
    CommData(0, 100, 705,  1, received_param[5]),
    CommData(0, 100, 706,  1, received_param[6]),
    CommData(0, 100, 707,  1, received_param[7]),
    CommData(0, 100, 708,  1, received_param[8]),
    CommData(0, 100, 709,  1, received_param[9])
]

# シリアルポートの設定
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600


def set_comm_ui():
    return received_watch, received_param

def set_comm_cam():
    return g_u16_comm_pet_srt

def input_comm():
    return

def serial_init():
    global ser
    try:
        # シリアルポートをオープン
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        return True
    except serial.SerialException as e:
        print("NONE")
        return False

def serial_reset():
    try:
        print("ERR")
        ser.close()
        time.sleep(0.3)
        ser.open()
    except serial.SerialException as e:
        print("OH,NO")

def send_data(command,value):

    """指定されたメッセージをシリアルポートに送信する"""
    message = f"@{command:03d}:{value:06d}\n"
    # ser.flush()
    try:
        ser.write(message.encode('utf-8'))
    except serial.SerialTimeoutException:
        serial_reset()
    except serial.SerialException as e:
        serial_reset()
    except Exception:
        serial_reset()
    print(f"Sent: {message}")
    # 次のタイマーをセット
    # threading.Timer(0.1, send_data, args=(command,value)).start()

def received_data():

    received_cmd_buff.clear()
    received_data_buff.clear()
    # ser.flush()

    try:
        data = ser.read(ser.in_waiting).decode('utf-8').strip()
    except serial.SerialTimeoutException:
        serial_reset()
    except serial.SerialException as e:
        serial_reset()
    except Exception:
        serial_reset()
    if data:
        received_cnt = 0
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
                # print(cmd, value)
            else:
                print("Input string must contain ':' after'@'")
                serial_reset()
                return None,None,None
        return received_cmd_buff,received_data_buff,buffer_num
    return None,None,None

def cyc_tx():
    global received_cnt

    global comm_rx_cnt
    global g_u16_comm_pet_xpos
    global g_u16_comm_pet_flg

    g_u16_comm_pet_xpos,g_u16_comm_pet_flg = camera.set_cam_comm()

    for data in tx_datas:
        if data.comm_cyc == None:
            continue
        if data.comm_cyc == data.comm_cnt:
            send_data(data.comm_cmd, data.comm_data())
            data.comm_cnt = 0
        data.comm_cnt += 1
    comm_rx_cnt += 1

    if 500 < received_cnt:
        print("RESET")
        received_cnt = 0
        return True
    else:
        received_cnt += 1
        return False

def cyc_rx():
    global rx_datas
    global comm_tx_cnt
    global comm_rx_cnt
    global comm_rx_dbg
    global g_u16_comm_pet_srt
    global received_datas
    global received_param
    global received_watch

    """シリアルポートからデータを受信する"""
    try:
        ser_wait = ser.in_waiting
    except serial.SerialException as e:
        serial_reset()
        ser_wait = 0
    if ser_wait > 0:  # データが待機中かどうかを確認
        cmd, data, buf_num = received_data()
        if buf_num == None:
            return
        for i in range(buf_num):
            for data_info in rx_datas:
                if cmd == None:
                    continue
                if cmd[i].isdigit():
                    if int(cmd[i]) == data_info.comm_cmd:
                        try:
                            dat = int(cmd[i])
                            if 600 > dat:
                                dat -= 500
                                received_datas[dat] = int(data[i])
                            elif 700 > dat:
                                tmp_val = int(data[i])
                                dat -= 600
                                if 0 == data_info.comm_sign:
                                    received_watch[dat] = tmp_val
                                else:
                                    if tmp_val >= 32767:
                                        received_watch[dat] = tmp_val - 65536
                                    else:
                                        received_watch[dat] = tmp_val
                            elif 800 > dat:
                                dat -= 700
                                received_param[dat] = int(data[i])
                            
                            continue
                        except(ValueError, TypeError):
                            continue
        comm_tx_cnt        = received_datas[0]
        comm_rx_cnt        = received_datas[1]
        comm_rx_dbg        = received_datas[2]
        g_u16_comm_pet_srt = received_datas[3]

def close():
    ser.close()  # シリアルポートを閉じる

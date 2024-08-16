# https://ohtayo.hatenablog.com/entry/2020/03/31/222007

import serial
import  threading


ser = serial.Serial('/dev/ttyACM0', '115200', timeout=1)

message: int = 128
messageTx = message.to_bytes(1,'little')


def SendMessage():
    while(1):
        line = ser.readline()
        ser.write(messageTx)  
        print(messageTx)
        if(line==b'a'):  
            break 

thread = threading.Thread(target=SendMessage)
#thread = threading.Timer(1,SendMessage)
thread.start()  
thread.join()  
ser.close()  

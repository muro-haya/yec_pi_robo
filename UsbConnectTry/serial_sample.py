# https://ohtayo.hatenablog.com/entry/2020/03/31/222007

import serial
import threading

ser = serial.Serial('/dev/ttyACM1', '115200', timeout=0.1)

def receive():
    while(1):
        line = ser.readline()
        if(len(line)>0):
            print(line)  
        if(line==b'test_str'):  
            break  


thread = threading.Thread(target=receive)  
thread.start()  
ser.write(b'test_str')  
thread.join()  
ser.close()  

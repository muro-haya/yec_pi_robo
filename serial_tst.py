import time
import serial,time

ser = serial.Serial('/dev/ttyAMA1',115200)

while True:
    if ser.in_waiting:
        x=ser.readline()
        
        ser.write(b'read:%s\n'%x)
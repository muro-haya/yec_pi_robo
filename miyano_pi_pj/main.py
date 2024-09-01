import threading

#import camera
import serial2SPIKE
import ui

def main():
    command = 0
    value = 0

    # データ送信を開始
    serial2SPIKE.send_data(command,value)    

    while(1):
        serial2SPIKE.receive_data()
        
        #end_jdg = camera.cyc_camera()
        #if( True == end_jdg ):
        #    break

    #camera.end_camera()


if __name__ == "__main__":
    main()
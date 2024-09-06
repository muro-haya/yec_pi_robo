import threading

import camera
import serial2SPIKE
import ui
import csv_log

def main():
    ui.ini_ui()

    while(1):
        serial2SPIKE.cyc_rx()
        serial2SPIKE.cyc_tx() 
        csv_log.cyc_log()
        ui.cyc_ui()
        end_jdg = camera.cyc_camera()
        if( True == end_jdg ):
           break

    camera.end_camera()
    ui.end_ui()
    serial2SPIKE.close()  # シリアルポートを閉じる

if __name__ == "__main__":
    main()
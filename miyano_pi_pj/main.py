import camera
import serial2SPIKE
import ui
import csv_log

serial_ini_flg = 0

def main():
    global serial_ini_flg

    ui.ini_ui()
    
    cnt = 0

    while(1):
        if False == serial_ini_flg:
            serial_ini_flg = serial2SPIKE.serial_init()
        else:
            serial2SPIKE.cyc_rx()
            if 100 < cnt:
                serial2SPIKE.cyc_tx()
            else:
                cnt += 1
        csv_log.cyc_log()
        ui.cyc_ui()
        camera.cyc_camera()
        end_jdg = ui.set_ui_main()
        if True == end_jdg:
           break

    camera.end_camera()
    ui.end_ui()
    serial2SPIKE.close()  # シリアルポートを閉じる

if __name__ == "__main__":
    main()
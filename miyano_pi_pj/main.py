import threading

import camera
import ui

def main():
    ui.ini_ui()
    while(1):
        ui.cyc_ui()
        end_jdg = camera.cyc_camera()
        if( True == end_jdg ):
            break

    camera.end_camera()
    ui.end_ui()


if __name__ == "__main__":
    main()
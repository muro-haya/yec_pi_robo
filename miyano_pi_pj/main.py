import threading

import camera
import serial
import ui

def main():
    
    while(1):
        end_jdg = camera.cyc_camera()
        if( True == end_jdg ):
            break

    camera.end_camera()


if __name__ == "__main__":
    main()
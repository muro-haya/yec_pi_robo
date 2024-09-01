import cv2
from datetime import datetime

# /dev/video0を指定
DEV_ID = 0

# パラメータ
WIDTH = 640
HEIGHT = 480

def main():
    # /dev/video0を指定
    cap = cv2.VideoCapture(DEV_ID)

    while( cap.isOpened() ):
        # キャプチャの実施
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow("camera", frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return


if __name__ == "__main__":
    main()
import cv2
from datetime import datetime

# /dev/video0を指定
DEV_ID = 0

# /dev/video0を指定
cap = cv2.VideoCapture(DEV_ID)

def cyc_camera():
    if( cap.isOpened() ):
        # キャプチャの実施
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow("camera", frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        return True
    else:
        return False

def end_camera():
    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return
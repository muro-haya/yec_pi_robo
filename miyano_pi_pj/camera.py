import cv2
import numpy as np
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
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_blue = np.array([50, 150, 100])
            upper_blue = np.array([140, 255, 255])

            # Get the image dimensions
            height, width = frame.shape[:2]
            # Create a white image of the same size as the original image
            white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            white_result = cv2.bitwise_and(white_image, white_image, mask=mask)
            result = cv2.bitwise_and(frame, frame, mask=mask)

            # Define a kernel for morphological operations
            kernel = np.ones((5, 5), np.uint8)
            # Apply erosion
            eroded_image = cv2.erode(white_result, kernel, iterations=1)
            # Apply dilation
            dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
            kernel = np.ones((20, 20), np.uint8)
            # Apply erosion
            eroded_image2 = cv2.erode(dilated_image, kernel, iterations=1)
            # Apply dilation
            dilated_image2 = cv2.dilate(eroded_image2, kernel, iterations=1)

            gray2 = cv2.cvtColor(dilated_image2,cv2.COLOR_BGR2GRAY)
            edges2 = cv2.Canny(gray2, 50, 150)
            contours2, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(dilated_image2, contours2, -1, (0,255,0), 2)

            for contour in contours2:
                epsilon = 0.05 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) == 4:
                    cv2.drawContours(frame, [approx], -1, (0,255,0), 2)

            cv2.imshow("camera", frame)
            # cv2.imshow("edge", dilated_image2)
            # cv2.imshow("mask", result)
            # cv2.imshow("white_mask", white_result)

    if cv2.waitKey(1) & 0xff == ord('q'):
        return True
    else:
        return False

def end_camera():
    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return
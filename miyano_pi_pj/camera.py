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
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_blue = np.array([50, 150, 100])
            upper_blue = np.array([140, 255, 255])

            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([40, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])

            # Get the image dimensions
            height, width = frame.shape[:2]
            # Create a white image of the same size as the original image
            white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = mask_red1 | mask_red2

            white_result_blue = cv2.bitwise_and(white_image, white_image, mask=mask_blue)
            white_result_red  = cv2.bitwise_and(white_image, white_image, mask=mask_red)

            # Define a kernel for morphological operations
            kernel = np.ones((5, 5), np.uint8)
            eroded_image_blue  = cv2.erode(white_result_blue, kernel, iterations=1)     # Apply erosion
            dilated_image_blue = cv2.dilate(eroded_image_blue, kernel, iterations=1)    # Apply dilation
            eroded_image_red   = cv2.erode(white_result_red, kernel, iterations=1)      # Apply erosion
            dilated_image_red  = cv2.dilate(eroded_image_red, kernel, iterations=1)     # Apply dilation

            kernel = np.ones((20, 20), np.uint8)
            eroded_image2_blue  = cv2.erode(dilated_image_blue, kernel, iterations=1)   # Apply erosion
            dilated_image2_blue = cv2.dilate(eroded_image2_blue, kernel, iterations=1)  # Apply dilation
            eroded_image2_red   = cv2.erode(dilated_image_red, kernel, iterations=1)    # Apply erosion
            dilated_image2_red  = cv2.dilate(eroded_image2_red, kernel, iterations=1)   # Apply dilation

            gray = cv2.cvtColor(dilated_image2_blue,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(dilated_image2_blue, contours, -1, (0,255,0), 2)
            for contour in contours:
                epsilon = 0.05 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) == 4:
                    cv2.drawContours(frame, [approx], -1, (255,0,0), 2)
                    
            gray = cv2.cvtColor(dilated_image2_red,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(dilated_image2_red, contours, -1, (0,255,0), 2)
            for contour in contours:
                epsilon = 0.05 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) == 4:
                    cv2.drawContours(frame, [approx], -1, (0,0,255), 2)

            cv2.imshow("camera", frame)
            # cv2.imshow("edge", dilated_image2_blue)
            # cv2.imshow("edge", dilated_image2_red)
            # cv2.imshow("white_mask", white_result_blue)
            # cv2.imshow("white_mask", white_result_red)

    if cv2.waitKey(1) & 0xff == ord('q'):
        return True
    else:
        return False

def end_camera():
    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return
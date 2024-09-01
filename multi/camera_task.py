import cv2
import numpy as np
import threading

class CameraTask:
    def __init__(self, dev_id=0):
        self.cap = cv2.VideoCapture(dev_id)
        self.frame = None
        self.running = True

    def start(self):
        self.thread = threading.Thread(target=self._capture, daemon=True)
        self.thread.start()

    def _capture(self):
        while self.running:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)

                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    lower_blue = np.array([50, 150, 100])
                    upper_blue = np.array([140, 255, 255])

                    height, width = frame.shape[:2]
                    white_image = np.ones((height, width, 3), dtype=np.uint8) * 255
                    mask = cv2.inRange(hsv, lower_blue, upper_blue)

                    white_result = cv2.bitwise_and(white_image, white_image, mask=mask)
                    result = cv2.bitwise_and(frame, frame, mask=mask)

                    kernel = np.ones((5, 5), np.uint8)
                    eroded_image = cv2.erode(white_result, kernel, iterations=1)
                    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
                    kernel = np.ones((20, 20), np.uint8)
                    eroded_image2 = cv2.erode(dilated_image, kernel, iterations=1)
                    dilated_image2 = cv2.dilate(eroded_image2, kernel, iterations=1)

                    gray2 = cv2.cvtColor(dilated_image2, cv2.COLOR_BGR2GRAY)
                    edges2 = cv2.Canny(gray2, 50, 150)
                    contours2, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cv2.drawContours(dilated_image2, contours2, -1, (0, 255, 0), 2)

                    for contour in contours2:
                        epsilon = 0.05 * cv2.arcLength(contour, True)
                        approx = cv2.approxPolyDP(contour, epsilon, True)
                        if len(approx) == 4:
                            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

                    self.frame = frame

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.cap.release()

    def __del__(self):
        self.stop()

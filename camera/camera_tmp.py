import cv2
import numpy as np
import time

# /dev/video0を指定
DEV_ID = 0

# /dev/video0を指定
cap = cv2.VideoCapture(DEV_ID)
n = 0

x_rate_dlt_old = 0
y_rate_dlt_old = 0
x_rate_dlt = 0
y_rate_dlt = 0
x_rate = 0
y_rate = 0

track_window = None
term_crit = (cv2.TermCriteria_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1)

def cyc_camera(): 
    global n
    global x_rate_dlt_old
    global y_rate_dlt_old
    global x_rate_dlt
    global y_rate_dlt
    global x_rate
    global y_rate
    global track_window
    
    if( cap.isOpened() ):
        start_time = time.time()

        # キャプチャの実施
        ret, frame = cap.read()
        if ret == True:
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([ 95, 130,  80])
            upper_blue = np.array([105, 255, 230])

            lower_red1 = np.array([170, 130,  20])
            upper_red1 = np.array([180, 255, 230])
            lower_red2 = np.array([0, 130, 20])
            upper_red2 = np.array([5, 255, 230])

            # Get the image dimensions
            height, width = frame.shape[:2]
            frame = cv2.copyMakeBorder(frame,10,10,10,10,cv2.BORDER_CONSTANT,value=0)

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

            kernel = np.ones((15, 15), np.uint8)
            eroded_image2_blue  = cv2.erode(dilated_image_blue, kernel, iterations=1)   # Apply erosion
            dilated_image2_blue = cv2.dilate(eroded_image2_blue, kernel, iterations=1)  # Apply dilation
            # eroded_image2_red   = cv2.erode(dilated_image_red, kernel, iterations=1)    # Apply erosion
            # dilated_image2_red  = cv2.dilate(eroded_image2_red, kernel, iterations=1)   # Apply dilation

            # kernel = np.ones((10, 10), np.uint8)
            # eroded_image2_blue  = cv2.erode(dilated_image2_blue, kernel, iterations=1)   # Apply erosion
            # dilated_image2_blue = cv2.dilate(eroded_image2_blue, kernel, iterations=1)  # Apply dilation
            # eroded_image2_red   = cv2.erode(dilated_image2_red, kernel, iterations=1)    # Apply erosion
            # dilated_image2_red  = cv2.dilate(eroded_image2_red, kernel, iterations=1)   # Apply dilation

            # kernel = np.ones((20, 20), np.uint8)
            # eroded_image2_blue  = cv2.erode(dilated_image2_blue, kernel, iterations=1)   # Apply erosion
            # dilated_image2_blue = cv2.dilate(eroded_image2_blue, kernel, iterations=1)  # Apply dilation
            # eroded_image2_red   = cv2.erode(dilated_image2_red, kernel, iterations=1)    # Apply erosion
            # dilated_image2_red  = cv2.dilate(eroded_image2_red, kernel, iterations=1)   # Apply dilation

            dilated_image2_blue = cv2.copyMakeBorder(dilated_image2_blue,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
            gray = cv2.cvtColor(dilated_image2_blue,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(dilated_image2_blue, contours, -1, (0,255,0), 2)
            for contour in contours:
                epsilon = 0.05 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                # if len(approx) == 4:
                #     width = abs(approx[0][0][0] - approx[3][0][0])
                #     if width > 20:
                #         line_width = abs(approx[0][0][0] - approx[1][0][0])
                #         if line_width < 10:
                #             cv2.drawContours(frame, [approx], -1, (255,0,0), 2)
                    
            # dilated_image2_red = cv2.copyMakeBorder(dilated_image2_red,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
            # gray2 = cv2.cvtColor(dilated_image2_red,cv2.COLOR_BGR2GRAY)
            # edges2 = cv2.Canny(gray2, 50, 150)
            # contours2, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(dilated_image2_red, contours, -1, (0,255,0), 2)
            dilated_image_red = cv2.copyMakeBorder(dilated_image_red,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
            gray = cv2.cvtColor(dilated_image_red,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            if track_window == None:
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                pet_bottle = False
                circularity_old = 1
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if int(area) < 800:
                        continue
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter == 0:
                        continue
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity < 0.85:
                        if circularity_old > circularity:
                            circularity_old = circularity
                            best_contour = contour
                            pet_bottle = True
                if  pet_bottle == True:
                    x, y, w, h = cv2.boundingRect(best_contour)
                    track_window = (x, y, w, h)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                ret, track_window = cv2.CamShift(edges, track_window, term_crit)

                pts = cv2.boxPoints(ret)
                pts = np.int0(pts)
                cv2.polylines(frame, [pts], True, (255, 0, 0), 2)

            # x_rate_dlt = 50
            # y_rate_dlt = 50
            # for contour in contours2:
            #     epsilon = 0.035 * cv2.arcLength(contour, True)
            #     approx = cv2.approxPolyDP(contour, epsilon, True)
            #     if len(approx) > 6:
            #         continue
            #     # print(approx)
            #     x = 0
            #     y = 0
            #     for i in range(len(approx)):
            #         x += approx[i][0][0]
            #         y += approx[i][0][1]
            #     x /= len(approx)
            #     y /= len(approx)
                
            #     cv2.drawContours(frame, [approx], -1, (0,0,255), 2)
                
            #     continue_flg = 0
            #     for i in range(len(approx)):
            #         if abs(x - approx[i][0][0]) < 12:
            #             continue_flg = 1
            #         # if abs(y - approx[i][0][1]) < 10:
            #         #     continue_flg = 1
            #     if 1 == continue_flg:
            #        continue

            #     x_rate_dlt_old = x_rate_dlt
            #     y_rate_dlt_old = y_rate_dlt
            #     x_rate_dlt = abs((x/width  * 100)-50)
            #     y_rate_dlt = abs((y/height * 100)-50)
            #     if x_rate_dlt < x_rate_dlt_old:
            #         x_rate = x/width  * 100
            #     if y_rate_dlt < y_rate_dlt_old:
            #         y_rate = y/height * 100
            if track_window != None:
                x_rate = (track_window[0] + track_window[2]/2)/width * 100
                y_rate = (track_window[1] + track_window[3]/2)/height * 100
                cv2.circle(frame, (int(x_rate/100*width), int(y_rate/100*height)), 3, (0,255,0), -1)
            
            cv2.imshow("camera", frame)
            # cv2.imshow("edge_bl", dilated_image2_blue)
            # cv2.imshow("edge_re", dilated_image2_red)
            # cv2.imshow("white_mask_bl", white_result_blue)
            # cv2.imshow("white_mask_re", white_result_red)
            
            if cv2.waitKey(1) & 0xff == ord('p'):
                cv2.imwrite("camera" + str(n) + ".jpg", frame)
                n += 1
            end_time = time.time()
            processing_time = end_time - start_time
            print(f"procssing time:{processing_time:.4f}seconds")

def set_cam_comm():
    return int(x_rate)

def end_camera():
    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return
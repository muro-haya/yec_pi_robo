import cv2
import numpy as np

import serial2SPIKE

# /dev/video0を指定
DEV_ID = 0

# /dev/video0を指定
cap = cv2.VideoCapture(DEV_ID)
term_crit = (cv2.TermCriteria_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1)

lower_blue = np.array([ 95, 130,  80])
upper_blue = np.array([105, 255, 230])
lower_red1 = np.array([170, 130, 130])
upper_red1 = np.array([180, 255, 230])
lower_red2 = np.array([  0, 130, 130])
upper_red2 = np.array([  5, 255, 230])

photo_num       = 0
processing_time = 0
x_rate          = 0
y_rate          = 0
roi_ini         = False
track_window = None

def detect_pet(frame, roi_frame, track_window_roi):
    height, width = roi_frame.shape[:2]
    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

    # Create a white image of the same size as the original image
    white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red  = mask_red1 | mask_red2

    white_result_red  = cv2.bitwise_and(white_image, white_image, mask=mask_red)

    # Define a kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)
    eroded_image_red   = cv2.erode(white_result_red, kernel, iterations=1)      # Apply erosion
    dilated_image_red  = cv2.dilate(eroded_image_red, kernel, iterations=1)     # Apply dilation

    # dilated_image_red = cv2.copyMakeBorder(dilated_image_red,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
    gray  = cv2.cvtColor(dilated_image_red,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    ret, track_window_roi = cv2.meanShift(edges, track_window_roi, term_crit)

    # cv2.imshow("ROI", edges)

    return track_window_roi

def cyc_camera():
    global lower_blue
    global upper_blue
    global lower_red1
    global upper_red1
    global lower_red2
    global upper_red2

    global photo_num
    global x_rate
    global y_rate
    global track_window
    global roi_ini
    global processing_time
    
    if( cap.isOpened() ):
        # start_time = time.time()

        pet_rec_ebl = serial2SPIKE.set_comm_cam()
        # キャプチャの実施
        ret, frame = cap.read()
        if ret == True:
            if pet_rec_ebl == True:
                height, width = frame.shape[:2]
                if track_window != None:
                    (xs, ys, w, h) = track_window

                    roi_xe = xs + w*3/2
                    roi_ye = ys + h*3/2
                    roi_xs = xs - w/2
                    roi_ys = ys - h/2
                    if roi_xs <= 0:
                        roi_xs = 0
                    if roi_ys <= 0:
                        roi_ys = 0
                    if roi_xe >= width:
                        roi_xe = width
                    if roi_ye >= height:
                        roi_ye = height

                    track_x = int(w*1/2)
                    track_y = int(h*1/2)
                    track_w = w
                    track_h = h

                    roi_frame = frame[int(roi_ys):int(roi_ye), int(roi_xs):int(roi_xe)]
                    track_window_roi = (track_x, track_y, track_w, track_h)
                    track_window_raw = detect_pet(frame, roi_frame, track_window_roi)
                    track_window = (track_window_raw[0]+xs-track_x, track_window_raw[1]+ys-track_y, track_window_raw[2], track_window_raw[3])

                else:
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    # Get the image dimensions
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
                    # dilated_image_blue = white_result_blue
                    # dilated_image_red = white_result_red

                    dilated_image_blue = cv2.copyMakeBorder(dilated_image_blue,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
                    gray  = cv2.cvtColor(dilated_image_blue,cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)
                    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # cv2.drawContours(dilated_image_blue, contours, -1, (0,255,0), 2)
                    for contour in contours:
                        epsilon = 0.05 * cv2.arcLength(contour, True)
                        approx = cv2.approxPolyDP(contour, epsilon, True)

                    dilated_image_red = cv2.copyMakeBorder(dilated_image_red,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
                    gray  = cv2.cvtColor(dilated_image_red,cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)

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

                if track_window != None:
                    x_rate = (track_window[0] + track_window[2]/2)/width * 100
                    y_rate = (track_window[1] + track_window[3]/2)/height * 100
                    cv2.circle(frame, (int(x_rate/100*width), int(y_rate/100*height)), 3, (0,255,0), -1)
                    cv2.rectangle(frame, (track_window[0], track_window[1]), (track_window[0]+track_window[2], track_window[1]+track_window[3]), (0, 0, 255), 2)
            else:
                x_rate          = 0
                y_rate          = 0
                processing_time = 0
                roi_ini         = False

            cv2.imshow("camera", frame)
            # cv2.imshow("edge_bl", dilated_image2_blue)
            # cv2.imshow("edge_re", dilated_image2_red)
            # cv2.imshow("white_mask_bl", white_result_blue)
            # cv2.imshow("white_mask_re", white_result_red)
            
            if cv2.waitKey(1) & 0xff == ord('p'):
                cv2.imwrite("camera" + str(photo_num) + ".jpg", frame)
                photo_num += 1

            # end_time = time.time()
            # processing_time += (end_time - start_time)
            # processing_time /= 2
            # print(f"procssing time:{processing_time:.4f}seconds")

def set_cam_comm():
    return int(x_rate)

def end_camera():
    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return
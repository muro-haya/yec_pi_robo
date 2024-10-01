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
lower_red1 = np.array([170, 130,  80])
upper_red1 = np.array([180, 255, 230])
lower_red2 = np.array([  0, 130,  80])
upper_red2 = np.array([  5, 255, 230])

photo_num       = 0
processing_time = 0
x_rate          = 0
y_rate          = 0
roi_ini         = False
track_window = None
pet_bottle   = 0

def trace_pet(frame, roi_frame, track_window_roi):
    height, width = roi_frame.shape[:2]
    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

    # Create a white image of the same size as the original image
    white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

    if 1 == pet_bottle:
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_img  = mask_red1 | mask_red2
    else:
        mask_img  = cv2.inRange(hsv, lower_blue, upper_blue)

    white_result  = cv2.bitwise_and(white_image, white_image, mask=mask_img)

    # Define a kernel for morphological operations
    kernel = np.ones((10, 10), np.uint8)
    eroded_image   = cv2.erode(white_result, kernel, iterations=1)      # Apply erosion
    dilated_image  = cv2.dilate(eroded_image, kernel, iterations=1)     # Apply dilation

    white_area = np.sum(dilated_image == 255)
    white_rate = white_area/dilated_image.size
    if white_rate < 0.1:
        return None

    # dilated_image_red = cv2.copyMakeBorder(dilated_image_red,10,10,10,10,cv2.BORDER_CONSTANT,value=0)
    gray  = cv2.cvtColor(dilated_image,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bestw = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if bestw < w:
            bestw = w
            track_window_roi = (x, y, w, h)

    # ret, track_window_roi = cv2.meanShift(edges, track_window_roi, term_crit)
    # print(x, y, w, h)
    # print(track_window_roi)

    # cv2.imshow("ROI", edges)

    return track_window_roi

def mask_pet(white_image,kernel,mask_img,frame):
    mask_result        = cv2.bitwise_and(white_image, white_image, mask=mask_img)
    # mask_result_color  = cv2.bitwise_and(frame, frame, mask=mask_img)

    # gray  = cv2.cvtColor(mask_result_color,cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 10, 80)

    # edges_not = cv2.bitwise_not(edges)
    # edge_result_red  = cv2.bitwise_and(mask_result, mask_result, mask=edges_not)
                
    # erode_result_red  = cv2.erode(edge_result_red, kernel, iterations=1)     # Apply erosion

    # edges_contours = cv2.Canny(erode_result_red, 10, 80)
    # contours, _ = cv2.findContours(edges_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask_result  = cv2.erode(mask_result, kernel, iterations=1)     # Apply erosion
    edges_contours = cv2.Canny(mask_result, 10, 80)
    contours, _ = cv2.findContours(edges_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    # return   contours,erode_result_red
    return   contours,mask_result

def detect_pet(dec_contours, binary_img):
    white_rate_old   = 0
    dec_area         = 0
    dec_best_contour = None
    dec_pet_bottle   = False

    _,width,_ = binary_img.shape

    for dec_contour in dec_contours:
        dec_area = int(cv2.contourArea(dec_contour))
        if dec_area < 500:
            continue
        x, y, w, h = cv2.boundingRect(dec_contour)
        roi = binary_img[y:y+h, x:x+w]
        white_area = np.sum(roi == 255)
        white_rate = white_area/roi.size
        x_rate_raw = (x+w/2)/width
        if white_rate < 0.4:
            continue
        if x_rate_raw < 0.2 or x_rate_raw > 0.8:
            continue
        if white_rate_old < white_rate:
            cv2.imshow("roi",roi)
            white_rate_old   = white_rate
            dec_best_contour = dec_contour
            dec_pet_bottle   = True

    return dec_area,dec_best_contour,dec_pet_bottle

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
    global pet_bottle
    
    if( cap.isOpened() ):
        # start_time = time.time()

        pet_rec_ebl = serial2SPIKE.set_comm_cam()
        # pet_rec_ebl = True
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
                    track_window_raw = trace_pet(frame, roi_frame, track_window_roi)
                    if track_window_raw == None:
                        track_window = None
                    else:
                        track_window = (track_window_raw[0]+xs-track_x, track_window_raw[1]+ys-track_y, track_window_raw[2], track_window_raw[3])

                else:
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    # Get the image dimensions
                    # frame = cv2.copyMakeBorder(frame,10,10,10,10,cv2.BORDER_CONSTANT,value=0)

                    # Create a white image of the same size as the original image
                    white_image = np.ones((height, width, 3), dtype=np.uint8) * 255
                    kernel = np.ones((10, 10), np.uint8)

                    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
                    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                    mask_red = mask_red1 | mask_red2

                    blue_contours,bluebinary = mask_pet(white_image,kernel,mask_blue,frame)
                    blue_area,blue_best_contour,blue_bottle = detect_pet(blue_contours,bluebinary)

                    # cv2.imshow("bl_mask",bluebinary)

                    red_contours,red_binary = mask_pet(white_image,kernel,mask_red,frame)
                    red_area,red_best_contour,red_bottle = detect_pet(red_contours,red_binary)

                    # cv2.imshow("rd_mask",red_binary)

                    pet_bottle = 0
                    if  red_bottle == True and blue_bottle == False:
                        x, y, w, h = cv2.boundingRect(red_best_contour)
                        pet_bottle = 1
                    elif  red_bottle == False and blue_bottle == True:
                        x, y, w, h = cv2.boundingRect(blue_best_contour)
                        pet_bottle = 2
                    elif red_bottle == True and blue_bottle == True:
                        if blue_area < red_area:
                            x, y, w, h = cv2.boundingRect(red_best_contour)
                            pet_bottle = 1
                        else:
                            x, y, w, h = cv2.boundingRect(blue_best_contour)
                            pet_bottle = 2
                    if 0 != pet_bottle:
                        track_window = (x, y, w, h)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    else:
                        x_rate = 50

                if track_window != None:
                    x_rate = (track_window[0] + track_window[2]/2)/width * 100
                    y_rate = (track_window[1] + track_window[3]/2)/height * 100
                    cv2.circle(frame, (int(x_rate/100*width), int(y_rate/100*height)), 3, (0,255,0), -1)
                    cv2.rectangle(frame, (track_window[0], track_window[1]), (track_window[0]+track_window[2], track_window[1]+track_window[3]), (0, 0, 255), 2)
            else:
                x_rate          = 50
                y_rate          = 50
                processing_time = 0
                roi_ini         = False
                    
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_color = (0, 255, 0)  # Green color
            font_thickness = 1
            # cv2.putText(frame, str(pet_rec_ebl), (10, 30), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
            cv2.imshow("camera", frame)
            # cv2.imshow("edge_bl", dilated_image2_blue)
            # cv2.imshow("edge_re", dilated_image2_red)
            # cv2.imshow("white_mask_bl", white_result_blue)
            # cv2.imshow("white_mask_re", white_result_red)
            # cv2.imshow("EDGE", edges)
            
                    
            if cv2.waitKey(1) & 0xff == ord('p'):
                cv2.imwrite("camera" + str(photo_num) + ".jpg", frame)
                photo_num += 1

            # end_time = time.time()
            # processing_time += (end_time - start_time)
            # processing_time /= 2
            # print(f"procssing time:{processing_time:.4f}seconds")

def set_cam_comm():
    return int(x_rate),pet_bottle

def end_camera():
    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return
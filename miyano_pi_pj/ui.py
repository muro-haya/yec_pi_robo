import cv2
import numpy as np
from datetime import datetime
import keyboard

import serial2SPIKE

# Initialize parameters
y_axis_val = 0
key_log = "_"

# List to store input values
input_val = []
joined_val = []
joined_val_index = 0
joined_val_index_max = 10

# List to store recieve values
recieve_val = [] 
recieve_val_index = 0
recieve_val_index_max = 10

# Define font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
font_color = (0, 255, 0)  # Green color
font_thickness = 1

# Create windows
cv2.namedWindow('Values Window')

button_states = {"download": False, "sent data2": False, "sent data3": False}  # Button states dictionary
# Button properties
buttons = [
    {"text": "download", "x": 20, "y":  350, "w": 120, "h":  20, "default_color": (255,   0,   0), "pressed_color": (  0,  0, 255)},
    # {"text": "sent data2", "x": 200, "y":  75, "w": 120, "h":  20, "default_color": (255,   0,   0), "pressed_color": (  0, 255,   0)},
    # {"text": "sent data3", "x": 200, "y": 105, "w": 120, "h":  20, "default_color": (255,   0,   0), "pressed_color": (  0, 255,   0)},
]

def set_ui_log():
    return recieve_val,joined_val

def set_ketboardnum(num):
    global key_log
    if str(num) != key_log:
        if 5 > len(input_val[joined_val_index]):
            input_val[joined_val_index].append(str(num))  # Append the digit to input_val
            joined_val[joined_val_index] = ''.join(input_val[joined_val_index])
    key_log = str(num)

def mouse_callback(event, x, y, flags, param):
    global button_states
    if event == cv2.EVENT_LBUTTONDOWN:
        for button in buttons:
            if button["x"] <= x <= button["x"] + button["w"] and button["y"] <= y <= button["y"] + button["h"]:
                button_states[button["text"]] = True
                print(f"{button['text']} pressed: {button_states[button['text']]}")
    elif event == cv2.EVENT_LBUTTONUP:
        for button in buttons:
            if button["x"] <= x <= button["x"] + button["w"] and button["y"] <= y <= button["y"] + button["h"]:
                button_states[button["text"]] = False
                print(f"{button['text']} pressed: {button_states[button['text']]}")     

# Set the mouse callback function for the 'Values Window'
cv2.setMouseCallback('Values Window', mouse_callback)

def ini_ui():# List to store input values
    global joined_val
    global input_val
    global recieve_val

    for i in range(joined_val_index_max):
        joined_val.append(0)
        input_val.append([])
    for i in range(recieve_val_index_max):
        recieve_val.append(0)

def cyc_ui():
    global joined_val_index
    global recieve_val_index
    global joined_val
    global input_val
    global recieve_val
    global key_log

    recieve_val, _ = serial2SPIKE.set_comm_ui() 

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    y_axis_val = 0

    # Create a black image for the values window
    value_window = np.zeros((400, 430, 3), dtype=np.uint8)

    # Prepare text to display current values
    text_time = f"Time: {current_time}"
    # Put text on the frame
    y_axis_val += 30
    cv2.putText(value_window, text_time, (10, y_axis_val), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    for i in range(joined_val_index_max):
        y_axis_val += 30
        if joined_val_index == i:
            text_input = f"@Input Val{i}: {joined_val[i]}"
        else:
            text_input = f" Input Val{i}: {joined_val[i]}"
        cv2.putText(value_window, text_input, (10, y_axis_val), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    y_axis_val = 30

    for i in range(recieve_val_index_max):
        y_axis_val += 30
        # print(recieve_val[i])
        text_receive = f" receive Val{i}: {recieve_val[i]}"
        cv2.putText(value_window, text_receive, (200, y_axis_val), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    # Draw buttons
    for button in buttons:
        button_color = button["pressed_color"] if button_states[button["text"]] else button["default_color"]
        # Draw button rectangle
        cv2.rectangle(value_window, (button["x"], button["y"]), (button["x"] + button["w"], button["y"] + button["h"]), button_color, -1)
        # Draw button text
        cv2.putText(value_window, button["text"], (button["x"] + 10, button["y"] + 17), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Display the values window
    cv2.imshow('Values Window', value_window)
    
    if keyboard.is_pressed('e'):
        if 'e' != key_log:
            cmd_num = int(10*10+joined_val_index)
            serial2SPIKE.send_data(cmd_num, int(joined_val[joined_val_index]))
            # input_val[joined_val_index].clear()
            # joined_val[joined_val_index] = 0
        key_log = 'e'
    elif keyboard.is_pressed('d'):
        if 'd' != key_log:
            input_val[joined_val_index].clear()
            joined_val[joined_val_index] = 0
        key_log = 'd'
    elif keyboard.is_pressed('up'):
        if 'u' != key_log:
            if joined_val_index > 0:
                joined_val_index -= 1
        key_log = 'u'
    elif keyboard.is_pressed('down'):
        if 'w' != key_log:
            if joined_val_index < joined_val_index_max-1:
                joined_val_index += 1
        key_log = 'w'
    elif keyboard.is_pressed('0'):
        set_ketboardnum(0)
    elif keyboard.is_pressed('1'):
        set_ketboardnum(1)
    elif keyboard.is_pressed('2'):
        set_ketboardnum(2)
    elif keyboard.is_pressed('3'):
        set_ketboardnum(3)
    elif keyboard.is_pressed('4'):
        set_ketboardnum(4)
    elif keyboard.is_pressed('5'):
        set_ketboardnum(5)
    elif keyboard.is_pressed('6'):
        set_ketboardnum(6)
    elif keyboard.is_pressed('7'):
        set_ketboardnum(7)
    elif keyboard.is_pressed('8'):
        set_ketboardnum(8)
    elif keyboard.is_pressed('9'):
        set_ketboardnum(9)
    else:
        key_log = '_'

def end_ui():
    # Release the capture and close windows
    cv2.destroyAllWindows()

import cv2
import numpy as np
from datetime import datetime

# Initialize parameters
y_axis_val = 0

# List to store input values
input_val = []
joined_val = []
joined_val_index = 0
joined_val_index_max = 4
for i in range(joined_val_index_max):
    joined_val.append(0)
    input_val.append([])

# List to store recieve values
recieve_val = [] 
recieve_val_index = 0
recieve_val_index = 6
for i in range(recieve_val_index):
    recieve_val.append(0)

# Define font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
font_color = (0, 255, 0)  # Green color
font_thickness = 1

button_states = {"sent data1": False, "sent data2": False, "sent data3": False}  # Button states dictionary
# Button properties
buttons = [
    {"text": "sent data1", "x": 200, "y":  45, "w": 120, "h":  20, "default_color": (255,   0,   0), "pressed_color": (  0, 255,   0)},
    {"text": "sent data2", "x": 200, "y":  75, "w": 120, "h":  20, "default_color": (255,   0,   0), "pressed_color": (  0, 255,   0)},
    {"text": "sent data3", "x": 200, "y": 105, "w": 120, "h":  20, "default_color": (255,   0,   0), "pressed_color": (  0, 255,   0)},
]

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

# Create windows
cv2.namedWindow('Values Window')

# Set the mouse callback function for the 'Values Window'
# cv2.setMouseCallback('Values Window', mouse_callback)

while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    y_axis_val = 0

    # Create a black image for the values window
    value_window = np.zeros((600, 800, 3), dtype=np.uint8)

    # Prepare text to display current values
    text_time = f"Time: {current_time}"
    # Put text on the frame
    y_axis_val += 30
    cv2.putText(value_window, text_time, (10, y_axis_val), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    for i in range(joined_val_index_max):
        y_axis_val += 30
        if joined_val_index == i:
            text_input = f"@Input Val: {joined_val[i]}"
        else:
            text_input = f" Input Val: {joined_val[i]}"
        cv2.putText(value_window, text_input, (10, y_axis_val), font, font_scale, font_color, font_thickness, cv2.LINE_AA)


    for i in range(recieve_val_index):
        y_axis_val += 30
        text_receive = f" receive Val: {recieve_val[i]}"
        cv2.putText(value_window, text_receive, (10, y_axis_val), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    # # Draw buttons
    # for button in buttons:
    #     button_color = button["pressed_color"] if button_states[button["text"]] else button["default_color"]
    #     # Draw button rectangle
    #     cv2.rectangle(value_window, (button["x"], button["y"]), (button["x"] + button["w"], button["y"] + button["h"]), button_color, -1)
    #     # Draw button text
    #     cv2.putText(value_window, button["text"], (button["x"] + 10, button["y"] + 17), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Display the values window
    cv2.imshow('Values Window', value_window)

    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key != 0xFF:  # Check if a key is pressed
        if key == 13:  # Enter key (ASCII 13)
            input_val[joined_val_index].clear()
            joined_val[joined_val_index] = 0
        elif key == 82:
            if joined_val_index > 0:
                joined_val_index -= 1
        elif key == 84:
            if joined_val_index < joined_val_index_max-1:
                joined_val_index += 1
        elif chr(key).isdigit():  # Check if the key is a digit
            if 5 > len(input_val[joined_val_index]):
                input_val[joined_val_index].append(chr(key))  # Append the digit to input_val
                joined_val[joined_val_index] = ''.join(input_val[joined_val_index])

    # Exit the loop when 'q' is pressed
    if key == ord('q'):
        break

# Release the capture and close windows
cv2.destroyAllWindows()

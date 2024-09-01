import cv2
import numpy as np
from datetime import datetime

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize parameters
brightness = 0
contrast = 1.0
input_val = []  # List to store input values
joined_str = 0
button_states = {"Button 1": False, "Button 2": False, "Button 3": False}  # Button states dictionary

# Define font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
font_color = (0, 255, 0)  # Green color
font_thickness = 1

# Button properties
buttons = [
    {"text": "Button 1", "x": 50, "y": 120, "w": 100, "h": 40, "color": (255, 0, 0)},  # Red
    {"text": "Button 2", "x": 160, "y": 120, "w": 100, "h": 40, "color": (0, 255, 0)},  # Green
    {"text": "Button 3", "x": 270, "y": 120, "w": 100, "h": 40, "color": (0, 0, 255)},  # Blue
]

# Button properties
buttons = [
    {"text": "Button 1", "x":  50, "y": 120, "w": 100, "h":  40, "default_color": (255,   0,   0), "pressed_color": (  0,   0, 255)},  # Red, Yellow, Blue
    {"text": "Button 2", "x": 160, "y": 120, "w": 100, "h":  40, "default_color": (  0, 255,   0), "pressed_color": (  0, 255, 255)},  # Green, Yellow, Cyan
    {"text": "Button 3", "x": 270, "y": 120, "w": 100, "h":  40, "default_color": (  0,   0, 255), "pressed_color": (255,   0,   0)},  # Blue, Magenta, Red
]

# Button properties
button_x, button_y, button_w, button_h = 50, 120, 100, 40  # Button position and size
button_text = "Press Me"

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
cv2.namedWindow('Video Stream')
cv2.namedWindow('Values Window')

# Set the mouse callback function for the 'Values Window'
cv2.setMouseCallback('Values Window', mouse_callback)

while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Apply brightness and contrast adjustments
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

    # Create a black image for the values window
    value_window = np.zeros((600, 800, 3), dtype=np.uint8)

    # Prepare text to display current values
    text_time = f"Time: {current_time}"
    text_contrast = f"Contrast: {contrast:.1f}"
    text_input = f"Last Key: {joined_str}"
    
    # Put text on the frame
    cv2.putText(value_window, text_time, (10, 30), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(value_window, text_contrast, (10, 60), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(value_window, text_input, (10, 90), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    # Draw buttons
    for button in buttons:
        button_color = button["pressed_color"] if button_states[button["text"]] else button["default_color"]
        # Draw button rectangle
        cv2.rectangle(value_window, (button["x"], button["y"]), (button["x"] + button["w"], button["y"] + button["h"]), button_color, -1)
        # Draw button text
        cv2.putText(value_window, button["text"], (button["x"] + 10, button["y"] + 25), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
 
    # Display the resulting frame
    cv2.imshow('Video Stream', adjusted_frame)

    # Display the values window
    cv2.imshow('Values Window', value_window)

    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key != 0xFF:  # Check if a key is pressed
        if key == 13:  # Enter key (ASCII 13)
            # Define action for Enter key if needed
            pass
        elif chr(key).isdigit():  # Check if the key is a digit
            if 5 > len(input_val):
                input_val.append(chr(key))  # Append the digit to input_val
                joined_str = ''.join(input_val)

    # Exit the loop when 'q' is pressed
    if key == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np

# Initialize variables for the selection
start_point = None
end_point = None
rect_drawn = False

img_path = '/home/robo2/jpg/camera6.jpg'

def mouse_callback(event, x, y, flags, param):
    global start_point, end_point, rect_drawn

    if None == end_point:
        if event == cv2.EVENT_LBUTTONDOWN:
            start_point = (x, y)
            rect_drawn = False
    
        elif event == cv2.EVENT_MOUSEMOVE:
            if start_point is not None:
                end_point = (x, y)
    
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        rect_drawn = True

# Load the image
image = cv2.imread(img_path)  # Replace 'your_image.jpg' with your image file

# Convert the image from BGR to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a window and set the mouse callback function
cv2.imshow('Image', image)
cv2.setMouseCallback('Image', mouse_callback)

print("Click and drag to select a region. Press 'q' to finish.")

while True:
    if start_point and end_point:
        temp_image = image.copy()
        cv2.rectangle(temp_image, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow('Image', temp_image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') and rect_drawn:
        break

cv2.destroyAllWindows()

# Compute the HSV range in the selected region
x1, y1 = start_point
x2, y2 = end_point
x1, x2 = min(x1, x2), max(x1, x2)
y1, y2 = min(y1, y2), max(y1, y2)

# Extract the region of interest (ROI) from the HSV image
roi_hsv = hsv_image[y1:y2, x1:x2]

# Compute the min and max HSV values
min_hsv = np.min(roi_hsv, axis=(0, 1))
max_hsv = np.max(roi_hsv, axis=(0, 1))

print(f"Selected region:")
print(f"Minimum HSV value: {min_hsv}")
print(f"Maximum HSV value: {max_hsv}")

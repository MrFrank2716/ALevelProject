import cv2
import time
from translate import *
from concurrent_videocapture import ConcurrentVideoCapture

cam_port = 1
cap = ConcurrentVideoCapture(cam_port)

# Initial contrast value
alpha = 1.0

# Function to adjust contrast
def adjust_contrast(val):
    global alpha
    alpha = val / 100

# Creating the window
cv2.namedWindow('Chessboard')

# Create a trackbar/slider on the screen
cv2.createTrackbar('Contrast', 'Chessboard', 100, 300, adjust_contrast)

while True:
    init = time.time()
    grabbed, frame = cap.read()

    # Original Resolution Frame before resize
    original_frame = frame

    # Adjust contrast
    frame = cv2.convertScaleAbs(frame, alpha=alpha)

    # Resize the image
    screen_res = 1280, 720  # Screen resolution
    scale_width = screen_res[0] / frame.shape[1]
    scale_height = screen_res[1] / frame.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(frame.shape[1] * scale)
    window_height = int(frame.shape[0] * scale)
    frame = cv2.resize(frame, (window_width, window_height))

    cv2.imshow('Chessboard', frame)

    key = cv2.waitKey(1)
    if key == ord('a'):  # 'a' key
        translate(original_frame,"transformed")
    elif key == 27:  # ESC
        break
    fps = 75
cap.release()

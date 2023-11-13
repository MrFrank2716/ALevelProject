import cv2
import time
from concurrent_videocapture import ConcurrentVideoCapture

cam_port = 1
cap = ConcurrentVideoCapture(cam_port)

while True:
    init = time.time()
    grabbed, frame = cap.read()
    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Chessboard', grayFrame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    fps = 75
cap.release()
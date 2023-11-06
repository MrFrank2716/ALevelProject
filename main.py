import cv2
import time
from concurrent_videocapture import ConcurrentVideoCapture

cam_port = 1
cap = ConcurrentVideoCapture(cam_port)

while True:
    init = time.time()
    grabbed, frame = cap.read()
    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsvFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hslFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    cv2.imshow("Colour Video Capture", frame)
    cv2.imshow("BW Video Capture", grayFrame)
    cv2.imshow("HSV Video Capture", hsvFrame)
    cv2.imshow("YCrCb Video Capture", hslFrame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    fps = 75
cap.release()
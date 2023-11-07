import cv2
import time
from concurrent_videocapture import ConcurrentVideoCapture

cam_port = 1
cap = ConcurrentVideoCapture(cam_port)

while True:
    init = time.time()
    grabbed, frame = cap.read()
    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(grayFrame, (7, 7), None)

    # terminating criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    if ret == True:
        corners2 = cv2.cornerSubPix(grayFrame, corners, (11, 11), (-1, -1), criteria)

        # Draw and display the corners
    img = cv2.drawChessboardCorners(grayFrame, (7, 7), corners, ret)
    cv2.imshow('Chessboard', img)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    fps = 75
cap.release()
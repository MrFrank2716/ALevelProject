import cv2 as cv
from concurrent_videocapture import ConcurrentVideoCapture
capture = ConcurrentVideoCapture(src=0)


while True:
    if not capture.read():
        print("Unable to Grab Frames from camera")
        break

    okay1, depth_map = capture.read(0, cv.CV_CAP_OPENNI_DEPTH_MAP)
    if not okay1:
        print("Unable to Retrieve Disparity Map from camera")
        break

    okay2, gray_image = capture.read(0, cv.CV_CAP_OPENNI_GRAY_IMAGE)
    if not okay2:
        print("Unable to retrieve Gray Image from device")
        break

    cv.imshow("depth camera", depth_map)
    cv.imshow("rgb camera", gray_image)

    if cv.waitKey(10) == 27:
        break

cv.destroyAllWindows()
capture.release()

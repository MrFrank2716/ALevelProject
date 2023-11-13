import cv2
from concurrent_videocapture import ConcurrentVideoCapture
import numpy as np

cam_port = 1
cam = ConcurrentVideoCapture(cam_port)
result, image = cam.read()
if result == True:
    gray = cv2.convertScaleAbs(image,1)
    result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("Image.png", result)
image = cv2.imread("Image.png")
def translate(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("Image.png", result)
    image = cv2.imread("Image.png")
# Finds the inside corners for a 8x8 board
ret, corners = cv2.findChessboardCorners(image, (7, 7), None)

# Inner Corners of the 8x8 search
topLeft = corners[42][0]
topRight = corners[0][0]
btmLeft = corners[48][0]
btmRight = corners[6][0]

painted_image = cv2.circle(image, (int(topLeft[0]),int(topLeft[1])), radius=10, color=(0, 255, 0), thickness=-1)
painted_image = cv2.circle(image, (int(topRight[0]),int(topRight[1])), radius=10, color=(0, 255, 0), thickness=-1)
painted_image = cv2.circle(image, (int(btmLeft[0]),int(btmLeft[1])), radius=10, color=(0, 255, 0), thickness=-1)
painted_image = cv2.circle(image, (int(btmRight[0]),int(btmRight[1])), radius=10, color=(0, 255, 0), thickness=-1)
cv2.putText(image,"TopRight", (int(topRight[0]),int(topRight[1])), cv2.FONT_HERSHEY_TRIPLEX, 2, 255)
cv2.putText(image,"TopLeft", (int(topLeft[0]),int(topLeft[1])), cv2.FONT_HERSHEY_TRIPLEX, 2, 255)


# Finds the outer corners of the chessboard
xy_diff = corners[8][0] - corners[0][0] #Find the side lengths of a square

topLeft[0] += xy_diff[0]
topLeft[1] -= xy_diff[1]
topRight[0] -= xy_diff[0]
topRight[1] += xy_diff[1]
btmLeft[0] += xy_diff[0]
btmLeft[1] -= xy_diff[1]
btmRight[0] -= xy_diff[0]
btmRight[1] += xy_diff[1]

cornerPoints = np.array([topLeft, topRight, btmRight, btmLeft], dtype='float32')

painted_image = cv2.circle(image, (int(topLeft[0]),int(topLeft[1])), radius=10, color=(0, 0, 255), thickness=-1)
painted_image = cv2.circle(image, (int(topRight[0]),int(topRight[1])), radius=10, color=(0, 0, 255), thickness=-1)
painted_image = cv2.circle(image, (int(btmLeft[0]),int(btmLeft[1])), radius=10, color=(0, 0, 255), thickness=-1)
painted_image = cv2.circle(image, (int(btmRight[0]),int(btmRight[1])), radius=10, color=(0, 0, 255), thickness=-1)
cv2.imwrite("PaintedImage.png", painted_image)
# Set the base and height of the output resolution of transformed image - 1000x1000px
base = 1000
height = 1000

# Define new corner points from base and height of the rectangle
new_cornerPoints = np.array([[0, 0], [base, 0], [base, height], [0, height]], dtype='float32')


# Calculate matrix to transform the perspective of the image
M = cv2.getPerspectiveTransform(cornerPoints, new_cornerPoints)

new_image = cv2.warpPerspective(image, M, (base, height))

cv2.imwrite('transformed.png', new_image)
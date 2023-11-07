import cv2
from concurrent_videocapture import ConcurrentVideoCapture
import numpy as np

cam_port = 1
cam = ConcurrentVideoCapture(cam_port)
result, image = cam.read()
cv2.imwrite("Image.png", image)
image = cv2.imread("Image.png")

ret, corners = cv2.findChessboardCorners(image, (7, 7), None)
#Paint some points in blue
points = np.array([corners[48][0], corners[42][0], corners[6][0], corners[0][0]])
for i in range(len(points)):
    cv2.circle(image, tuple(points[i].astype('int64')), radius=0, color=(255, 0, 0), thickness=10)
cv2.imwrite('Image_withPoints.png', image)

#Put pixels of the chess corners: top left, top right, bottom right, bottom left.
cornerPoints = np.array([corners[42][0], corners[0][0], corners[6][0], corners[48][0]], dtype='float32')

#Find base of the rectangle given by the chess corners
base = np.linalg.norm(cornerPoints[1] - cornerPoints[0] )

#Height has 8 squares while base has 8 squares.
height = base/8*8

#Define new corner points from base and height of the rectangle
new_cornerPoints = np.array([[0, 0], [int(base), 0], [int(base), int(height)], [0, int(height)]], dtype='float32')

#Calculate matrix to transform the perspective of the image
M = cv2.getPerspectiveTransform(cornerPoints, new_cornerPoints)

new_image = cv2.warpPerspective(image, M, (int(base), int(height)))

#Function to get data points in the new perspective from points in the image
def calculate_newPoints(points, M):
    new_points = np.einsum('kl, ...l->...k', M,  np.concatenate([points, np.broadcast_to(1, (*points.shape[:-1], 1)) ], axis = -1) )
    return new_points[...,:2] / new_points[...,2][...,None]

new_points = calculate_newPoints(points, M)

#Paint new data points in red
for i in range(len(new_points)):
    cv2.circle(new_image, tuple(new_points[i].astype('int64')), radius=0, color=(0, 0, 255), thickness=5)

cv2.imwrite('transformed.png', new_image)
import cv2
import numpy as np

def getChessboardCorners(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use the Canny edge detection method to find edges
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area in descending order and keep the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    # Get the outer corners of the largest contour
    corners = cv2.approxPolyDP(contours[0], 0.01 * cv2.arcLength(contours[0], True), True)

    # Puts the corner points into a numpy array for efficient processing
    cornerPoints = np.array(corners, dtype='float32')
    return cornerPoints

def removeBorder(fileName):
    # Load your image
    img = cv2.imread(f'{fileName}.png')

    # Crop the borders of the 1000x1000px image to 900x900px
    img = img[50:950, 50:950]

    # Save the result
    cv2.imwrite(f'{fileName}.png', img)
def perspectiveTransform(image,corners,fileName):

    # Set the base and height of the output resolution of transformed image - 1000x1000px
    base = 1000
    height = 1000

    cornerPoints = corners
    # Define new corner points from base and height of the rectangle
    new_cornerPoints = np.array([[0, 0], [base, 0], [base, height], [0, height]], dtype='float32')

    # Calculate matrix to transform the perspective of the image
    Matrix = cv2.getPerspectiveTransform(cornerPoints, new_cornerPoints)

    new_image = cv2.warpPerspective(image, Matrix, (base, height))

    cv2.imwrite(f'{fileName}.png', new_image)

def translate(image,fileName):
    perspectiveTransform(image,getChessboardCorners(image),fileName)
    removeBorder(fileName)

from settings import *
import cv2
from PIL import Image
import numpy as np
def old_detect_chess_piece(image_path, square_colour):  # The square's colour passed through is a black or white value 0 or 255 a value.
    img = Image.open(image_path).convert('L')  # Converts the image to grayscale so it's easier to compare colours.
    # Define a function for thresholding, 255 for white and returns 0 for black
    fn = lambda x: 255 if x > settings.return_value("detect_chess_piece_threshold") else 0
    img = img.point(fn, mode='1') # Applies the thresholding basically binarizes the image.
    img.save("bw.png")
    width, height = img.size
    # Define points for the 4x4 grid locations to grab the colours.
    points = [(x, y) for x in range(width // 2 - 2, width // 2 + 2) for y in range(height // 2 - 2, height // 2 + 2)]

    # Get the colours of the points using the PIL package built into python.
    colours = [img.getpixel(point) for point in points]

    # Check if the middle points are a different color than the square which is passed through as a parameter.
    return any(abs(colour - square_colour) > settings.return_value("detect_chess_piece_threshold") for colour in
               colours)  # Threshold for the colour comparison - this seems to work great for a green board.


#print(old_detect_chess_piece("squares/C_2.png", 0))

class Detector:
    def __init__(self):
        self.image_path = "squares/C_1"
        # Load an images of empty square for comparison
        self.empty_light_square_image = cv2.imread('squares/D_4.png')
        self.empty_light_square_mean_colour = cv2.mean(self.empty_light_square_image)
        self.empty_dark_square_image = cv2.imread('squares/D_5.png')
        self.empty_dark_square_mean_colour = cv2.mean(self.empty_dark_square_image)
        self.chessboard_colour_array = [
            [1 ,0 ,1 ,0 ,1 ,0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1]
        ]
        self.occupied_square_array = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    def is_square_occupied_edges(self, image_path):
        image = cv2.imread(image_path)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use Canny edge detection to find edges in the image
        edges = cv2.Canny(blurred, 30, 150)
        cv2.imwrite("grayscale.png",edges)
        # Count the number of white pixels in the edge-detected image
        num_edges = np.sum(edges > 0)

        # If the number of edges exceeds a certain threshold, assume a piece is present
        if num_edges > 227:  # Needs to be adjusted in different lighting environments - currently works
            return True
        else:
            return False
    def is_square_occupied_colour_light(self, image_path):
        image = cv2.imread(image_path)
        # Calculate the mean color of the input image
        image_mean_colour = cv2.mean(image)

        # Calculate the difference between the mean colors
        colour_difference = np.abs(np.subtract(image_mean_colour, self.empty_light_square_mean_colour))

        # If the color difference exceeds a certain threshold, assume a piece is present
        if np.sum(colour_difference) > 10:  # It works under normal lighting might need to change if different
            return True
        else:
            return False

    def is_square_occupied_colour_dark(self, image_path):
        image = cv2.imread(image_path)
        # Calculate the mean color of the input image
        image_mean_colour = cv2.mean(image)

        # Calculate the difference between the mean colors
        colour_difference = np.abs(np.subtract(image_mean_colour, self.empty_dark_square_mean_colour))

        # If the color difference exceeds a certain threshold, assume a piece is present
        if np.sum(colour_difference) > 10:  # It works under normal lighting might need to change if different
            return True
        else:
            return False

    def is_square_occupied_contours(self, image_path, min_contour_area=5000):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresholded = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite("bw.png",thresholded)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imwrite("grayscale.png", _)
        for contour in contours:
            if cv2.contourArea(contour) > min_contour_area:
                return True

        return False

detector = Detector()

print(detector.is_square_occupied_contours("squares/E_4.png"))

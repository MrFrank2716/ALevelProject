import random
from sklearn.cluster import KMeans
from collections import Counter
from settings import *
import cv2
from PIL import Image
import numpy as np
import os
import chess
from gamestate import *

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
        self.move_number = 1
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
        self.previous_occupied_square_array = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    def is_square_occupied_edges_black(self, image_path):
        image = cv2.imread(image_path)
        # Define the amount to crop on each side
        crop_amount = 10  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use Canny edge detection to find edges in the image
        edges = cv2.Canny(blurred, 60, 60)

        # Count the number of white pixels in the edge-detected image
        num_edges = np.sum(edges > 0)

        # If the number of edges exceeds a certain threshold, assume a piece is present
        if num_edges > 227:  # Needs to be adjusted in different lighting environments - currently works
            return True
        else:
            return False

    def is_square_occupied_edges_white(self, image_path):
        image = cv2.imread(image_path)
        # Define the amount to crop on each side
        crop_amount = 10  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use Canny edge detection to find edges in the image
        edges = cv2.Canny(blurred, 50, 50)

        # Count the number of white pixels in the edge-detected image
        num_edges = np.sum(edges > 0)

        # If the number of edges exceeds a certain threshold, assume a piece is present
        if num_edges > 227:  # Needs to be adjusted in different lighting environments - currently works
            return True
        else:
            return False

    def is_square_occupied_colour_light(self, image_path):
        image = cv2.imread(image_path)

        # Define the amount to crop on each side
        crop_amount = 10  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)
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
        # Define the amount to crop on each side
        crop_amount = 10  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)

        # Calculate the mean color of the input image
        image_mean_colour = cv2.mean(image)

        # Calculate the difference between the mean colors
        colour_difference = np.abs(np.subtract(image_mean_colour, self.empty_dark_square_mean_colour))

        # If the color difference exceeds a certain threshold, assume a piece is present
        if np.sum(colour_difference) > 10:  # It works under normal lighting might need to change if different
            return True
        else:
            return False

    def is_square_occupied_contours_black(self, image_path):
        image = cv2.imread(image_path)

        # Define the amount to crop on each side
        crop_amount = 10  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresholded = cv2.threshold(blurred, 127, 127, cv2.THRESH_BINARY)

        # Check for white pixel in the center
        center_pixel = thresholded[height // 2, width // 2]
        if center_pixel == 0:  # 255 represents white in a grayscale image
            return True

        return False

    def is_square_occupied_contours_white(self, image_path):
        image = cv2.imread(image_path)

        # Define the amount to crop on each side
        crop_amount = 10  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

        # Check for white pixel in the center
        center_pixel = thresholded[height // 2, width // 2]
        if center_pixel == 255:  # 255 represents white in a grayscale image
            return True

        return False


    def detect_colour_1(self, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Define the amount to crop on each side
        crop_amount = 30  # adjust this value as needed

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Define the center and size for the crop
        center = (width // 2, height // 2)
        size = (width - 2 * crop_amount, height - 2 * crop_amount)

        # Crop the image
        image = cv2.getRectSubPix(image, size, center)

        # Convert the image to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the colour range for blue and black
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Create masks for blue and black
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_black = cv2.inRange(hsv, lower_black, upper_black)
        # Apply thresholding
        _, mask_blue = cv2.threshold(mask_blue, 5, 255, cv2.THRESH_BINARY)
        _, mask_black = cv2.threshold(mask_black, 5, 255, cv2.THRESH_BINARY)

        # Check if the colours are present in the image
        is_blue_present = np.any(mask_blue)
        is_black_present = np.any(mask_black)

        # Return 1 for blue, 2 for black, or 0 for neither
        if is_blue_present:
            return 1
        elif is_black_present:
            return 2
        else:
            return 0

    def detect_colour_2(self, image_path):
        # Load the image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Reshape the image to be a list of pixels
        pixels = image.reshape(-1, 3)

        # Perform K-means clustering to find the most dominant colors
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(pixels)

        # Count the number of pixels associated with each cluster label
        label_counts = Counter(kmeans.labels_)

        # Get the most common cluster label
        dominant_color = kmeans.cluster_centers_[label_counts.most_common(1)[0][0]]

        # Define the colour range for blue and black
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Check if the dominant colour is within the range for blue or black
        is_blue = np.all((lower_blue <= dominant_color) & (dominant_color <= upper_blue))
        is_black = np.all((lower_black <= dominant_color) & (dominant_color <= upper_black))

        # Return 1 for blue, 2 for black, or 0 for neither
        if is_blue:
            return 1
        elif is_black:
            return 2
        else:
            return 0

    def detect_colour_3(self, image_path):
        # Load the image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the colour range for blue and black
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Create masks for blue and black
        mask_blue = cv2.inRange(image, lower_blue, upper_blue)
        mask_black = cv2.inRange(image, lower_black, upper_black)

        # Calculate the colour histograms
        hist_blue = cv2.calcHist([image], [0], mask_blue, [256], [0, 256])
        hist_black = cv2.calcHist([image], [0], mask_black, [256], [0, 256])

        # Check if the colours are present in the image
        is_blue_present = np.sum(hist_blue) > 0
        is_black_present = np.sum(hist_black) > 0

        # Return 1 for blue, 2 for black, or 0 for neither
        if is_blue_present:
            return 1
        elif is_black_present:
            return 2
        else:
            return 0

    def detect_chess_piece_colour(self, image_path):
        # Initialize a list to store the detected colours
        detected_colors = []

        # Call each detect_colour function once and store the result
        detected_colors.append(self.detect_colour_1(image_path))
        detected_colors.append(self.detect_colour_2(image_path))
        detected_colors.append(self.detect_colour_3(image_path))

        # Compute the most frequently detected colour
        most_common_colour = Counter(detected_colors).most_common(1)[0][0]

        return most_common_colour

    def process_chessboard(self):
        self.previous_occupied_square_array = self.occupied_square_array
        settings.set_value("previous_board", self.previous_occupied_square_array)

        # Define the row labels
        row_labels = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        for i, row in enumerate(self.chessboard_colour_array):
            for j, square in enumerate(row):
                # Define the flag
                average = 0
                # Construct the image path
                image_path = os.path.join("squares", f"{row_labels[i]}_{j + 1}.png")
                # Load the image
                img = cv2.imread(image_path)
                if img is None:
                    print(f"Image not found: {image_path}")
                    continue
                # Process the image
                if square == 0:
                    if self.is_square_occupied_colour_dark(image_path):
                        average += 1
                    if self.is_square_occupied_contours_black(image_path):
                        average += 1
                    if self.is_square_occupied_contours_white(image_path):
                        average += 1
                    if self.is_square_occupied_edges_white(image_path):
                        average += 1
                    if self.is_square_occupied_edges_black(image_path):
                        average += 1

                    if average >= 3:
                        self.occupied_square_array[i][j] = self.detect_chess_piece_colour(image_path)

                    else:
                        self.occupied_square_array[i][j] = 0

                elif square == 1:
                    if self.is_square_occupied_colour_light(image_path):
                        average += 1
                    if self.is_square_occupied_contours_black(image_path):
                        average += 1
                    if self.is_square_occupied_contours_white(image_path):
                        average += 1
                    if self.is_square_occupied_edges_white(image_path):
                        average += 1
                    if self.is_square_occupied_edges_black(image_path):
                        average += 1

                    if average >= 3:
                        self.occupied_square_array[i][j] = self.detect_chess_piece_colour(image_path)

                    else:
                        self.occupied_square_array[i][j] = 0

        settings.set_value("current_board",self.occupied_square_array)
        return self.occupied_square_array


detector = Detector()

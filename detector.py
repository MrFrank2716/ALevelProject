from settings import *
import os
from PIL import Image
import numpy as np
def detect_chess_piece(image_path, square_colour):  # The square's colour passed through is a grayscale value 0-255 a value of 200 seems to work brilliantly for a green board.
    img = Image.open(image_path).convert('L')  # Converts the image to grayscale so it's easier to compare colours.
    width, height = img.size

    # Define points for the 4x4 grid locations to grab the colours.
    points = [(x, y) for x in range(width // 2 - 2, width // 2 + 2) for y in range(height // 2 - 2, height // 2 + 2)]

    # Get the colours of the points using the PIL package built into python.
    colours = [img.getpixel(point) for point in points]

    # Check if the middle points are a different color than the square which is passed through as a parameter.
    return any(abs(colour - square_colour) > settings.return_value("detect_chess_piece_threshold") for colour in
               colours)  # Threshold for the colour comparision - this seems to work great for a green board.


def detect_full_board():
    print(settings.return_value("square_array"))

print(detect_chess_piece("squares/square_C_1.png", 200))
detect_full_board()
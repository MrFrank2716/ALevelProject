import os
import pygame
import pygame_gui
from PIL import Image

import settings
from settings import *
def draw_board(manager, window_surface, window_width):
    # Load the image
    image_path = settings.return_value("chessboard_image_path")
    board_image = pygame.image.load(image_path)

    # Create a UIImage
    board_ui_image = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(((window_width/2) - (board_image.get_width()/4),0), (400,400)),
        image_surface=board_image,
        manager=manager
    )

    # Draw the UIImage on the screen
    manager.update(0.1)  # Update the manager
    manager.draw_ui(window_surface)
    pygame.display.update()

class Piece:
    def __init__(self, image_path, pos, manager):
        self.image = pygame.image.load(image_path)
        self.pos = pos
        self.ui_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(self.pos, (self.image.get_width(), self.image.get_height())),
            image_surface=self.image,
            manager=manager
        )

    def draw(self, window_surface, manager):
        self.ui_image.kill()  # Remove the old image
        self.ui_image = pygame_gui.elements.UIImage(  # Create a new image at the updated position
            relative_rect=pygame.Rect(self.pos, (self.image.get_width(), self.image.get_height())),
            image_surface=self.image,
            manager=manager
        )
        manager.update(0.1)
        manager.draw_ui(window_surface)
        pygame.display.update()

    def move(self, new_pos):
        self.pos = new_pos

def draw_pieces(manager, window_surface, window_width):
    # Load the image
    pawn_image_path = settings.return_value("white_pawn")
    pawn_image = pygame.image.load(pawn_image_path)
    pawn = Piece()


import time
st = time.time()
def detect_chess_piece(image_path, square_colour): # The square's colour passed through is a grayscale value 0-255 a value of 200 seems to work brilliantly for a green board.
    img = Image.open(image_path).convert('L')  # Converts the image to grayscale so it's easier to compare colours.
    width, height = img.size

    # Define points for the 4x4 grid locations to grab the colours.
    points = [(x, y) for x in range(width//2 - 2, width//2 + 2) for y in range(height//2 - 2, height//2 + 2)]

    # Get the colours of the points using the PIL package built into python.
    colours = [img.getpixel(point) for point in points]

    # Check if the middle points are a different color than the square which is passed through as a parameter.
    return any(abs(colour - square_colour) > settings.return_value("detect_chess_piece_threshold") for colour in colours)  # Threshold for the colour comparision - this seems to work great for a green board.

print(detect_chess_piece("squares/square_C_1.png",200))

et = time.time()
elapsed = et - st
print("Execution time:",elapsed)
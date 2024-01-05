import os
import pygame
import pygame_gui

def draw_board(manager, window_surface, window_width):
    # Load the image
    image_path = "images/board.png"
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
    pawn_image_path = "images/white-pawn.png"
    pawn_image = pygame.image.load(pawn_image_path)
    pawn = Piece()
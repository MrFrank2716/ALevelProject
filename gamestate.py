import chess
import chess.svg
import pygame
import pygame_gui
from PIL import Image
from settings import *
import detector
class GameEngine():
    def __init__(self):
        self.board = chess.Board()
        self.move_list = []

    def print_board(self):
        print(self.board)


    def get_latest_board_string(self):
        return self.board

    def get_board(self):
        return self.board

    def verify_checkmate(self):
        return self.board.is_checkmate()

    def is_check(self):
        return self.board.is_check()

    def is_stalemate(self):
        return self.board.is_stalemate()


game = GameEngine()


class ChessBoard:
    def __init__(self, manager, window_surface, window_width):
        self.manager = manager
        self.window_surface = window_surface
        self.window_width = window_width
        self.piece_images = pieceSettings.returnImageLocations()
        self.need_update = True

    def needUpdate(self):
        return self.need_update
    def needUpdateTrue(self):
        self.need_update = True

    def needUpdateFalse(self):
        self.need_update = False

    def draw_board(self, board, image_path):
        # Load the image
        original_board_image = pygame.image.load(image_path)

        # Resize the image
        board_image = pygame.transform.scale(original_board_image, (400, 400))

        # Create a Surface for the chessboard
        chessboard_surface = pygame.Surface((400, 400))

        # Blit the board image onto the chessboard surface
        chessboard_surface.blit(board_image, (0, 0))

        # Draw each piece on the board
        for i in range(8):
            for j in range(8):
                piece = board.piece_at(chess.square(j, 7 - i))
                if piece is not None:
                    piece_image = self.piece_images[str(piece)]
                    x = j * piece_image.get_width()
                    y = i * piece_image.get_height()
                    chessboard_surface.blit(piece_image, (x, y))

        # Create a UIImage from the chessboard surface
        board_ui_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(((self.window_width / 2) - (chessboard_surface.get_width() / 2), 0), (400, 400)),
            image_surface=chessboard_surface,
            manager=self.manager
        )

        # Draw the UIImage on the screen
        self.manager.update(0.1)  # Update the manager
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()
        self.needUpdateFalse()


def movepieces(board):
    move = chess.Move.from_uci('g1f3')  # Move knight from g1 to f3
    board.push(move)
    detector.detect_full_board()
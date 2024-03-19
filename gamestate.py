import chess
import chess.svg
import pygame
import pygame_gui
import internet_chess
from PIL import Image
import numpy
from settings import *
from detector import *


class GameEngine():
    def __init__(self):
        self.board = chess.Board()
        self.move_list = []
        self.previous_board = [[2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1],
                        [2, 2, 0, 0, 0, 0, 1, 1]]
        self.current_board = [[2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1],
                               [2, 2, 0, 0, 0, 0, 1, 1]]

    def move(self, move):
        self.board.push(move)

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

    def is_legal(self, move):
        return self.board.is_legal(move)

    def valid_moves(self):
        return self.board.legal_moves

    def find_chess_move(self):
        # Boards
        previous_board = list(settings.return_value("previous_board"))
        current_board = list(settings.return_value("current_board"))

        # Define the row and column labels
        row_labels = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        col_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

        # Initialize the move variables
        move_from = move_to = None

        # Compare the two boards
        for i in range(8):
            for j in range(8):
                square = f"{row_labels[i]}{col_labels[j]}"
                if previous_board[i][j] == 1:  # Piece moved from this square
                    move_from = square
                elif current_board[i][j] == 1:  # Piece moved to this square
                    move_to = square
        print(f"The move was from {move_from} to {move_to}.")

        move = chess.Move.from_uci(move_from + move_to)
        # Make the move
        self.board.push(move)

    def find_move(self, old_board, new_board):
        # Define the chessboard columns
        row_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        col_labels = ['8', '7', '6', '5', '4', '3', '2', '1']
        # Initialize move variables
        from_square = to_square = None

        # Compare the two boards
        for i in range(8):
            for j in range(8):
                if old_board[i][j] != new_board[i][j]:
                    square = row_labels[i] + col_labels[j]  # Convert to chess notation
                    if old_board[i][j] != 0 and new_board[i][j] == 0:
                        from_square = square
                    elif old_board[i][j] == 0 and new_board[i][j] != 0:
                        to_square = square
                    elif old_board[i][j] != 0 and new_board[i][j] != 0:
                        from_square = square
                        to_square = square
                    elif old_board[i][j] != 0 and new_board[i][j] == 0 and from_square is None:
                        from_square = square
                    elif old_board[i][j] == 0 and new_board[i][j] != 0 and to_square is None:
                        to_square = square
        internet_chess.api.make_move(from_square,to_square)
        return str(from_square) + str(to_square)


    def movepieces(self):
        self.previous_board = self.current_board
        self.current_board = numpy.rot90(numpy.flip(numpy.flip(detector.process_chessboard(),1),0))
        for row in self.previous_board:
            print(row)

        print("current")
        for row in self.current_board:
            print(row)

        self.push_move(str(self.find_move(self.previous_board,self.current_board)))


    def push_move(self,declared_move):
        move = chess.Move.from_uci(declared_move)
        # Make the move
        self.board.push(move)
        # Add move to the list
        self.move_list.append(declared_move)




chessGame = GameEngine()


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

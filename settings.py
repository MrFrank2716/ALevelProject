import pygame

class GlobalSettings:
  def __init__(self):
    self.setting_values = {
      "detect_chess_piece_threshold": 50,
      "dark_square_colour": "Green",
      "chessboard_image_path": "images/board.png",
      "window_width" : 800,
      "window_height" : 600,
      "standard_button": (100, 50),
      "dark_mode": "dark_mode.json",
      "light_mode": "light_mode.json",
      "latest_caption": "Main window",
      "base": 900,
      "height": 900,
      "square_size": 100,
      "transformed_image_name": "transformed",
      "window_switch_time": 0,
      "camera_scale": 4
    }

  def return_value(self,set):
    return self.setting_values[set]

  def set_value(self,set,val):
    self.setting_values[set] = val

settings = GlobalSettings()

class PieceSettings:
  def __init__(self):
    self.piece_image_locations = {
      'r': pygame.transform.scale(pygame.image.load('images/black-rook.png'), (50, 50)),
      'n': pygame.transform.scale(pygame.image.load('images/black-knight.png'), (50, 50)),
      'b': pygame.transform.scale(pygame.image.load('images/black-bishop.png'), (50, 50)),
      'q': pygame.transform.scale(pygame.image.load('images/black-queen.png'), (50, 50)),
      'k': pygame.transform.scale(pygame.image.load('images/black-king.png'), (50, 50)),
      'p': pygame.transform.scale(pygame.image.load('images/black-pawn.png'), (50, 50)),
      'R': pygame.transform.scale(pygame.image.load('images/white-rook.png'), (50, 50)),
      'N': pygame.transform.scale(pygame.image.load('images/white-knight.png'), (50, 50)),
      'B': pygame.transform.scale(pygame.image.load('images/white-bishop.png'), (50, 50)),
      'Q': pygame.transform.scale(pygame.image.load('images/white-queen.png'), (50, 50)),
      'K': pygame.transform.scale(pygame.image.load('images/white-king.png'), (50, 50)),
      'P': pygame.transform.scale(pygame.image.load('images/white-pawn.png'), (50, 50)),
    }

  def returnImageLocations(self):
    return self.piece_image_locations

pieceSettings = PieceSettings()
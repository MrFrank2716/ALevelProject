class GlobalSettings:
  def __init__(self):
    self.setting_values = {
      "detect_chess_piece_threshold": 50,
      "dark_square_colour": "Green",
      "chessboard_image_path": "images/board.png",
      "window_width" : 800,
      "window_height" : 600
    }
  def return_value(self,set):
    return self.setting_values[set]

  def set_value(self,set,val):
    self.setting_values[set] = val

settings = GlobalSettings()

class PieceSettings:
  def __init__(self):
    self.piece_locations = {
      "white_pawn": "images/white-pawn.png"
    }
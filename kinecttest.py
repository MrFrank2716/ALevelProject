import requests
import chess.pgn
import io

def get_chess_time(username):
    response = requests.get(f'https://lichess.org/api/games/user/{username}')
    if response.text:
        pgn = io.StringIO(response.text)
        game = chess.pgn.read_game(pgn)
        # extract the time for the white player
        # replace with the actual key if different
        print(game)
        white_time = game.headers["TimeControl"]  # initial time in seconds
        print(white_time)
    else:
        print("No data received from the API")
        return None

get_chess_time("FrankiePang")

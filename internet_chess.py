import requests
import settings

class lichessAPI:
    def __init__(self):
        self.api_token = settings.settings.return_value("api_token")
        self.game_id = self.get_current_games()

    def make_move(self, from_square, to_square):
        url = f"https://lichess.org/api/board/game/{self.game_id}/move/{from_square}{to_square}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print("Move made successfully")
        else:
            print(f"Failed to make move: {response.content}")

    def get_current_games(self):
        url = "https://lichess.org/api/account/playing"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            games = response.json()['nowPlaying']
            return games[0]['gameId'] if games else None
        else:
            print(f"Failed to get current games: {response.content}")

api = lichessAPI()

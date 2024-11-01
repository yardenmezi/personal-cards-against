from game import Game

class GamesRunner:
    def __init__(self):
        self.games = {}
        self.player_to_chat = {}

    def get_game(self, chat_id):
        if chat_id not in self.games:
            self.games[chat_id] = Game(chat_id)
        return self.games[chat_id]

    def add_player(self, chat_id, player_id):
        self.games[player_id] = self.games[chat_id]
        self.games[chat_id].add_player(player_id)
        self.player_to_chat[player_id] = chat_id

    def get_chat_id(self, player_id):
        return self.player_to_chat[player_id]

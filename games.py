from gamepy.gamemenu.menu import menus
from gamepy.gamesheet.gamesheet import spreadsheets_id, scopes
from gamepy.gamesheet.gameroom import GameRoom

game_room = GameRoom()

class Player:
    def __init__(self, name, strategies, game_id=None, isPlayer1=True):
        self.name = name
        self.strategies = strategies
        self.played_strategy = None
        self.game_id = game_id
        self.isPlayer1 = isPlayer1
    def play(self, played_strategy):
        play_method(self, played_strategy)
    def join(self, room_id):
        game_room_id = self.game_id + ":" + room_id
        if self.isPlayer1:
            game_room.register_player1_name(game_room_id, self.name)
        else:
            game_room.register_player2_name(game_room_id, self.name)

class Games:
    menus = menus
    games_played = dict()
    def __init__(self):
        pass
    def new(self, game_id):
        game = new_method(self, game_id)
        if (not self.__class__.games_played or 
            game_id not in self.__class__.games_played):
            self.__class__.games_played[game_id] = [game]
        else:
            self.__class__.games_played[game_id].append(game)
        return game, game.players
    def switch(self, game_id, index=0):
        return self.__class__.games_played[game_id][index]
    @classmethod
    def new2(cls, game_id):
        game = new_method(cls, game_id)
        if (not cls.games_played or
            game_id not in cls.games_played):
            cls.games_played[game_id] = [game]
        else:
            cls.games_played[game_id].append(game)
        return game, game.players
    @classmethod
    def switch2(cls, game_id, index = 0):
        return cls.games_played[game_id][index]

class Game(Games):
    def __init__(self, player_names, player_strategies, payoffMatrix, name=None, game_id=None):
        super().__init__()
        self.name = name
        self.id = game_id
        self.players = [Player(player_names[i], player_strategies[i], game_id=game_id,
                               isPlayer1 = True if i == 0 else False
                               ) for i in range(len(player_names))]
        self.payoffMatrix = payoffMatrix
    def payoff(self):
        played_strategies = self.players[0].played_strategy, self.players[1].played_strategy
        if all(played_strategies):
            # if both players have played their strategies
            return self.payoffMatrix[played_strategies]
        else:
            print("Not all players have played their strategies yet.")
    def create_room(self, room_id):
        create_room(self, room_id)

# helpers

def new_method(games, game_id):
    selected_game = games.menus[game_id] # access class property
    game = Game(
        selected_game["players"],
        selected_game["strategies"],
        selected_game["payoff_matrix"],
        game_id = game_id
        )
    return game
# helper function
def payoff_method(game):
    played_strategies = game.players[0].played_strategy, game.players[1].played_strategy
    if all(played_strategies):
        # if both players have played their strategies
        return game.payoff_function(played_strategies)
    else:
        print("Not all players have played their strategies yet.")

def play_method(player, played_strategy):
    if played_strategy not in player.strategies:
        raise ValueError("Invalid strategy")
    else:
        player.played_strategy = played_strategy
        
        
def create_room(game, room_id):
    game_room_id = game.id +":"+room_id
    game_room.register_game_room(game_room_id)

from gamepy.gamemenu.menu import menus

class Player:
    def __init__(self, name: str, strategies: list[str]):
        self.name = name
        self.strategies = strategies
        self.played_strategy = None
    def play(self, played_strategy):
        play_method(self, played_strategy)

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
        return game
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
        return game
    @classmethod
    def switch2(cls, game_id, index = 0):
        return cls.games_played[game_id][index]

class Game(Games):
    def __init__(self, player_names, player_strategies, payoffMatrix, name=None):
        super().__init__()
        self.name = name
        self.players = [Player(player_names[i], player_strategies[i]) for i in range(len(player_names))]
        self.payoffMatrix = payoffMatrix
    def payoff(self):
        played_strategies = self.players[0].played_strategy, self.players[1].played_strategy
        if all(played_strategies):
            # if both players have played their strategies
            return self.payoffMatrix[played_strategies]
        else:
            print("Not all players have played their strategies yet.")

# helpers

def new_method(games, game_id):
    selected_game = games.menus[game_id] # access class property
    game = Game(
        selected_game["players"],
        selected_game["strategies"],
        selected_game["payoff_matrix"]
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
        
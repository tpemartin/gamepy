from gamepy.gamemenu.menu import menus
from gamepy.gamesheet.gamesheet import spreadsheets_id, scopes
from gamepy.gamesheet.gameroom import GameRoom
from gamepy.gamesheet.play import PlaySheet, PlayIndex
import numpy as np
import nashpy as nash

game_room = GameRoom()
playSheet = PlaySheet()

class Player:
    def __init__(self, game, name, strategies, game_id=None, isPlayer1=True):
        self.game = game
        self.name = name
        self.strategies = strategies
        self.played_strategy = None
        self.game_id = game_id
        self.isPlayer1 = isPlayer1
        self.gameRoomSheet = game_room
        self.playSheet = playSheet
        self.round = 0
    def play(self, played_strategy):
        self.playPure = True
        play_method(self, played_strategy)
        mixed_strategy = convert_to_mixed_strategy(self, played_strategy)
        mix(self, mixed_strategy)
        game_room_id = self.game_id + ":" + self.room_id
        self.round += 1
        if self.isPlayer1:
            self.gameRoomSheet = game_room.register_player1_choice(game_room_id, self.played_strategy, self.round)
            self.gameRoomSheet.register_player1_mix(game_room_id, str(self.mixed_strategy))
            self.playSheet = playSheet.register_player1_choice(game_room_id, self.played_strategy)
            self.playSheet.register_player1_mix(game_room_id, str(self.mixed_strategy))
        else:
            self.gameRoomSheet = game_room.register_player2_choice(game_room_id, self.played_strategy, self.round)
            self.gameRoomSheet.register_player2_mix(game_room_id, str(self.mixed_strategy))
            self.playSheet = playSheet.register_player2_choice(game_room_id, self.played_strategy)
            self.playSheet.register_player2_mix(game_room_id, str(self.mixed_strategy))   
    def play_mixed(self, mixed_strategy):
        self.playPure = False
        mix(self, mixed_strategy)
        self.played_strategy = random_play(self)
        game_room_id = self.game_id + ":" + self.room_id
        self.round += 1
        if self.isPlayer1:
            self.gameRoomSheet = game_room.register_player1_choice(game_room_id, self.played_strategy, self.round)
            self.gameRoomSheet.register_player1_mix(game_room_id, str(self.mixed_strategy))
            self.playSheet = playSheet.register_player1_choice(game_room_id, self.played_strategy)
            self.playSheet.register_player1_mix(game_room_id, str(self.mixed_strategy))
        else:
            self.gameRoomSheet = game_room.register_player2_choice(game_room_id, self.played_strategy, self.round)
            self.gameRoomSheet.register_player2_mix(game_room_id, str(self.mixed_strategy))
            self.playSheet = playSheet.register_player2_choice(game_room_id, self.played_strategy)
            self.playSheet.register_player2_mix(game_room_id, str(self.mixed_strategy))
        
    def join(self, room_id):
        game_room_id = self.game_id + ":" + room_id
        self.room_id = room_id
        if game_room_id not in self.gameRoomSheet.record.keys():
                create_gameRoomSheetRecord(self, room_id)
        if game_room_id not in self.playSheet.record.keys():
                create_playSheetRecord(self, room_id)
        if self.isPlayer1:
            self.gameRoomSheet = game_room.register_player1_name(game_room_id, self.name)
            self.playSheet = playSheet.register_player1_name(game_room_id, self.name)
        else:
            self.gameRoomSheet = game_room.register_player2_name(game_room_id, self.name)
            self.playSheet = playSheet.register_player2_name(game_room_id, self.name)
    def payoff(self):
        player_payoff(self)
        print(get_expected_payoff(self.game))
    
        

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
        self.players = [Player(self, player_names[i], player_strategies[i], game_id=game_id,
                               isPlayer1 = True if i == 0 else False
                               ) for i in range(len(player_names))]
        self.payoffMatrix = payoffMatrix
        self._nashpy = generate_nashpyGame(self)
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
    return player
        
        
def create_room(game, room_id):
    game_room_id = game.id +":"+room_id
    game.room_id = room_id
    game_room.register_game_room(game_room_id)
    playSheet.register_play(game_room_id)

def player_payoff(player):
    try:
        playSheetRow = player.playSheet.record[player.game_id+':'+player.room_id]
        playResult = player.playSheet._get(f"A{playSheetRow}:G{playSheetRow}")
        player.game.players[0].played_strategy = playResult[0][PlayIndex.player1_choice]
        player.game.players[1].played_strategy = playResult[0][PlayIndex.player2_choice]
    except:
        raise Exception("Other player has not played yet")
    payoff_result = player.game.payoff()
    player.game.payoff_result = payoff_result
    player.payoff_result = payoff_result[0] if player.isPlayer1 else payoff_result[1]
    print((player.payoff_result, player.game.payoff_result))
    return player

def create_playSheetRecord(player, room_id):
    game_room_id = player.game_id+':'+room_id
    rowNumber = player.playSheet._get("A1:A").index([game_room_id])+1
    player.playSheet.record = {game_room_id: rowNumber}
    return rowNumber

def create_gameRoomSheetRecord(player, room_id):
    game_room_id = player.game_id+':'+room_id
    rowNumber = player.gameRoomSheet._get("A1:A").index([game_room_id])+1
    player.gameRoomSheet.record = {game_room_id: rowNumber}
    return rowNumber

def get_expected_payoff(game):
    return game._nashpy[game.players[0].mixed_strategy_array, game.players[1].mixed_strategy_array]

def mix(player, mixed_strategy):
    # convert mixed strategy to array
    mixed_strategy_array = np.array([v for v in mixed_strategy.values()])
    player.mixed_strategy = mixed_strategy
    player.mixed_strategy_array = mixed_strategy_array
    return player

def generate_nashpyGame(game):
    payoffMat1= []
    payoffMat2= []
    for i in  range(len(game.players[0].strategies)):
        for j in range(len(game.players[1].strategies)):
            payoffMat1.append(game.payoffMatrix[(game.players[0].strategies[i], game.players[1].strategies[j])][0])
            payoffMat2.append(game.payoffMatrix[(game.players[0].strategies[i], game.players[1].strategies[j])][1])
            print(game.players[0].strategies[i], game.players[1].strategies[j], game.payoffMatrix[(game.players[0].strategies[i], game.players[1].strategies[j])])

    payoffMat1 = np.array(payoffMat1).reshape(len(game.players[0].strategies), len(game.players[1].strategies))
    payoffMat2 = np.array(payoffMat2).reshape(len(game.players[0].strategies), len(game.players[1].strategies))
    return nash.Game(payoffMat1, payoffMat2)

def random_play(player):
    strategies = player.strategies
    prob = player.mixed_strategy_array
    return np.random.choice(strategies, p=prob)

def convert_to_mixed_strategy(player, strategy):
    mixed_strategy = {}
    for s in player.strategies:
        if s == strategy:
            mixed_strategy[s] = 1
        else:
            mixed_strategy[s] = 0
    return mixed_strategy
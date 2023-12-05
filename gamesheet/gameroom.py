import re
from .gamesheet import Sheet

class GameRoomIndex:
    (game_room_id,
    game_id,
    room_id,
    player1_id,
    player2_id,
    round_number,
    player1_choice,
    player2_choice,
    payoff) = [x for x in range(9)]

class GameRoom(Sheet):
    record = dict()
    def __init__(self, spreadsheets_id, scopes):
        super().__init__("game-room", spreadsheets_id, scopes)
    def register_game_room(self, game_room_id):
        game_id, room_id = game_room_id.split(":")
        values = [game_room_id, game_id, room_id]
        result = self._append(values)
        self.__class__.record[game_room_id] = find_row_number_from_range(
              result['updates']['updatedRange']
          )
        return self
    def register_player1_name(self, game_room_id, player1_name):
        values = self._create_values(GameRoomIndex.player1_id, player1_name)
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self
    def register_player2_name(self, game_room_id, player2_name):
        values = [None]*(GameRoomIndex.player2_id+1)
        values[GameRoomIndex.player2_id] = player2_name
        row_index = self.record[game_room_id]
        self._update(row_index, values)
    def register_player1_choice(self, game_room_id, player1_choice):
        values = [None]*(GameRoomIndex.player1_choice+1)
        values[GameRoomIndex.player1_choice] = player1_choice
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self
    def register_player2_choice(self, game_room_id, player2_choice):
        values = [None]*(GameRoomIndex.player2_choice+1)
        values[GameRoomIndex.player2_choice] = player2_choice
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self
    def register_payoff(self, game_room_id, payoff):
        values = self._create_values(GameRoomIndex.payoff, payoff)
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self


# helpers

def find_row_number_from_range(range):
    return int(re.findall(r"\d+",range)[0])

import re
from .gamesheet import Sheet
from . import scopes, spreadsheets_id

class GameRoomIndex:
    (game_room_id,
    game_id,
    room_id,
    player1_id,
    player2_id,
    round_number,
    player1_choice,
    player2_choice,
    payoff,
    player1_mix,
    player2_mix,
    expect_payoff) = [x for x in range(12)]

class GameRoom(Sheet):
    record = dict()
    def __init__(self):
        super().__init__("game-room", spreadsheets_id, scopes)
    def register_game_room(self, game_room_id):
        game_id, room_id = game_room_id.split(":")
        values = [game_room_id, game_id, room_id, None, None, 1]
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
    def register_player1_choice(self, game_room_id, player1_choice, round =1):
        values = [None]*(GameRoomIndex.player1_choice+1)
        values[GameRoomIndex.player1_choice] = player1_choice
        row_index = self.record[game_room_id]
        self.round=round
        self._update(row_index, values)
        return self
    def register_player2_choice(self, game_room_id, player2_choice, round=1):
        values = [None]*(GameRoomIndex.player2_choice+1)
        values[GameRoomIndex.player2_choice] = player2_choice
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        self.round=round
        return self
    def register_payoff(self, game_room_id, payoff):
        values = self._create_values(GameRoomIndex.payoff, payoff)
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self
    def register_player1_mix(self, game_room_id, player1_mix):
        values = self._create_values(GameRoomIndex.player1_mix, player1_mix)
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self
    def register_player2_mix(self, game_room_id, player2_mix):
        values = self._create_values(GameRoomIndex.player2_mix, player2_mix)
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self
    def register_expect_payoff(self, game_room_id, expect_payoff):
        values = self._create_values(GameRoomIndex.expect_payoff, expect_payoff)
        row_index = self.record[game_room_id]
        self._update(row_index, values)
        return self


# helpers

def find_row_number_from_range(range):
    return int(re.findall(r"\d+",range)[0])

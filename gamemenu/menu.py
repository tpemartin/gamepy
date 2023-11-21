# prisoner's dilemma game
games = [{
    "game_id": "g-1",
    "name": "prisoner's dilemma",
    "players": ["player1", "player2"],
    "strategies": [
                ['C', 'D'],
                ['C', 'D']
            ],
    "payoff_matrix": {
            ('C', 'C'): (-1, -1),
            ('C', 'D'): (-3, 0),
            ('D', 'C'): (0, -3),
            ('D', 'D'): (-2, -2)
        }
},
# paper, scissors, rock game
{
    "game_id": "g-2",
    "name": "paper, scissors, rock",
    "players": ["player1", "player2"],
    "strategies": [
                ['paper', 'scissors', 'rock'],
                ['paper', 'scissors', 'rock']
            ],
    "payoff_matrix": {
            ('paper', 'paper'): (0, 0),
            ('paper', 'scissors'): (-1, 1),
            ('paper', 'rock'): (1, -1),
            ('scissors', 'paper'): (1, -1),
            ('scissors', 'scissors'): (0, 0),
            ('scissors', 'rock'): (-1, 1),
            ('rock', 'paper'): (-1, 1),
            ('rock', 'scissors'): (1, -1),
            ('rock', 'rock'): (0, 0)
        }
}]

game_dict = {"g-1":1, "g-2":2}
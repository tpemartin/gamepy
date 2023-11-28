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
# P, S, R game
{
    "game_id": "g-2",
    "name": "Paper, Scissor, Rock",
    "players": ["player1", "player2"],
    "strategies": [
                ['P', 'S', 'R'],
                ['P', 'S', 'R']
            ],
    "payoff_matrix": {
            ('P', 'P'): (0, 0),
            ('P', 'S'): (-1, 1),
            ('P', 'R'): (1, -1),
            ('S', 'P'): (1, -1),
            ('S', 'S'): (0, 0),
            ('S', 'R'): (-1, 1),
            ('R', 'P'): (-1, 1),
            ('R', 'S'): (1, -1),
            ('R', 'R'): (0, 0)
        }
}]

menus = {g["game_id"]: g for g in games}
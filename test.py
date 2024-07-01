import alpha_beta
from simple_game_state import *

test_game_state = {
    "game": {
        "id": "totally-unique-game-id",
        "ruleset": {
            "name": "standard",
            "version": "v1.1.15",
            "settings": {
                "foodSpawnChance": 15,
                "minimumFood": 1,
                "hazardDamagePerTurn": 14
            }
        },
        "map": "standard",
        "source": "league",
        "timeout": 500
    },
    "turn": 1,
    "board": {
        "height": 11,
        "width": 11,
        "food": [
            {"x": 2, "y": 6},
            {"x": 9, "y": 7},
        ],
        "hazards": [
        ],
        "snakes": [
            {
                "id": "snake-0",
                "name": "My Snake",
                "health": 100,
                "body": [
                    {"x": 2, "y": 5},
                    {"x": 2, "y": 4},
                    {"x": 2, "y": 3}
                ],
                "latency": "111",
                "head": {"x": 2, "y": 5},
                "length": 3,
                "shout": "why are we shouting??",
                "customizations": {
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel"
                }
            },
            {
                "id": "snake-1",
                "name": "Another Snake",
                "health": 100,
                "body": [
                    {"x": 2, "y": 2},
                    {"x": 3, "y": 2},
                    {"x": 4, "y": 2}
                ],
                "latency": "222",
                "head": {"x": 2, "y": 2},
                "length": 3,
                "shout": "I'm not really sure...",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled"
                }
            },
            {
                "id": "snake-2",
                "name": "Another Snake",
                "health": 100,
                "body": [
                    {"x": 6, "y": 5},
                    {"x": 7, "y": 5},
                    {"x": 8, "y": 5},
                    {"x": 9, "y": 5}
                ],
                "latency": "222",
                "head": {"x": 5, "y": 5},
                "length": 4,
                "shout": "I'm not really sure...",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled"
                }
            },
            {
                "id": "snake-3",
                "name": "Another Snake",
                "health": 100,
                "body": [
                    {"x": 5, "y": 6},
                    {"x": 5, "y": 7},
                    {"x": 5, "y": 8}
                ],
                "latency": "222",
                "head": {"x": 5, "y": 6},
                "length": 3,
                "shout": "I'm not really sure...",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled"
                }
            },
        ]
    },
    "you": {
        "id": "snake-0",
        "name": "My Snake",
        "health": 100,
        "body": [
            {"x": 2, "y": 5},
            {"x": 2, "y": 4},
            {"x": 2, "y": 3}
        ],
        "latency": "111",
        "head": {"x": 2, "y": 5},
        "length": 3,
        "shout": "why are we shouting??",
        "customizations": {
            "color": "#FF0000",
            "head": "pixel",
            "tail": "pixel"
        }
    }
}

test_moves_1 = [["snake-0", "up"], ["snake-1", "up"], ["snake-2", "left"], ["snake-3", "down"]]
test_moves_2 = [["snake-0", "down"]] # player dies
test_moves_3 = [["snake-0", "up"], ["snake-1", "right"], ["snake-2", "right"], ["snake-3", "up"]] # player wins

state = SimpleGameState(test_game_state)
move = test_moves_1
#print(state.next_state(move))
#print(alpha_beta.utility(state.next_state(move)))


#foo = alpha_beta.alpha_beta_decision(test_game_state, 2)
#print(foo)
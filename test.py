import time
from monte_carlo_tree_search.simple_game_state_new import SimpleGameState
from monte_carlo_tree_search.mcts import mcts
from monte_carlo_tree_search.heuristic import heuristic_2, normalize_heuristic

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
                    {"x": 2, "y": 3},
                    {"x": 1, "y": 3}
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
            }
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
player_move = "up"

start = time.time()

state = SimpleGameState(test_game_state)
print(mcts(state, 10, 10))

end = time.time()

print(((end - start)*1000), "ms")
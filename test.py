import time

from alpha_beta import alpha_beta_new, simple_game_state_new

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

start = time.time()
state = simple_game_state_new.SimpleGameState(test_game_state)

move = alpha_beta_new.alpha_beta(state, 11)
end = time.time()

print(move)

print(end - start, "s")
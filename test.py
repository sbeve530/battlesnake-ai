

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
            {"x": 5, "y": 5},
            {"x": 9, "y": 0},
            {"x": 2, "y": 6}
        ],
        "hazards": [
        ],
        "snakes": [
            {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "name": "My Snake",
                "health": 100,
                "body": [
                    {"x": 0, "y": 0},
                    {"x": 1, "y": 0},
                    {"x": 2, "y": 0}
                ],
                "latency": "111",
                "head": {"x": 0, "y": 0},
                "length": 3,
                "shout": "why are we shouting??",
                "customizations":{
                    "color":"#FF0000",
                    "head":"pixel",
                    "tail":"pixel"
                }
            },
            {
                "id": "snake-b67f4906-94ae-11ea-bb37",
                "name": "Another Snake",
                "health": 16,
                "body": [
                    {"x": 5, "y": 4},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 3},
                    {"x": 6, "y": 2}
                ],
                "latency": "222",
                "head": {"x": 5, "y": 4},
                "length": 4,
                "shout": "I'm not really sure...",
                "customizations":{
                    "color":"#26CF04",
                    "head":"silly",
                    "tail":"curled"
                }
            }
        ]
    },
    "you": {
        "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0}
        ],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "customizations": {
            "color":"#FF0000",
            "head":"pixel",
            "tail":"pixel"
        }
    }
}

test_moves = [
    "up", "up"
]
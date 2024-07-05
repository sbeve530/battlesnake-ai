def create_board(board, snakes, hazards):
    height = board['height']
    width = board['width']
    matrix = [[0 for _ in range(width)] for _ in range(height)]

    for food in board['food']:
        matrix[food['x']][food['y']] = 0

    for hazard in hazards:
        matrix[hazard['x']][hazard['y']] = 2

    for snake in snakes:
        for segment in snake['body']:
            matrix[segment['x']][segment['y']] = 1

    return matrix


def floodfill(matrix, start):
  rows, cols = len(matrix), len(matrix[0])
  x,y = start
  if matrix[x][y] != 0:
    return 0

    stack = [(x,y)]
    area = 0
    visited = set()

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited or cx < 0 or cx >= rows or cy < 0 or cy >= cols or matrix[cx][cy] != 0:
            continue

        visited.add((cx, cy))
        area += 1

        stack.append((cx+1, cy))
        stack.append((cx-1, cy))
        stack.append((cx, cy+1))
        stack.append((cx, cy-1))


    return area

# so wird heuristik dann irgendwie in next_move integriert
#
# matrix = create_board(board, board['snakes'], board['hazards'])
# max_area = -1
# best move = "up"
# for move in possible_moves:
#         new_head = directions[move]
#         area = flood_fill_battlesnake(matrix, new_head)
#         if area > max_area:
#             max_area = area
#             best_move = move


test_data = {
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
    "turn": 14,
    "board": {
        "height": 11,
        "width": 11,
        "food": [
            {"x": 5, "y": 5},
            {"x": 9, "y": 0},
            {"x": 2, "y": 6}
        ],
        "hazards": [
            {"x": 3, "y": 2}
        ],
        "snakes": [
            {
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
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel"
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
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled"
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
            "color": "#FF0000",
            "head": "pixel",
            "tail": "pixel"
        }
    }
}

print(create_board(test_data['board'], test_data['snakes'], test_data['hazards']))
from typing import Dict
from monte_carlo_tree_search.simple_game_state_new import SimpleGameState

from monte_carlo_tree_search.snake import Snake


def heuristic(state: SimpleGameState, snake: Snake) -> Dict[str, float]:
    def distance_to_nearest_food(point: Dict[str, float]) -> int:
        min_dist = float("inf")
        for food in state.foods:
            min_dist = min(min_dist, abs(food["x"] - point["x"]) + abs(food["y"] - point["y"]))
        return min_dist

    heuristic = dict([[move, 0] for move in state.safe_moves(snake)])
    new_head = snake.head.copy()
    for move, probability in heuristic.items():
        if move == "left":
            new_head["x"] -= 1
        elif move == "right":
            new_head["x"] += 1
        elif move == "up":
            new_head["y"] += 1
        elif move == "down":
            new_head["y"] -= 1

        heuristic[move] -= distance_to_nearest_food(new_head)

    return heuristic


# ideas:
# - approach smaller snakes, avoid bigger snakes
# - get food until bigger than every other snake (hunting and collecting mode)
# - avoid map boarders
# - avoid inner spirals (no three same turns in a row)
# - avoid areas smaller than self
# - prioritize food based on hea;th
# - lock off map when longer than 11
# - floodfill evidence / provocation
# - circle food

def heuristic_2(state: SimpleGameState, snake: Snake) -> Dict[str, float]:
    heuristic = dict([[move, 0] for move in state.safe_moves(snake)])
    for move, probability in heuristic.items():
        new_head = snake.head.copy()

        if move == "left":
            new_head["x"] -= 1
        elif move == "right":
            new_head["x"] += 1
        elif move == "up":
            new_head["y"] += 1
        elif move == "down":
            new_head["y"] -= 1

        heuristic[move] += (
                10 * food_rating(new_head, state.foods, state.x_size) +
                1 * board_pos_rating(new_head, state.x_size, state.y_size)
        )

    return normalize_heuristic(heuristic)


def food_rating(point: Dict, foods: Dict, board_size: int) -> float:
    """Rates position based on foods on the board. 1 if on food, 0 if no food available, otherwise (0, 1) based on distance to nearest food.
    :param point: Point on the board
    :param foods: List of foods
    :return: Rating of food-situation"""
    if foods == []:
        return 0
    min_dist = float('inf')
    for food in foods:
        if food["x"] == point["x"] and food["y"] == point["y"]:
            return 1.0
        distance = manhattan_distance(food, point)
        if distance < min_dist:
            min_dist = distance
    if min_dist < (board_size - 1) * 2:
        return 1 / (min_dist + 1)


def board_pos_rating(point: Dict, x_size: int, y_size: int) -> float:
    """Rates position based in relation to borders and corners of the board.
    :param point: Point on the board
    :param x_size: Size of x axis
    :param y_size: Size of y axis
    :return: Rating of board position. 0 for corners, 0.5 for edges, 1 otherwise"""
    if point["x"] == 0 or point["x"] == x_size - 1:
        if point["y"] == 0 or point == y_size - 1:
            return 0
        return 0.5
    if point["y"] == 0 or point["y"] == y_size - 1:
        return 0.5
    return 1.0


def manhattan_distance(point_a: Dict[str, int], point_b: Dict[str, int]) -> int:
    return abs(point_a["x"] - point_b["x"]) + abs(point_a['y'] - point_b['y'])


def normalize_heuristic(heuristic: Dict[str, float]) -> Dict[str, float]:
    values = [heuristic[move] for move, probability in heuristic.items()]
    _sum = sum(values)
    if _sum == 0:
        return heuristic
    return dict([[move, (heuristic[move] / _sum)] for move in heuristic])

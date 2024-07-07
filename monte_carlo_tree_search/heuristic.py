# Florian Darsow, 222200974
# Michael Gutbrod, 222201691
# Milan Kai, 222201385
# Jannes Peters, 221201486
# Felix Thiesen, 223202358

from typing import Dict
from monte_carlo_tree_search.simple_game_state import SimpleGameState

from monte_carlo_tree_search.snake import Snake


# ideas:
# - approach smaller snakes, avoid bigger snakes
# - get food until bigger than every other snake (hunting and collecting mode)
# X avoid map boarders
# ? avoid inner spirals (no three same turns in a row?)
# ? avoid areas smaller than self
# X prioritize food based on hea;th
# - lock off map when longer than 11
# ? floodfill evidence / provocation
# - circle food
# X avoid head-to-head

def heuristic(state: SimpleGameState, snake: Snake) -> Dict[str, float]:
    """A heuristic function that calculates a utility value for every legal move of a snake in the given game state.
    :param state: The game state to evaluate on
    :param snake: The snake to evaluate for
    :return: A Dict containing a utility value for each legal move of a snake in the given game state. Sum of all utility values is 1"""
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
                5 * food_rating(new_head, state.foods, state.x_size) +
                0.5 * board_pos_rating(new_head, state.x_size, state.y_size) +
                1 * head_to_head(new_head, state.opponent.head, len(snake.body), len(state.opponent.body), 2,
                                 state.x_size)
        )
    res = normalize_heuristic(heuristic)
    return res


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
    else:
        return 0.5  # default


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


def head_to_head(new_player_head, opp_head, player_size, opp_size, min_size_difference, board_size) -> float:
    """Calculates head-to-head utility for a given position and a given game state.
    :param new_player_head: The new head location of the player
    :param opp_head: The head location of the opponent
    :param player_size: The size of the player snake
    :param opp_size: The size of the opponent snake
    :param min_size_difference: The minimum size difference between player and opponent needed to reward approaching opponent's head
    :param board_size: The size of the board of the game
    :return: 0 if player would collide with opponent body, (0, 1) depending on distance to opponent's head depending on if bigger than opponent"""
    distance = manhattan_distance(new_player_head, opp_head)
    if player_size >= (opp_size + min_size_difference):
        if distance == 0:
            return 0
        else:
            return 1 / (distance)
    else:
        if distance == 0:
            return 0
        else:
            return distance / (2 * (board_size - 1))


def manhattan_distance(point_a: Dict[str, int], point_b: Dict[str, int]) -> int:
    """Calculates the manhattan distance between two points.
    :param point_a: Point on the board
    :param point_b: Point on the board
    :return: Manhattan distance of point_a and point_b"""
    return abs(point_a["x"] - point_b["x"]) + abs(point_a['y'] - point_b['y'])


def normalize_heuristic(heuristic: Dict[str, float]) -> Dict[str, float]:
    """Normalizes given heuristic Dict, making sure all values sum up to 1
    :param heuristic: Dictionary containing heuristic values
    :return: Dictionary containing normalized heuristic values"""
    values = [heuristic[move] for move, probability in heuristic.items()]
    _sum = sum(values)
    if _sum == 0:
        return heuristic
    return dict([[move, (heuristic[move] / _sum)] for move in heuristic])

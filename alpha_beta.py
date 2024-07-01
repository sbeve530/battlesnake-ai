import itertools
from copy import deepcopy
from typing import Dict, List, Tuple
from simple_game_state import SimpleGameState
import math
from itertools import product
import time


def alpha_beta_decision(game_state: Dict, depth: int) -> Dict:
    """Calculates the best move by exploring possible paths up to a specified depth.
    Rates the final states using a utility function and then backtracks, storing the worst outcome for each path.
    At depth=1, it selects the move that provides the best of these worst outcomes.
    It is not assumed, that opponents play optimal, but rather that they play safe.
    :param game_state: The game state to calculate the best move for.
    :param depth: The depth of the game state.
    :return: The best move based on the given game state and used utility function.
    """
    if depth < 1:
        return {"move": "down"}
    
    initial_state = SimpleGameState(game_state)
    player_index = initial_state.get_player_index()
    beta = math.inf
    best_move = None
    best_value = -math.inf

    # all_moves_each_snake = [[[snake[0], move] for move in initial_state.get_safe_moves(snake_index)] for
    #                        snake_index, snake in enumerate(initial_state.snakes)]

    # all possible moves for every snake that isn't the player
    all_moves_each_np_snake = [[[snake[0], move] for move in initial_state.get_safe_moves(snake_index)] for
                               snake_index, snake in enumerate(initial_state.snakes) if
                               snake[0] != initial_state.player_id]

    # for each possible move of player, get min of all following paths
    for safe_move in initial_state.get_safe_moves(player_index):
        cartesian = snakes_moves_cartesian(all_moves_each_np_snake)
        for move_list in cartesian:
            foobar = math.inf
            move_list.insert(0, [initial_state.player_id, safe_move])  # insert player move to cartesian
            successor_state = initial_state.next_state(move_list)
            foo = utility(successor_state)
            if foo < foobar:
                foobar = foo
        if foobar > best_value:
            best_value = foobar
            best_move = safe_move

    return {"move": best_move} if best_move else {"move": "down"}


def min_value_2(current_game_state: SimpleGameState, depth: int) -> float:
    """"""
    if depth < 1 or is_terminal(current_game_state):
        return utility(current_game_state)
    player_index = current_game_state.get_player_index()
    value = math.inf
    _all_moves_np_snakes = all_moves_np_snakes(current_game_state)
    for safe_move in current_game_state.get_safe_moves(player_index):
        value_3 = math.inf
        cartesian = snakes_moves_cartesian(_all_moves_np_snakes)
        for move_list in cartesian:
            next_state = current_game_state.next_state(move_list)
            value_2 = min_value_2(next_state, depth - 1)
            if value_2 < value:
                value = value_2
    return value


def all_moves_np_snakes(game_state: SimpleGameState):
    """Calculates all possible safe move combinations for all non-player snakes.
    :param game_state: The game state to calculate the best move for.
    :return: A list of all possible safe move combinations."""
    return [[[snake[0], move] for move in game_state.get_safe_moves(snake_index)] for
            snake_index, snake in enumerate(game_state.snakes) if
            snake[0] != game_state.player_id]


def max_value(simplified_game_state, alpha, beta, depth) -> float:  # TODO: adapt to simple_game_state.py
    if depth < 1 or is_terminal(simplified_game_state):
        return utility(simplified_game_state)
    value = -math.inf
    for moves, new_state in successors(simplified_game_state):
        value = max(value, min_value(new_state, alpha, beta, depth - 1))
        if value >= beta:
            return value
        alpha = max(alpha, value)

    return value


def min_value(current_game_state: SimpleGameState, alpha, beta, depth) -> float:  # TODO: adapt to simple_game_state.py
    if depth < 1 or is_terminal(current_game_state):
        return utility(current_game_state)

    value = math.inf
    # for moves, new_state in successors(simplified_game_state):
    #    value = min(value, max_value(new_state, alpha, beta, depth - 1))
    #    if value <= alpha:
    #        return value

    return value


def snakes_moves_cartesian(moves_per_snake: list):
    """
    :param moves_per_snake: list of lists of tuples of snake_id and move
    :return: cartesian product of all moves per snake
    """
    combinations = list(product(*moves_per_snake))
    combinations = [list(combo) for combo in combinations]
    return combinations


def utility(simplified_game_state: SimpleGameState) -> float:
    """Calculates the utility value of a given game state.
    The utility value greater the closer food is.
    :param simplified_game_state: SimpleGameState object
    :return: utility value of the game state. Returns -inf if player is dead.
    """
    if simplified_game_state == []:
        return -math.inf
    utility_value = 0

    my_head = next(
        snake[1][0] for snake in simplified_game_state.snakes if snake[0] == simplified_game_state.player_id)
    min_distance = math.inf
    if simplified_game_state.player_has_grown == True:
        utility_value += 100
    for food in simplified_game_state.foods:
        distance = food_distance(my_head, food)
        if distance < min_distance:
            min_distance = distance
    utility_value += 1 / min_distance
    return utility_value
    ###
    # ideas:
    # - approach smaller snakes, avoid bigger snakes
    # - get food until bigger than every other snake (hunting and collecting mode)
    # - avoid map boarders
    # - avoid inner spirals (no three same turns in a row)
    # - lock off map when longer than 11
    # - floodfill evidence / provocation
    # - circle food

def food_distance(head_pos, food_pos) -> float:
    return abs(head_pos["x"] - food_pos["x"]) + abs(head_pos["y"] - food_pos["y"])


def is_terminal(simplified_game_state: SimpleGameState) -> bool:
    if simplified_game_state == []:
        return True
    return False

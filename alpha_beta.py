import itertools
from copy import deepcopy
from typing import Dict, List, Tuple
from simple_game_state import SimpleGameState
import math
from itertools import product
import time


def alpha_beta_decision(game_state: Dict, depth: int) -> Dict:
    if depth < 1:
        return {"move": "down"}
    simplified_game_state = SimpleGameState(game_state)
    alpha = -math.inf
    beta = math.inf
    best_move = None
    best_value = -math.inf
    all_moves_each_snake = [[[snake[0], move] for move in simplified_game_state.get_safe_moves(snake_index)] for
                            snake_index, snake in enumerate(simplified_game_state.snakes)]

    for move_list in snakes_moves_cartesian(all_moves_each_snake):
        # print(move_list)
        next_state = simplified_game_state.next_state(move_list)
        value = min_value(next_state, alpha, beta, depth - 1)
        if value > best_value:
            best_value = value
            # TODO: ab hier
            # best_move = [move for move in move_list if move[0] == simplified_game_state.player_id]
            best_move = move_list.filter(lambda move: move[0] == simplified_game_state.player_id)

    # for moves, new_state in simplified_game_state.next_state():
    #    value = min_value(new_state, alpha, beta, depth - 1)
    #    if value > best_value:
    #        best_value = value
    #        best_move = moves[0]

    ###

    # print(all_moves_each_snake)
    # print("kart. product test:")
    # print(snakes_moves_cartesian(all_moves_each_snake))
    # print("length: " + str(len(snakes_moves_cartesian(all_moves_each_snake))))

    return best_move


def snakes_moves_cartesian(moves_per_snake: list):
    """
    :param moves_per_snake: list of lists of tuples of snake_index and move
    :return: cartesian product of all moves per snake
    """
    combinations = list(product(*moves_per_snake))
    combinations = [list(combo) for combo in combinations]
    return combinations

    # return {"move": best_move} if best_move else {"move": "down"}


def max_value(game_state, alpha, beta, depth) -> float:  # TODO: adapt to simple_game_state.py
    if depth < 1 or is_terminal(game_state):
        foo = utility(game_state)
        print(foo)
        return foo
    value = -math.inf
    for moves, new_state in successors(game_state):
        value = max(value, min_value(new_state, alpha, beta, depth - 1))

        if value >= beta:
            return value
        alpha = max(alpha, value)

    return value


def min_value(game_state, alpha, beta, depth) -> float:  # TODO: adapt to simple_game_state.py
    if depth < 1 or is_terminal(game_state):
        foo = utility(game_state)
        print(foo)
        return foo
    value = math.inf
    for moves, new_state in successors(game_state):
        value = min(value, max_value(new_state, alpha, beta, depth - 1))
        if value <= alpha:
            return value

        beta = min(beta, value)

    return value


# Utility function to evaluate game state based on the sum of the inverses of the distances to the food sources
def utility(game_state: Dict) -> float:  # TODO: adapt to simple_game_state.py; improve heuristic
    utility_value = 0
    my_head = game_state["you"]["body"][0]
    food_sources = game_state["board"]["food"]

    total_inverse_distance = 0
    for food in food_sources:
        distance = abs(my_head["x"] - food["x"]) + abs(my_head["y"] - food["y"])
        if distance != 0:
            total_inverse_distance += 1 / distance
        else:
            utility_value += 3

    utility_value += total_inverse_distance / len(food_sources)

    return utility_value


# TODO: check if next_state returns []
def is_terminal(game_state: Dict) -> bool:
    return False

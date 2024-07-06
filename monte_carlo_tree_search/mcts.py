import random

from monte_carlo_tree_search.simple_game_state_new import SimpleGameState
from monte_carlo_tree_search.snake import Snake
from monte_carlo_tree_search.heuristic import heuristic_2


def mcts(state: SimpleGameState, samples_per_move: int, max_sample_depth: int) -> str:
    """Un-optimized version of the Monte Carlo Tree Search algorithm. This implementation currently only checks random pahts.
    :param state: SimpleGameState object representing the current game state
    :param samples_per_move: Number of samples to evaluate per move
    :param max_sample_depth: Maximum depth of the tree search
    :return: the best-evaluated move"""
    safe_moves = state.safe_moves(state.player)
    bar = heuristic_2(state, state.player)
    print(bar)

    if safe_moves == []: # catch exception
        return "down"  # default

    move_ratings = []

    for move in safe_moves:
        outcomes = []
        for sample in range(samples_per_move):
            outcomes.append(get_outcome(state, move, max_sample_depth))
        
        #print("move: " + str(move) + ", sample outcomes: " + str(outcomes))

        new_outcomes = [bar[move] if x == 0 else x for x in outcomes]
        _sum = sum(new_outcomes)
        #wins = outcomes.count(1)
        #losses = outcomes.count(-1)
        #draws = outcomes.count(0)

        #move_ratings.append(wins - losses + draws * bar[move])
        move_ratings.append(_sum)
        #print("move: " + str(move) + ", sample outcomes: " + str(new_outcomes))
    print(move_ratings)
    return safe_moves[max(enumerate(move_ratings), key=lambda x: x[1])[0]]


def get_outcome(state: SimpleGameState, player_move: str, max_path_depth: int) -> int:
    """Calculates  the outcome of a random path with an initial player move.
    :param state: SimpleGameState object representing the current game state
    :param player_move: string representing the initial player move
    :param max_path_depth: Maximum depth of the tree search
    :return: 1 for win, -1 for loss, 0 for draw"""
    if max_path_depth <= 0:
        return 0

    depth = 1

    init_opp_move = random_move(state, state.opponent)
    curr_state = state.simulate_moves(player_move, init_opp_move)

    while depth <= max_path_depth:
        if curr_state.is_terminal():
            return curr_state.eval_terminal()
        curr_state = curr_state.simulate_moves(random_move(curr_state, curr_state.player),
                                               random_move(curr_state, curr_state.opponent))
        depth += 1
    return curr_state.eval_terminal()


def random_move(state: SimpleGameState, snake: Snake) -> str:
    """Randomly chooses a safe move if possible.
    :param state: SimpleGameState object representing the current game state
    :param snake: The Snake object to choose a move for
    :return: A random move if possible, "down" otherwise"""
    safe_moves = state.safe_moves(snake)
    # für "morgen": heuristic zeit messen
    #    ValueError: Total of weights must be greater than zero - exception
    if safe_moves == [] or safe_moves is None: # catch exception
        return "down"  # default
    if len(safe_moves) == 1:
        return safe_moves[0]
    else:
        foo = heuristic_2(state, snake)
        weights = [foo[move] for move, probability in foo.items()]
        #print(weights)
        return random.choices(safe_moves, weights=weights)[0]

from alpha_beta.simple_game_state_new import SimpleGameState


def alpha_beta(state: SimpleGameState, cutoff_depth) -> str:
    """Assumes opponent is using same move heuristic as player.
    :param state: initial game state
    :param cutoff_depth: max depth before termination
    :returns: next move (can be {"up", "down", "left", "right"})

    """
    safe_moves = state.safe_moves(state.player)
    min_values = [min_value(state.simulate_moves(safe_move, None), -float('inf'), float('inf'), cutoff_depth) for safe_move in safe_moves]

    #print("moves: " + str(safe_moves))
    #print("min_values: " + str(min_values))

    best_move_index = max(enumerate(min_values), key=lambda x: x[1])[0]
    return safe_moves[best_move_index]

def max_value(state: SimpleGameState, alpha: float, beta: float, depth) -> float:
    """computes value for best move for player
    :param state: current game state
    :param alpha: the value of the best alternative for max() along the path to state
    :param beta: the value of the best alternative for min() along the path to state
    :param depth: depth left before termination
    """
    if state.is_terminal() or depth <= 0:
        return state.eval()
    v = -float('inf')
    for move in state.safe_moves(state.player):
        s = state.copy()
        s.simulate_moves(move, None)

        #print(("\t") * depth + "player move: " + str(move))
        #print(("\t") * depth + "player: " + str(s.player.body))
        #print(("\t") * depth + "opponent: " + str(s.opponent.body))

        v = max(v, min_value(s, alpha, beta, depth-1))

        #print(("\t")*depth + str(v))

        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state: SimpleGameState, alpha: float, beta: float, depth) -> float:
    """computes value for best move for opponent"""
    if state.is_terminal() or depth <= 0:
        return state.eval()
    v = float("inf")
    for move in state.safe_moves(state.opponent):
        s = state.copy()
        s.simulate_moves(None, move)

        #print(("\t") * depth + "opponent move: " + str(move))
        #print(("\t") * depth + "player: " + str(s.player.body))
        #print(("\t") * depth + "opponent: " + str(s.opponent.body))

        v = min(v, max_value(s, alpha, beta, depth - 1))

        #print(("\t") * depth + str(v))

        if v <= alpha:
            return v
        beta = min(beta, v)

    return v
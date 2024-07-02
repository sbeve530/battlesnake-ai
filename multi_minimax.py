from simple_game_state import SimpleGameState

def multi_minimax(max_player_id: str, min_players_ids: [str], depth: int, game_state: SimpleGameState) -> dict:
    moveToMake = 0
    maxMove = float('inf')
    alpha = -float('inf')

    for move in game_state.get_safe_moves(game_state.get_player_index()):
        game_state.next_state(move) # falsche Methode
        minMove = float('inf')
        beta = float('inf')
        for opponent_id in min_players_ids:
            minMove = min(minMove, minimax(max_player_id, opponent_id, depth-1, alpha, beta, game_state, False))
            beta = minMove
            if alpha >= beta:
                break
        if minMove >= maxMove:
            moveToMake = move
            maxMove = minMove
            alpha = maxMove
    return moveToMake


def minimax(max_player_id: str, min_player_id: str, depth: int, alpha: float, beta: float, game_state: SimpleGameState, max):
    player_safe_moves = game_state.get_safe_moves(game_state.get_player_index())
    if depth == 0 or player_safe_moves == []:
        return heuristic(game_state)
    if max:
        max_move = float('-inf')
        for opponent_id in max_player_id.children
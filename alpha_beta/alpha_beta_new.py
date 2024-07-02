from alpha_beta.simple_game_state_new import SimpleGameState


def alpha_beta(state: SimpleGameState, cutoff_depth) -> str:


def max_value(state: SimpleGameState, alpha: float, beta: float, cutoff_depth) -> float:
    if state.is_terminal() or cutoff_depth <= 0:
        return state.eval()
    v = float('-inf')

def min_value(state: SimpleGameState, alpha: float, beta: float) -> float:

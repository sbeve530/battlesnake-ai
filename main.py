# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
# Florian Darsow, 222200974
# Michael Gutbrod, 222201691
# Milan Kai, 222201385
# Jannes Peters, 221201486
# Felix Thiesen, 223202358

import typing
import time
from monte_carlo_tree_search.simple_game_state import SimpleGameState
from monte_carlo_tree_search.mcts import mcts


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Jannes Peters",
        "color": "#0000FF",
        "head": "default",
        "tail": "default",
    }


def start(game_state: typing.Dict):
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    """Calculates the best rated move for the player in a given game state.
    Generates a SimpleGameState object using the received game-state.
    :param game_state: The game state to calculate the move for
    :return: The move with the best evaluated outcome"""
    start = time.time()
    state = SimpleGameState(game_state)
    
    next_move = mcts(state, 5, 16)
    
    end = time.time()
    print("total: " + str((end - start) * 1000) + " ms")
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end
    })

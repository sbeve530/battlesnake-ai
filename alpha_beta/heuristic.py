from typing import Dict
from alpha_beta.simple_game_state_new import SimpleGameState
from alpha_beta.snake import Snake


def heuristic(state: SimpleGameState, snake: Snake) -> Dict[str, float]:
    def distance_to_nearest_food(point: Dict[str, float]) -> int:
        min_dist = float("inf")
        for food in state.foods:
            min_dist = min(min_dist,abs(food["x"]-point["x"]) + abs(food["y"]-point["y"]))
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
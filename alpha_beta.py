from copy import deepcopy
from typing import Dict, List, Tuple
import math
import time


def alpha_beta_decision(game_state: Dict, depth: int) -> Dict:
    if depth < 1:
        return {"move": "down"}
    alpha = -math.inf
    beta = math.inf
    best_move = None
    best_value = -math.inf

    for moves, new_state in successors(game_state):
        value = min_value(new_state, alpha, beta, depth - 1)
        if value > best_value:
            best_value = value
            best_move = moves[0]
    return {"move": best_move} if best_move else {"move": "down"}


def max_value(game_state, alpha, beta, depth) -> float:
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


def min_value(game_state, alpha, beta, depth) -> float:
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


def safe_moves(game_state :Dict, snake: Dict) -> List[str]:
    """Checks if a move would end in the snake dying on next turn

    :param game_state: Game state of the game
    :param snake: Snake state of the game
    :return: List of possible moves
    :type game_state: Dict
    :type snake: Dict
    :rtype: List[str]
    """
    start = time.time()
    possible_moves = [
        "up",
        "down",
        "left",
        "right"
    ]

    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]

    snake_head = snake["body"][0]  # Coordinates of the snake's head
    snakes = game_state["board"]["snakes"]
    other_bodies = [cell for other_snake in snakes for cell in other_snake["body"]]

    # Border checking
    if snake_head["x"] == 0 or {"x": snake_head["x"] - 1, "y": snake_head["y"]} in other_bodies:
        possible_moves.pop(2)
    elif snake_head["x"] == board_width - 1 or {"x": snake_head["x"] + 1, "y": snake_head["y"]} in other_bodies:
        possible_moves.pop(3)
    if snake_head["y"] == 0 or {"x": snake_head["x"], "y": snake_head["y"] - 1} in other_bodies:
        possible_moves.pop(1)
    elif snake_head["y"] == board_height - 1 or {"x": snake_head["x"], "y": snake_head["y"] + 1} in other_bodies:
        possible_moves.pop(0)
    end = time.time()

    print("safe_moves: " + str(end - start))
    return possible_moves

    # Utility function to evaluate game state based on the sum of the inverses of the distances to the food sources


def utility(game_state: Dict) -> float:
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


# Successors function to generate all possible states
def successors(game_state: Dict) -> List[Tuple[str, Dict]]:
    snakes = game_state["board"]["snakes"]
    moves_list = [safe_moves(game_state, snake) for snake in snakes]

    next_states = []

    def generate_states(current_moves, index):
        if index == len(snakes):
            new_state = simulate_moves(game_state, current_moves)
            next_states.append((current_moves, new_state))
            return

        for move in moves_list[index]:
            generate_states(current_moves + [move], index + 1)

    generate_states([], 0)


    return next_states


def simulate_moves(game_state: Dict, moves: List[str]) -> Dict:
    """Simulates a turn and returns the next game state.
        @param game_state {dict} The game state of the game
        @param moves {List[str]} The moves to simulate
        @return {dict} The next game state
    """
    new_state = deepcopy(game_state)
    for i, move in enumerate(moves):
        snake = new_state["board"]["snakes"][i]
        new_state = simulate_move(new_state, snake, move)

    return new_state

type simple_game_state = Tuple["x_size":int, int, List[str], List[Dict[str, int]], Dict]





def simulate_moves_2(game_state: SimpleGameState, moves: List[str]) -> SimpleGameState:
    tmp_state = deepcopy(game_state)
    for i, move in enumerate(moves):
        if move == "up":
            tmp_state.snakes[i].insert(0, {"x": game_state.snakes[i][0]["x"], "y": game_state.snakes[i][0]["y"] + 1})
    return tmp_state


def simulate_move(game_state: Dict, snake: Dict, move: str) -> Dict:
    new_state = deepcopy(game_state)
    snake_copy = deepcopy(snake)
    new_head = deepcopy(snake_copy["body"][0])
    if move == "up":
        new_head["y"] += 1
    elif move == "down":
        new_head["y"] -= 1
    elif move == "left":
        new_head["x"] -= 1
    elif move == "right":
        new_head["x"] += 1

    snake_copy["body"].insert(0, new_head)  # Move head
    snake_copy["body"].pop()  # Remove tail

    for i, existing_snake in enumerate(new_state["board"]["snakes"]):
        if existing_snake["body"][0] == snake["body"][0]:
            new_state["board"]["snakes"][i] = snake_copy
            break

    if game_state["you"]["body"][0] == snake["body"][0]:
        new_state["you"] = snake_copy

    return new_state

def simulate_move2(game_state: Dict, snake_index: int, move: str) -> Dict:
    new_state = deepcopy(game_state)
    new_snake_head = deepcopy(game_state["snakes"][snake_index]["body"][0])
    if move == "up":
        new_snake_head["y"] += 1
    elif move == "down":
        new_snake_head["y"] -= 1
    if move == "left":
        new_snake_head["x"] -= 1
    elif move == "right":
        new_snake_head["x"] += 1

    new_state["board"]["snakes"][snake_index]["body"].insert(0, new_snake_head)
    new_state["board"]["snakes"][snake_index]["head"] = new_snake_head
    if snake_index == 0:
        new_state["you"]["head"] = new_snake_head
    new_state["board"]["snakes"]["you"]["head"] = new_state["you"]["body"][0]
    new_state["board"]["snakes"]["snake"]["body"].pop()


# TODO: Check if the game state is terminal
def is_terminal(game_state: Dict) -> bool:
    return False
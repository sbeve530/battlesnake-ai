import copy
import typing
import math

def alpha_beta_decision(game_state: typing.Dict, depth: int) -> typing.Dict:
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


def safe_moves(game_state: typing.Dict, snake: typing.Dict) -> typing.List[str]:
  is_move_safe = {
    "up": True,
    "down": True,
    "left": True,
    "right": True
  }

  board_width = game_state["board"]["width"]
  board_height = game_state["board"]["height"]

  snake_head = snake["body"][0]  # Coordinates of the snake's head

  # Border checking
  if snake_head["x"] == 0:
    is_move_safe["left"] = False
  if snake_head["x"] == board_width - 1:
    is_move_safe["right"] = False
  if snake_head["y"] == 0:
    is_move_safe["down"] = False
  if snake_head["y"] == board_height - 1:
    is_move_safe["up"] = False

  # Snake and self collision checking
  snakes = game_state["board"]["snakes"]

  for other_snake in snakes:
    snake_body = other_snake["body"]
    if {"x": snake_head["x"] - 1, "y": snake_head["y"]} in snake_body:  # Body left to head, don't move left
      is_move_safe["left"] = False
    if {"x": snake_head["x"] + 1, "y": snake_head["y"]} in snake_body:  # Body right to head, don't move right
      is_move_safe["right"] = False
    if {"x": snake_head["x"], "y": snake_head["y"] - 1} in snake_body:  # Body under head, don't move down
      is_move_safe["down"] = False
    if {"x": snake_head["x"], "y": snake_head["y"] + 1} in snake_body:  # Body above head, don't move up
      is_move_safe["up"] = False

  safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]

  return safe_moves


  # Utility function to evaluate game state based on the sum of the inverses of the distances to the food sources
def utility(game_state: typing.Dict) -> float:
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
def successors(game_state: typing.Dict) -> typing.List[typing.Tuple[str, typing.Dict]]:
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


# Simulate multiple moves for all snakes
def simulate_moves(game_state: typing.Dict, moves: typing.List[str]) -> typing.Dict:
  new_state = copy.deepcopy(game_state)
  for i, move in enumerate(moves):
    snake = new_state["board"]["snakes"][i]
    new_state = simulate_move(new_state, snake, move)

  return new_state


# Simulate move function
def simulate_move(game_state: typing.Dict, snake: typing.Dict, move: str) -> typing.Dict:
  new_state = copy.deepcopy(game_state)
  snake_copy = copy.deepcopy(snake)
  new_head = copy.deepcopy(snake_copy["body"][0])
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


# TODO: Check if the game state is terminal
def is_terminal(game_state: typing.Dict) -> bool:
  return False
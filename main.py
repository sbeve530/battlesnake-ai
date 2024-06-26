# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import copy


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Jannes Peters",  # Your Battlesnake Username
        "color": "#663300",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # prevent Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # prevent Battlesnake from moving out of bounds
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    if my_head["x"] == 0:    # Head is at left boarder, don't move left
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1: # Head is at right boarder, don't move right
        is_move_safe["right"] = False
    if my_head["y"] == 0:    # Head is at bottom boarder, don't move down
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1: # Head is at upper boarder, don't move up
        is_move_safe["up"] = False

    # prevent Battlesnake from colliding with itself
    #my_body = game_state["you"]["body"]
    #if {"x": my_head["x"] - 1, "y": my_head["y"]} in my_body:     # Body left to head, don't move left
    #    is_move_safe["left"] = False
    #if {"x": my_head["x"] + 1, "y": my_head["y"]} in my_body:     # Body right to head, don't move right
    #    is_move_safe["right"] = False
    #if {"x": my_head["x"], "y": my_head["y"] - 1} in my_body:     # Body under to head, don't move down
    #    is_move_safe["down"] = False    
    #if {"x": my_head["x"], "y": my_head["y"] + 1} in my_body:     # Body over to head, don't move up
    #    is_move_safe["up"] = False   

    # prevent Battlesnake from colliding with other Battlesnakes
    snakes = game_state["board"]["snakes"]
    for snake in snakes:
        snake_body = snake["body"]
        if {"x": my_head["x"] - 1, "y": my_head["y"]} in snake_body:     # Body left to head, don't move left
            is_move_safe["left"] = False
        if {"x": my_head["x"] + 1, "y": my_head["y"]} in snake_body:     # Body right to head, don't move right
            is_move_safe["right"] = False
        if {"x": my_head["x"], "y": my_head["y"] - 1} in snake_body:     # Body under to head, don't move down
            is_move_safe["down"] = False
        if {"x": my_head["x"], "y": my_head["y"] + 1} in snake_body:     # Body over to head, don't move up
            is_move_safe["up"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}



    # Choose move 
    
    
    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })

# Rate state (heuristik)
def rate_state(game_state):
    # closer to food is better
    foods = game_state["board"]["food"]
    rating = 0
    for food in foods:
        distance = abs(game_state["you"]["head"]["x"] - food["x"]) + abs(game_state["you"]["head"]["y"] - food["y"])
        rating += 1 / distance
    return rating
        

# Explore next possible States (only for own snake for now)
def explore(game_state):
    possible_states = []
    for move in [{0, 1}, {0, -1}, {-1, 0}, {1, 0}]:
        new_state = copy.deepcopy(game_state)
        new_state["you"]["head"]["x"] += move[0]
        new_state["you"]["head"]["y"] += move[1]
        possible_states.append(new_state)
        
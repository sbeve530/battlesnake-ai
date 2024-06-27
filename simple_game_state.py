from copy import deepcopy


class SimpleGameState:
    """An abstraction of Battlesnakes' Game State Dict and easier work with"""
    def __init__(self, game_state = None):
        if game_state is None:
            return
        self.x_size = game_state["board"]["width"]
        self.y_size = game_state["board"]["height"]
        self.snakes = [snake["body"] for snake in game_state["board"]["snakes"]] # your body is snake with index 0, head is dict in snake body with index 0
        self.foods = [game_state["board"]["food"]]
        self.is_temp = False

    def copy(self):
        new_state = SimpleGameState()
        new_state.x_size = self.x_size
        new_state.y_size = self.y_size
        new_state.snakes = deepcopy(self.snakes)
        new_state.foods = deepcopy(self.foods)
        return new_state

    def get_safe_moves(self, snake_index: int) -> list[str]:
        possible_moves = [
            "up",
            "down",
            "left",
            "right"
        ]
        snake_head = self.snakes[snake_index][0]
        all_snake_bodies = [snake_cell for snake_cell in self.snakes]
        
        if snake_head["x"] == 0 or {"x": snake_head["x"] - 1, "y": snake_head["y"]} in all_snake_bodies:
            possible_moves.pop(2)
        elif snake_head["x"] == self.x_size - 1 or {"x": snake_head["x"] + 1, "y": snake_head["y"]} in all_snake_bodies:
            possible_moves.pop(3)
        if snake_head["y"] == 0 or {"x": snake_head["x"], "y": snake_head["y"] - 1} in all_snake_bodies:
            possible_moves.pop(1)
        elif snake_head["y"] == self.y_size - 1 or {"x": snake_head["x"], "y": snake_head["y"] + 1} in all_snake_bodies:
            possible_moves.pop(0)

        return possible_moves


    def next_move(self, moves:list[str]):
        """Calculates next state given moves for all snakes.
        Returns next state and eliminated snakes (removes eliminated snakes from next state).
        """
        tmp_state = self.copy()

        for i, snake in enumerate(self.snakes):
            if len(tmp_state.get_safe_moves(i)) == 0:
                pass


        for i, move in enumerate(moves):
            if move == "up":
                tmp_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"], "y": self.snakes[i][0]["y"] + 1})
            elif move == "down":
                tmp_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"], "y": self.snakes[i][0]["y"] - 1})
            elif move == "left":
                tmp_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"] - 1, "y": self.snakes[i][0]["y"]})
            elif move == "right":
                tmp_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"] + 1, "y": self.snakes[i][0]["y"]})

        # collision detection




        self.snakes = tmp_state.snakes

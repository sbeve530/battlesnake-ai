from copy import deepcopy


class SimpleGameState:
    """An abstraction of Battlesnakes' Game State Dict and easier work with"""
    def __init__(self, game_state = None):
        if game_state is None:
            return

        self.x_size = game_state["board"]["width"]
        self.y_size = game_state["board"]["height"]
        self.snakes = [[snake["id"], snake["body"]] for snake in game_state["board"]["snakes"]] # head is body with index 0
        self.foods = game_state["board"]["food"]
        self.player = game_state["you"]["id"]
        self.is_temp = False

    def copy(self):
        new_state = SimpleGameState()
        new_state.x_size = self.x_size
        new_state.y_size = self.y_size
        new_state.snakes = deepcopy(self.snakes)
        new_state.foods = deepcopy(self.foods)
        return new_state

    def get_safe_moves(self, snake_index: int) -> list[str]:
        """Returns a list of all  possible moves for a snake
        :param snake_index: Index of the snake to get moves for
        :return: A list of all possible moves for a snake"""
        possible_moves = [
            "up",
            "down",
            "left",
            "right"
        ]
        snake_head = self.snakes[snake_index][0]
        all_snake_bodies = [snake_cell for snake_cells in self.snakes for snake_cell in snake_cells[1]]

        if snake_head["x"] == 0 or {"x": snake_head["x"] - 1, "y": snake_head["y"]} in all_snake_bodies:
            possible_moves.pop(2)
        elif snake_head["x"] == self.x_size - 1 or {"x": snake_head["x"] + 1, "y": snake_head["y"]} in all_snake_bodies:
            possible_moves.pop(3)
        elif snake_head["y"] == 0 or {"x": snake_head["x"], "y": snake_head["y"] - 1} in all_snake_bodies:
            possible_moves.pop(1)
        elif snake_head["y"] == self.y_size - 1 or {"x": snake_head["x"], "y": snake_head["y"] + 1} in all_snake_bodies:
            possible_moves.pop(0)

        return possible_moves


    def next_move(self, moves:list[str]):
        """Calculates next state given moves for all snakes.
        :param moves: A list of moves for all snakes
        :return: new updated state, eliminated snakes
        """
        new_state = self.copy()

        all_safe_moves = [] # safe moves for snakes in initial state
        for i, snake in enumerate(self.snakes):
            all_safe_moves.append(self.get_safe_moves(i))

        # add new heads
        heads = []
        for i, move in enumerate(moves):
            if move == "up":
                new_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"], "y": self.snakes[i][0]["y"] + 1})
                heads.append({"x": self.snakes[i][0]["x"], "y": self.snakes[i][0]["y"] + 1})
            elif move == "down":
                new_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"], "y": self.snakes[i][0]["y"] - 1})
                heads.append({"x": self.snakes[i][0]["x"], "y": self.snakes[i][0]["y"] - 1})
            elif move == "left":
                new_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"] - 1, "y": self.snakes[i][0]["y"]})
                heads.append({"x": self.snakes[i][0]["x"] - 1, "y": self.snakes[i][0]["y"]})
            elif move == "right":
                new_state.snakes[i].insert(0, {"x": self.snakes[i][0]["x"] + 1, "y": self.snakes[i][0]["y"]})
                heads.append({"x": self.snakes[i][0]["x"] + 1, "y": self.snakes[i][0]["y"]})

        # check eliminations
        eliminated_snakes = [] # indices of all eliminated snakes

        for i, snake in enumerate(new_state.snakes):
            if len(all_safe_moves[i]): # check border and body collisions
                eliminated_snakes.append(i)
                break
            #if snake["body"][0] in


        # check food consumptions



        return new_state, eliminated_snakes

    def next_state_2(self, moves: [[str, str]]):
        """Calculates next state given moves for all snakes.
        :param moves: A list of moves for all snakes, e.g. [["id-1", "up"], ["id-2", "down"]]
        :return: if self dies, then empty state, else new state"""
        new_state = self.copy()

        # order snakes by length
        new_state.snakes.sort(key = lambda tup: len(tup[1]), reverse = True)

        # 1. apply moves (add new heads and pop tails)
        for snake in new_state.snakes:
            move = next((move[1] for move in moves if move[0] == snake[0]), "down")
            if move == "up":
                snake[1].insert(0, {"x": snake[1][0]["x"], "y": snake[1][0]["y"] + 1})
                snake[1].pop()
            elif move == "down":
                snake[1].insert(0, {"x": snake[1][0]["x"], "y": snake[1][0]["y"] - 1})
                snake[1].pop()
            elif move == "left":
                snake[1].insert(0, {"x": snake[1][0]["x"] - 1, "y": snake[1][0]["y"]})
                snake[1].pop()
            elif move == "right":
                snake[1].insert(0, {"x": snake[1][0]["x"] + 1, "y": snake[1][0]["y"]})
                snake[1].pop()

        # 2. reduce snake health

        # 3. feed snakes (go through ordered snake list and feed the longest snake, reset health)
        for food in new_state.foods:
            fed_snake = next((snake for snake in new_state.snakes if snake[1][0] == food), None)
            if fed_snake:
                new_state.foods.remove(food)
                # TODO: append tail

        # 4. TODO: elimination (eliminate starved or deserted snakes, check collisions, apply eliminations)

    #def order_snakes(self):
    #    """Sorts snakes by length (descending) to allow for easy feeding later.
    #    """
    #    self.snakes.sort(key = lambda tup: len(tup[1]), reverse = True)

    #def apply_moves(self, moves: [[str, str]]):
    #    """Applies moves to all snakes by creating new head and popping the tail for each snake.
    #    :param moves: A list of moves for all snakes, e.g. [["id-1", "up"], ["id-2", "down"]]"""
    #    for snake in self.snakes:
    #        move = next((move[1] for move in moves if move[0] == snake[0]), "down")
    #        if move == "up":
    #            snake[1].insert(0, {"x": snake[1][0]["x"], "y": snake[1][0]["y"] + 1})
    #            snake[1].pop()
    #        elif move == "down":
    #            snake[1].insert(0, {"x": snake[1][0]["x"], "y": snake[1][0]["y"] - 1})
    #            snake[1].pop()
    #        elif move == "left":
    #            snake[1].insert(0, {"x": snake[1][0]["x"] - 1, "y": snake[1][0]["y"]})
    #            snake[1].pop()
    #        elif move == "right":
    #            snake[1].insert(0, {"x": snake[1][0]["x"] + 1, "y": snake[1][0]["y"]})
    #            snake[1].pop()

from copy import deepcopy


class SimpleGameState:
    """An abstraction of Battlesnakes' Game State Dict and easier work with"""
    def __init__(self, game_state = None):
        if game_state is None:
            return

        self.x_size = game_state["board"]["width"]
        self.y_size = game_state["board"]["height"]
        self.snakes = [[snake["id"], snake["body"], snake["health"]] for snake in game_state["board"]["snakes"]] # head is body with index 0
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

        # original pipeline was the following (due to modularity of the original code):
        #   1. order snakes by length
        #   2. apply moves (add new heads and pop tails)
        #   3. reduce snakes health
        #   4. feed snakes (go through ordered snake list and feed the longest snake, reset health)
        #   5. eliminate snakes (eliminate starved or deserted snakes, check collisions, apply eliminations)
        #
        # the pipeline has been optimized to the following:

        # 1. order snakes by length
        new_state.snakes.sort(key = lambda tup: len(tup[1]), reverse = True)

        # 2. add new heads and reduce health
        for snake in new_state.snakes:
            move = next((move[1] for move in moves if move[0] == snake[0]), "down")
            if move == "up":
                snake[1].insert(0, {"x": snake[1][0]["x"], "y": snake[1][0]["y"] + 1})
                snake[2] -= 1
            elif move == "down":
                snake[1].insert(0, {"x": snake[1][0]["x"], "y": snake[1][0]["y"] - 1})
                snake[2] -= 1
            elif move == "left":
                snake[1].insert(0, {"x": snake[1][0]["x"] - 1, "y": snake[1][0]["y"]})
                snake[2] -= 1
            elif move == "right":
                snake[1].insert(0, {"x": snake[1][0]["x"] + 1, "y": snake[1][0]["y"]})
                snake[2] -= 1

        # 3. feed snakes (go through ordered snake list and feed the longest snake, reset health)
        # and pop tails
        fed_snakes = []
        for food in new_state.foods:
            fed_snake = next((snake for snake in new_state.snakes if snake[1][0] == food), None)
            if fed_snake:
                new_state.foods.remove(food)
                fed_snake[2] = 100
                fed_snakes.append(fed_snake)
        # TODO: possible, but very unlikely scenario: two snakes of same length on same food. No snake should grow and food should persist

        for snake in new_state.snakes:
            if snake not in fed_snakes:
                snake[1].pop()

        # 4. elimination (eliminate starved or deserted snakes, check collisions, apply eliminations)
        eliminated_snakes = [] # contains id's of eliminated snakes
        snake_heads = [[snake[0], snake[1][0], len(snake[1])] for snake in new_state.snakes]  # [id, pos, len]
        for snake in new_state.snakes:
            # out of bound, body and starvation collisions
            snake_head_pos = snake[1][0]
            all_snake_bodies = [snake_cell for snake_cells in new_state.snakes for snake_cell in snake_cells[1][1:]] # without heads

            # eliminate starved
            if (snake[2] <= 0):
                eliminated_snakes.append(snake)
                continue
            # eliminate out of bounds
            elif (snake_head_pos["x"] < 0 or snake_head_pos["x"] > new_state.x_size - 1) or (snake_head_pos["y"] < 0 or snake_head_pos["y"] > new_state.y_size - 1):
                eliminated_snakes.append(snake)
                continue
            # eliminate body collided
            elif (snake_head_pos in all_snake_bodies):
                eliminated_snakes.append(snake)
                continue
            # eliminate head-to-head loosers
            for other_snake in new_state.snakes:
                if snake[0] == other_snake[0]:
                    continue
                if snake[1][0] == other_snake[1][0] and len(snake[1]) <= len(other_snake[1]):
                    eliminated_snakes.append(snake)
                    continue
        for eliminated_snake in eliminated_snakes:
            new_state.snakes.remove(eliminated_snake)

        return new_state

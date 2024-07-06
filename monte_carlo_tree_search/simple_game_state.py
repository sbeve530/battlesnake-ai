from copy import deepcopy
from monte_carlo_tree_search.snake import Snake


class SimpleGameState:
    """A class to simplify the game-state-dict received in a server request and minimizing it to boost performance."""

    def __init__(self, game_state=None):
        if game_state is None:
            return
        self.x_size = game_state["board"]["width"]
        self.y_size = game_state["board"]["height"]
        self.foods = game_state["board"]["food"]
        opponent_index = [index for index, snake in enumerate(game_state["board"]["snakes"]) if
                          snake["id"] != game_state["you"]["id"]][0]
        self.player = Snake(game_state["you"]["id"],
                            game_state["you"]["body"],
                            game_state["you"]["health"],
                            game_state["you"]["head"])
        self.opponent = Snake(game_state["board"]["snakes"][opponent_index]["id"],
                              game_state["board"]["snakes"][opponent_index]["body"],
                              game_state["board"]["snakes"][opponent_index]["health"],
                              game_state["board"]["snakes"][opponent_index]["head"])

    def simulate_moves(self, player_move, opponent_move):
        """Simulates the moves given by player_move and opponent_move and returns the resulting game state.
        :param player_move: player move
        :param opponent_move: opponent move
        :return: a new game state"""
        new_state = self.copy()
        if player_move == None:
            print("choose default")
            player_move = "down"
        if opponent_move == None:
            print("choose default")
            opponent_move = "down"

        # add new heads
        new_state.player.add_new_head(player_move)
        new_state.opponent.add_new_head(opponent_move)

        # reduce health
        new_state.player.reduce_health(1)
        new_state.opponent.reduce_health(1)

        # feed snakes
        player_fed = False
        opponent_fed = False
        for food in new_state.foods:
            if food == new_state.player.head and (
                    food != new_state.opponent.head or len(self.player.body) > len(self.opponent.body)):
                new_state.foods.remove(food)
                new_state.player.reset_health()
                player_fed = True
            if food == new_state.opponent.head and (
                    food != new_state.player.head or len(self.opponent.body) > len(self.player.body)):
                new_state.foods.remove(food)
                new_state.opponent.reset_health()
                opponent_fed = True

        # pop tails of snakes that didn't consume food
        if not player_fed:
            new_state.player.remove_tail()
        if not opponent_fed:
            new_state.opponent.remove_tail()

        # check eliminated and update is_alive
        if (new_state.player.health <= 0) or (
                new_state.player.check_out_of_bounds(new_state.x_size, new_state.y_size)) or (
                new_state.player.check_body_collision(new_state.opponent)) or (
                new_state.player.check_body_collision(new_state.player)) or (
                new_state.player.check_head_to_head_looser(new_state.opponent)):
            new_state.player.is_alive = False

        if (new_state.opponent.health <= 0) or (
                new_state.opponent.check_out_of_bounds(new_state.x_size, new_state.y_size)) or (
                new_state.opponent.check_body_collision(new_state.player)) or (
                new_state.opponent.check_body_collision(new_state.opponent)) or (
                new_state.opponent.check_head_to_head_looser(new_state.player)):
            new_state.opponent.is_alive = False

        return new_state

    def copy(self):
        """:return: A deepcopy of  itself"""
        new_state = SimpleGameState()
        new_state.x_size = self.x_size
        new_state.y_size = self.y_size
        new_state.foods = deepcopy(self.foods)
        new_state.player = deepcopy(self.player)
        new_state.opponent = deepcopy(self.opponent)
        return new_state

    def safe_moves(self, snake: Snake) -> [str]:
        """Returns all possible moves for given snake.
        :param snake: Snake to get moves for (player or opponent)
        :return: all possible moves for given snake, None if no moves are possible"""
        possible_moves = [
            "up",
            "down",
            "left",
            "right"
        ]
        head = snake.head
        bodies = self.player.body + self.opponent.body

        if head["x"] == 0 or {"x": head["x"] - 1, "y": head["y"]} in bodies:
            possible_moves.remove("left")
        if head["x"] == self.x_size - 1 or {"x": head["x"] + 1, "y": head["y"]} in bodies:
            possible_moves.remove("right")
        if head["y"] == 0 or {"x": head["x"], "y": head["y"] - 1} in bodies:
            possible_moves.remove("down")
        if head["y"] == self.y_size - 1 or {"x": head["x"], "y": head["y"] + 1} in bodies:
            possible_moves.remove("up")

        return possible_moves

    def is_terminal(self):
        """Checks if the game state is terminal.
        :return: True if the game state is terminal, False otherwise"""
        if self.player.is_alive == False or self.opponent.is_alive == False:
            return True

    def eval_terminal(self):
        """Evaluates a terminal game state.
        :return: 1 for win, -1 for loss, 0 for draw"""
        if self.player.is_alive == self.opponent.is_alive:
            return 0
        elif self.player.is_alive == False:
            return -1
        else:
            return 1

    def eval(self):
        """Utility function for evaluating a game state.
        :return: the value of the game state"""
        if self.player.is_alive == False:
            return -float('inf')
        if self.opponent.is_alive == False:
            return float('inf')
        if self.player.health == 100:
            return 100
        else:
            return 0

    def print_state(self):
        """Debugging function for printing the game state so that testing can be done locally more easily."""
        board = []
        print("+ " + "- " * self.x_size + "+")
        for y in range(self.y_size):
            row = ['| ']
            for x in range(self.x_size):
                row.append('  ')
            row.append('|')
            board.append(row)

        for s in self.player.body:
            board[s["y"]][s["x"]] = 'x '
        board[self.player.head["y"]][self.player.head["x"]] = 'X '

        for s in self.opponent.body:
            board[s["y"]][s["x"]] = 'o '
        board[self.opponent.head["y"]][self.opponent.head["x"]] = 'O '

        for f in self.foods:
            board[f["y"]][f["x"]] = 'F '

        board.reverse()
        for r in board:
            s = ""
            for c in r:
                s += c
            print(s)
        print("+ " + "- " * self.x_size + "+")

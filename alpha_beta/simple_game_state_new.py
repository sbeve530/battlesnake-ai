from copy import deepcopy

from alpha_beta.snake import Snake


class SimpleGameState:
    def __init__(self, game_state=None):
        if game_state is None:
            return
        self.x_size = game_state["board"]["width"]
        self.y_size = game_state["board"]["height"]
        self.foods = game_state["board"]["food"]
        opponent_index = [index for index, snake in enumerate(game_state["board"]["snakes"]) if
             snake["id"] != game_state["you"]["id"]][0]
        self.player = Snake(game_state["you"]["id"], game_state["you"]["body"], game_state["you"]["health"],
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
            if food == new_state.player.head and (food != new_state.opponent.head or len(self.player.body) > len(self.opponent.body)):
                new_state.foods.remove(food)
                new_state.player.reset_health()
                player_fed = True
            if food == new_state.opponent.head and (food != new_state.player.head or len(self.opponent.body) > len(self.player.body)):
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

    def is_terminal(self):
        """Checks if the game state is terminal.
        :return: True if the game state is terminal, False otherwise"""
        if self.player.is_alive == False or self.opponent.is_alive == False:
            return True
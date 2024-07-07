# Florian Darsow, 222200974
# Michael Gutbrod, 222201691
# Milan Kai, 222201385
# Jannes Peters, 221201486
# Felix Thiesen, 223202358

class Snake:
    """Class for representing snakes on the board. Makes it easier to implement state-simulation.
    Attributes:
        id: id of the snake
        body: all body parts as dict-points (including head)
        head: the head as a dict-point
        health: health-points
        is_alive: attribute used to tell if a snake is alive"""

    def __init__(self, id, body, health, head):
        self.id = id
        self.body = body  # Dict Tuples
        self.health = health
        if self.health > 0:
            self.is_alive = True
        else:
            self.is_alive = False
        if head is None:
            self.head = self.body[0]
        else:
            self.head = head

    def add_new_head(self, move):
        """Adds a new head to the snake according to the move.
        :param move: The move for where to add the head."""
        if not move:
            return

        if move == "left":
            self.head["x"] -= 1
        elif move == "right":
            self.head["x"] += 1
        elif move == "up":
            self.head["y"] += 1
        elif move == "down":
            self.head["y"] -= 1

        self.body.insert(0, self.head.copy())

    def reduce_health(self, amount):
        """Reduces the health of the snake by the given amount.
        :param amount: The amount to reduce the health of the snake."""
        self.health -= amount

    def reset_health(self):
        """Resets the health of the snake to 100."""
        self.health = 100

    def remove_tail(self):
        """Removes the tail of the snake"""
        self.body.pop()

    def check_out_of_bounds(self, x_size, y_size) -> bool:
        """Checks if the snake is out of bounds.
        :param x_size: The x size of the board.
        :param y_size: The y size of the board.
        :return: True if the snake is out of bounds, False otherwise."""
        if self.head["x"] < 0 or self.head["x"] > x_size - 1 or self.head["y"] < 0 or self.head["y"] > y_size - 1:
            return True
        else:
            return False

    def check_body_collision(self, other_snake) -> bool:
        """Checks if self is colliding with the given snake.
        :param other_snake: Snake to check collision with. Can also be self
        :return: True if the snake is colliding with the given snake, False otherwise."""
        if self.head in other_snake.body[1:]:
            return True
        else:
            return False

    def check_head_to_head_looser(self, other_snake) -> bool:
        """Checks if self is loosing head-to-head collision with given snake.
        :param other_snake: Snake to check collision with.
        :return: True if the snake is loosing head-to-head collision, False otherwise."""
        if self.head == other_snake.head and len(self.body) <= len(other_snake.body):
            return True
        else:
            return False

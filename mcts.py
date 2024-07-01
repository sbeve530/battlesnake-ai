import math

from simple_game_state import SimpleGameState


class Node:
    def __init__(self, state: SimpleGameState, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

def ucb1t(node, exploration_param=math.sqrt(2)): # sqrt(2) is a commonly used exploration parameter
    """
    Upper Confidence Bound 1 applied to Trees as derived by Auer, Cesa-Bianchi and Fischer
    """
    if node.visits == 0:
        return math.inf
    return node.wins / node.visits + exploration_param * math.sqrt(math.log(node.parent.visits) / node.visits)
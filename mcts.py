import math
import random

from alpha_beta import is_terminal
from simple_game_state import SimpleGameState


class Node:
    def __init__(self, state: SimpleGameState, parent=None, move_list=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.move_list = move_list


def ucb1t(node, exploration_param=math.sqrt(2)): # sqrt(2) is a commonly used exploration parameter
    """
    Upper Confidence Bound 1 applied to Trees as derived by Auer, Cesa-Bianchi and Fischer
    """
    if node.visits == 0:
        return math.inf
    return node.wins / node.visits + exploration_param * math.sqrt(math.log(node.parent.visits) / node.visits)

def select_node(node):
    while node.children:
        node = max(node.children, key=ucb1t)
    return node

def expand_node(node):
    state = node.state
    player_moves = state.get_safe_moves(state.get_player_index)
    for move in player_moves:
        child_node = Node(state, parent=node, move_list=[move])
        node.children.append(child_node)
    return random.choice(node.children) if node.children else node

def simulate(state: SimpleGameState):
    while not is_terminal(state):


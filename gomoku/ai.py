from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random

class Node:
    """
    A node in the MCTS tree. Each node contains:
    - state: the current state of the game. A tuple of (player, grid) where player is WHITE or BLACK, and grid is 2D list of the board.
    - num_wins: the number of wins for the player of the parent node
    - num_visits: the number of visits to this node
    - parent: the parent node of this node
    - children: a list of child nodes
    - untried_actions: a list of actions that have not been tried yet
    - is_terminal: bool indicating if the game is over
    """
    # NOTE: modifying this block is not recommended
    def __init__(self, state, actions, parent=None):
        self.state = (state[0], copy.deepcopy(state[1]))
        self.num_wins = 0
        self.num_visits = 0
        self.parent = parent
        self.children = [] #store actions and children nodes in the tree as (action, node) tuples
        self.untried_actions = copy.deepcopy(actions)
        simulator = Game(*state)
        self.is_terminal = simulator.game_over

# NOTE: deterministic_test() requires BUDGET = 1000
# You can try higher or lower values to see how the AI's strength changes
BUDGET = 10_000

class AI:
    # NOTE: modifying this block is not recommended because it affects the random number sequences
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state) #using * to unpack the state tuple
        self.root = Node(state, self.simulator.get_actions())

    def mcts_search(self):
        iters = 0
        action_win_rates = {} #store the table of actions and their ucb values

        while iters < BUDGET:
            if (iters + 1) % 100 == 0:
                # NOTE: if your terminal driver doesn't support carriage returns you can use: 
                # print("{}/{}".format(iters + 1, BUDGET))
                print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")

            node = self.select(self.root)
            winner = self.rollout(node)
            self.backpropagate(node, winner)

            iters += 1
        print()

        # Note: Return the best action, and the table of actions and their win values 
        #   For that we simply need to use best_child and set c=0 as return values
        _, action, action_win_rates = self.best_child(self.root, 0)

        return action, action_win_rates

    def select(self, node):
        # NOTE: deterministic_test() requires using c=1 for best_child()

        while not node.is_terminal:
            if node.untried_actions:
                return self.expand(node)
            else:
                node, _, _ = self.best_child(node)

        return node

    def expand(self, node):
        # NOTE: passing the deterministic_test() requires popping an action like this

        action = node.untried_actions.pop(0)
        self.simulator.reset(*node.state)
        self.simulator.place(*action)
        child_node = Node(self.simulator.state(), self.simulator.get_actions(), parent=node)
        node.children.append((action, child_node))

        return child_node

    def best_child(self, node, c=1): 
        best_child_node = None # to store the child node with best UCB
        best_action = None # to store the action that leads to the best child
        action_ucb_table = {} # {action: UCB_value}. We will use this for grading to ensure you are computing UCB correctly.

        # NOTE: deterministic_test() requires iterating in this order
        for action, child in node.children:
            # NOTE: deterministic_test() requires, in the case of a tie, choosing the FIRST action with 
            # the maximum upper confidence bound 
            ucb = (child.num_wins / child.num_visits) + c * (sqrt(2 * log(node.num_visits) / child.num_visits))
            action_ucb_table[action] = ucb
            if best_action == None or ucb > action_ucb_table[best_action]:
                best_action = action
                best_child_node = child

        return best_child_node, best_action, action_ucb_table

    def backpropagate(self, node, result):
        while node is not None:
            node.num_visits += 1
            if node.parent:
                node.num_wins += result[node.parent.state[0]]
            node = node.parent

    def rollout(self, node):
        # NOTE: deterministic_test() requires that you select a random move using self.simulator.rand_move()

        self.simulator.reset(*node.state)
        while not self.simulator.game_over:
            action = self.simulator.rand_move()
            self.simulator.place(*action)

        # Determine reward indicator from result of rollout
        reward = {}
        if self.simulator.winner == BLACK:
            reward[BLACK] = 1
            reward[WHITE] = 0
        elif self.simulator.winner == WHITE:
            reward[BLACK] = 0
            reward[WHITE] = 1
        return reward

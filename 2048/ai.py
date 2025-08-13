from __future__ import absolute_import, division, print_function
import copy, random
from game import Game
import math

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        if not self.children:
            return True
        return False

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    def build_tree(self, node = None, depth = 0):
        # base case
        if node is None:
            node = self.root

        if depth == 0:
            return
        
        # update simulator to current game state before building tree
        self.simulator.set_state(*node.state)

        # if player node create children with all possible player moves
        if node.player_type == MAX_PLAYER:
            for dir in MOVES:
                simboard = Game(*node.state)
                if simboard.move(dir):
                    child = Node(simboard.current_state(), CHANCE_PLAYER)
                    node.children.append((dir, child))
                    self.build_tree(child, depth - 1)
            
        # if chance player create children with all possible boards from
        # adding a single 2 tile
        elif node.player_type == CHANCE_PLAYER:
            potential_moves = self.simulator.get_open_tiles()
            for i, j in potential_moves:
                simboard = Game(*node.state)
                board, score = simboard.current_state()
                board[i][j] = 2
                child = Node((board, score), MAX_PLAYER)
                node.children.append((None, child))
                self.build_tree(child, depth - 1)

    def expectimax(self, node = None):
        if node is None:
            node = self.root

        # base case: return no direction and the score
        if node.is_terminal():
            return (None, node.state[1])
        
        # calculate best direction using score as heuristic
        elif node.player_type == MAX_PLAYER:
            best_value = float('-inf')
            best_direction = None
            for direction, child in node.children:
                _, value = self.expectimax(child)
                if value > best_value:
                    best_value = value
                    best_direction = direction
            return (best_direction, best_value)
        
        # calculate average best average score if chance player
        elif node.player_type == CHANCE_PLAYER:
            value = 0
            for direction, child in node.children:
                value = value + self.expectimax(child)[1] * (1.0 / len(node.children))
            return (None, value)
        
    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax_ec(self.root)
        return direction
    
    def expectimax_ec(self, node = None):
        if node is None:
            node = self.root

        # base case: return no direction and the score
        if node.is_terminal():
            empty_cells = 0
            for i in range(4):
                for j in range(4):
                    if node.state[0][i][j] == 0:
                        empty_cells += 1

            # if empty_cells > 6:
            #     score_weight = 1.7
            # else:
            #     score_weight = 3.7
            return (None, self.snake_hueristic(node.state[0]) * 0.1 + node.state[1] * 1.7)
        # .1, 1.0: 1, 2, 4, 7, 8, 9, 10
        # .1, 1.7: 1, 2, 4, 5, 6, 7, 9, 10
        
        # calculate best direction using score as heuristic
        elif node.player_type == MAX_PLAYER:
            best_value = float('-inf')
            best_direction = None
            for direction, child in node.children:
                _, value = self.expectimax_ec(child)
                if value > best_value:
                    best_value = value
                    best_direction = direction
            return (best_direction, best_value)
        
        # calculate average best average score if chance player
        elif node.player_type == CHANCE_PLAYER:
            value = 0
            for direction, child in node.children:
                value = value + self.expectimax_ec(child)[1] * (1.0 / len(node.children))
            return (None, value)
    
    def snake_hueristic(self, board):
        perfect_snake = [
            [2, 2**2, 2**3, 2**4],
            [2**8, 2**7, 2**6, 2**5],
            [2**9, 2**10, 2**11, 2**12],
            [2**16, 2**15, 2**14, 2**13],
        ]
        h = 0
        board_t = list(zip(*board))
        for i in range(len(board)):
            for j in range(len(board)):
                h += board_t[i][j] * perfect_snake[i][j]

        return h
    
import random
import numpy as np
from Data import Data
from Tree_visualizer import Graph

class MCTS:
    #data: the current state of the game to solve
    #exploration_constant: the constant of the UCT formula. See: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []
        self.visit = 0
        self.value = 0
        self.exploration_constant = 2

    #build tree is the main function of this MCTS algorithm implementation
    #max_iter: the number of simulation of the MCTS. Note: also possible to use a computation time limit
    #game: the game to solve. The two variable a game needs to work with implementation:
    #player => the current player of the state
    #all_next_legal_moves: all next legal moves to build the child nodes. Here the fonction data_mcts() returns them.
    def build_tree(self, max_iter: int, game):
        #first expand the root node
        self.visit = 1
        self.expand(game.data_mcts())
        #Graph.build_graph(self, 0)
        #select => expand => rollout => backpropagation
        for e in range(max_iter):
            selected_node = self.selection()
            rollout_node = selected_node.expand(selected_node.data.game.data_mcts())
            rollout = rollout_node.data.game.rollout(self.children[0].data.player)
            rollout_node.backpropagation(rollout, self.children[0].data.player)
            #Graph.build_graph(self, e + 1) uncomment this line to see the building process of the tree


    #get the best move according to the MCTS
    def best_choice(self):
        value_root_children = [child.value / child.visit for child in self.children]
        return self.children[self.index_max(value_root_children)]

    #select a node based on the UCT formula (computed by the compute_heusristic_search() here)
    def selection(self):
        if self.is_terminal():
            return self
        else:
            result_heuristic_search = []
            for child in self.children:
                result_heuristic_search.append(child.compute_heusristic_search())
            index_children_with_max_heuristic_search = MCTS.index_max(result_heuristic_search)
            return self.children[index_children_with_max_heuristic_search].selection()

    #This implementation uses the standard heuristic function UCT
    def compute_heusristic_search(self):
        if self.visit == 0:
            return np.inf
        average_value = self.value / self.visit
        log_visit_parent_div_visit = np.log(self.parent.visit) / self.visit
        exploration_factor = np.sqrt(log_visit_parent_div_visit) * self.exploration_constant
        uct = average_value + exploration_factor
        return uct

    #expand iff the current as not already been expanded: len(self.children) == 0, has not been visited already
    #self.visit != 0, there are some legal moves ahead: len(data) > 0
    #if expanded, choose a random new children (they are all set with the same value), else return itself because
    #there is no child to return
    def expand(self, data: list):
        if len(self.children) == 0 and self.visit != 0 and len(data) > 0:
            for e in range(len(data)):
                data_child = Data(data[e].player, data[e])
                child = MCTS(data_child)
                child.parent = self
                self.children.append(child)
            return random.choice(self.children)
        return self

    def backpropagation(self, rollout_result, current_player):
        #If the player of the node is the winner of the rollout, positive increment, else negative increment
        if current_player == self.data.player:
            self.value += rollout_result
        else:
            self.value -= rollout_result
        self.visit += 1
        #if self.parent is None it means we are at the root node and the backpropagation stops
        if self.parent is not None:
            self.parent.backpropagation(rollout_result, current_player)

    def is_terminal(self):
        if len(self.children) == 0:
            return True
        return False

    @staticmethod
    def index_max(values):
        max_value = values[0]
        index_max = 0
        for e in range(1, len(values)):
            if values[e] > max_value:
                max_value = values[e]
                index_max = e
        return index_max

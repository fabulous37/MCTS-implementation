import unittest
from MCTS import MCTS
from Data import Data
import copy
from Tictactoe import Tictactoe


class TestMCTS(unittest.TestCase):
    def test_uct(self):
        current_node = MCTS(None)
        current_node.visit = 3
        child = MCTS(None)
        child.parent = current_node
        child.value = 20
        child.visit = 2
        child.exploration_constant = 2
        current_node.children.append(child)
        uct = child.compute_heusristic_search()
        self.assertAlmostEqual(uct, 11.482303807, places=7, msg=None, delta=None)

    def test_selection(self):
        root = MCTS(None)
        root.visit = 3

        child1 = MCTS(None)
        child1.parent = root
        child1.value = 20
        child1.visit = 2
        child1.exploration_constant = 2
        root.children.append(child1)

        child2 = MCTS(None)
        child2.parent = root
        child2.value = 24
        child2.visit = 2
        child2.exploration_constant = 2
        root.children.append(child2)

        child3 = MCTS(None)
        child3.parent = child2
        child3.value = 24
        child3.visit = 2
        child3.exploration_constant = 2
        child2.children.append(child3)

        selected_node = root.selection()

        self.assertEqual(selected_node, child3)

    def test_best_choice(self):
        root = MCTS(None)

        child1 = MCTS(None)
        child1.parent = root
        child1.value = 20
        child1.visit = 2
        child1.exploration_constant = 2
        root.children.append(child1)

        child2 = MCTS(None)
        child2.parent = root
        child2.value = 24
        child2.visit = 2
        child2.exploration_constant = 2
        root.children.append(child2)

        best_node = root.best_choice()

        self.assertEqual(best_node, child2)

    def test_backpropagation(self):
        root = MCTS(Data(1, None))
        root.visit = 3
        root.value = 30

        child1 = MCTS(Data(1, None))
        child1.parent = root
        child1.value = 20
        child1.visit = 2
        root.children.append(child1)

        child2 = MCTS(Data(1, None))
        child2.parent = root
        child2.value = 10
        child2.visit = 1
        root.children.append(child2)

        child3 = MCTS(Data(1, None))
        child3.parent = child2
        child3.value = 0
        child3.visit = 0
        child2.children.append(child3)

        value = 14

        child3.backpropagation(value, 1)

        self.assertEqual(child3.value, 14)
        self.assertEqual(child2.value, 24)
        self.assertEqual(child1.value, 20)
        self.assertEqual(root.value, 44)

        self.assertEqual(child3.visit, 1)
        self.assertEqual(child2.visit, 2)
        self.assertEqual(child1.visit, 2)
        self.assertEqual(root.visit, 4)

    def test_result_1000_games(self):
        res = [0, 0, 0]
        for e in range(1000):
            game = Tictactoe()
            while game.is_game_finished() == -1:
                root = MCTS(Data(game.player, copy.deepcopy(game)))
                root.build_tree(200, game)
                choice = root.best_choice()
                game = copy.deepcopy(choice.data.game)
            res[game.is_game_finished()] += 1
            if e % 100 == 0:
                print(f'Iteration: {e} in test_result_1000_games().')
        self.assertEqual(res[0], 1000)




if __name__ == '__main__':
    unittest.main()

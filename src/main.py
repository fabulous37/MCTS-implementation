import copy
from MCTS import MCTS
from Tictactoe import Tictactoe
from Tree_visualizer import Graph
from Data import Data


if __name__ == '__main__':
    res = [0, 0, 0]
    for e in range(1000):
        game = Tictactoe()
        while game.is_game_finished() == -1:
            root = MCTS(Data(game.player, copy.deepcopy(game)))
            root.build_tree(100, game)
            Graph.build_graph(root, 0)
            choice = root.best_choice()
            game = copy.deepcopy(choice.data.game)
            #game.toString()
        res[game.is_game_finished()] += 1
        game.result_to_string()
    print(f'Player 1: {res[1]} \nPlayer 2: {res[2]} \nDaw: {res[0]}')

"""
GIF generation
from PIL import Image
ims = []
im1 = Image.open('tree_iter0.png')
for e in range(1, 100):
    ims.append(Image.open(f'tree_iter{e}.png'))
im1.save("out.gif", save_all=True, append_images=ims, duration=100, loop=0)
"""
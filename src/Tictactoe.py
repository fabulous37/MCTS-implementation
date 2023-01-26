import copy
import random


class Tictactoe:

    def __init__(self):
        self.board = [[0, 0, 0], [1, 0, 1], [0, 2, 0]]
        self.player = 1

    def player_turn(self, x, y):
        if self.board[x][y] == 0:
            self.board[x][y] = self.player
        else:
            print("Case already played.")

    def is_game_finished(self):
        found_empty_case = False
        for x in range(3):
            if self.board[x][0] == 0 or self.board[x][1] == 0 or self.board[x][2] == 0:
                found_empty_case = True
            if self.board[x][0] != 0 and self.board[x][1] == self.board[x][0] and self.board[x][2] == self.board[x][0]:
                return self.board[x][0]
        for y in range(3):
            if self.board[0][y] != 0 and self.board[1][y] == self.board[0][y] and self.board[2][y] == self.board[0][y]:
                return self.board[0][y]
        if not found_empty_case:
            return 0
        return -1

    def get_legal_moves(self):
        legal_moves = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    legal_moves.append((x, y))
        return legal_moves

    def update_player_index(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def toString(self):
        print("------ Game state ------")
        for x in range(3):
            line = ""
            for y in range(3):
                line += str(self.board[x][y])
            print(line)
        print(f'Current player: {self.player}')

    def data_mcts(self):
        if self.is_game_finished() != -1:
            return []
        legal_moves = self.get_legal_moves()
        data = []
        for e in range(len(legal_moves)):
            data_game = copy.deepcopy(self)
            choice = legal_moves[e]
            data_game.update_player_index()
            data_game.player_turn(choice[0], choice[1])
            data.append(data_game)
        return data

    def rollout(self, root_player):
        rollout_game = copy.deepcopy(self)
        while rollout_game.is_game_finished() == -1:
            possible_choices = rollout_game.get_legal_moves()
            choice = random.choice(possible_choices)
            rollout_game.update_player_index()
            rollout_game.player_turn(choice[0], choice[1])
            rollout_game.is_game_finished()
        if root_player == rollout_game.is_game_finished():
            return 1
        if 0 == rollout_game.is_game_finished():
            return 0
        return -1

    def toString_graph(self):
        line = ""
        for x in range(3):
            for y in range(3):
                line += str(self.board[x][y])
            line += "\n"
        return line

    def result_to_string(self):
        res = self.is_game_finished()
        if res == 0:
            print("*************** \n Draw! \n*************** \n")
        elif res == -1:
            print("*************** \n The game is not finished, let's play! \n*************** \n")
        else:
            print(f'*************** \n Player {res} win! \n*************** \n')


"""
import copy
import random


class Tictactoe:

    def __init__(self):
        self.board = [[0, 0, 0], [1, 0, 1], [0, 2, 0]]
        self.player = 1

    def player_turn(self, x, y):
        if self.board[x][y] == 0:
            self.board[x][y] = self.player
        else:
            print("Case already played.")

    def game_ends(self):
        found_empty_case = False
        for x in range(3):
            if self.board[x][0] == 0 or self.board[x][1] == 0 or self.board[x][2] == 0:
                found_empty_case = True
            if self.board[x][0] != 0 and self.board[x][1] == self.board[x][0] and self.board[x][2] == self.board[x][0]:
                return self.board[x][0]
        for y in range(3):
            if self.board[0][y] != 0 and self.board[1][y] == self.board[0][y] and self.board[2][y] == self.board[0][y]:
                return self.board[0][y]
        if not found_empty_case:
            return 0
        return -1

    def get_legal_moves(self):
        legal_moves = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    legal_moves.append((x, y))
        return legal_moves

    def update_player_index(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def rollout(self, root_player):
        rollout_game = copy.deepcopy(self)
        while rollout_game.game_ends() == -1:
            possible_choices = rollout_game.get_legal_moves()
            choice = random.choice(possible_choices)
            rollout_game.player_turn(choice[0], choice[1])
            rollout_game.update_player_index()
            rollout_game.game_ends()
        if root_player == rollout_game.game_ends():
            return 1
        if 0 == rollout_game.game_ends():
            return 0
        return -1

    def data_mcts(self):
        if self.game_ends() != -1:
            return []
        legal_moves = self.get_legal_moves()
        data = []
        for e in range(len(legal_moves)):
            data_game = copy.deepcopy(self)
            choice = legal_moves[e]
            data_game.board[choice[0]][choice[1]] = self.player
            data_game.update_player_index()
            data.append(data_game)
        return data

    def toString(self):
        print("------ Game state ------")
        for x in range(3):
            line = ""
            for y in range(3):
                line += str(self.board[x][y])
            print(line)

    def toString_graph(self):
        line = ""
        for x in range(3):
            for y in range(3):
                line += str(self.board[x][y])
            line += "\n"
        return line

    def result_to_string(self):
        res = self.game_ends()
        if res == 0:
            print("*************** \n Draw! \n*************** \n")
        elif res == -1:
            print("*************** \n The game is not finished, let's play! \n*************** \n")
        else:
            print(f'*************** \n Player {res} win! \n*************** \n')


"""

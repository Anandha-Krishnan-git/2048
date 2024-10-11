import random
from logic import Game2048

class AI2048:
    def __init__(self, algorithm='expectimax'):
        self.depth = 3
        self.algorithm = algorithm

    def get_best_move(self, game):
        best_score = float('-inf')
        best_move = None
        for move in range(4):
            new_game = self.clone_game(game)
            if new_game.move(move):
                if self.algorithm == 'minimax':
                    score = self.minimax(new_game, self.depth, True)
                else:  # expectimax
                    score = self.expectimax(new_game, self.depth, True)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move if best_move is not None else random.randint(0, 3)

    def minimax(self, game, depth, is_max_player):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game)

        if is_max_player:
            max_score = float('-inf')
            for move in range(4):
                new_game = self.clone_game(game)
                if new_game.move(move):
                    score = self.minimax(new_game, depth - 1, False)
                    max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            empty_cells = [(i, j) for i in range(4) for j in range(4) if game.grid[i][j] == 0]
            for i, j in empty_cells:
                for value in [2, 4]:
                    new_game = self.clone_game(game)
                    new_game.grid[i][j] = value
                    score = self.minimax(new_game, depth - 1, True)
                    min_score = min(min_score, score)
            return min_score

    def expectimax(self, game, depth, is_max_player):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game)

        if is_max_player:
            max_score = float('-inf')
            for move in range(4):
                new_game = self.clone_game(game)
                if new_game.move(move):
                    score = self.expectimax(new_game, depth - 1, False)
                    max_score = max(max_score, score)
            return max_score
        else:
            avg_score = 0
            empty_cells = [(i, j) for i in range(4) for j in range(4) if game.grid[i][j] == 0]
            for i, j in empty_cells:
                for value in [2, 4]:
                    new_game = self.clone_game(game)
                    new_game.grid[i][j] = value
                    prob = 0.9 if value == 2 else 0.1
                    score = self.expectimax(new_game, depth - 1, True)
                    avg_score += prob * score / len(empty_cells)
            return avg_score

    def evaluate(self, game):
        empty_cells = sum(row.count(0) for row in game.grid)
        max_tile = game.get_max_tile()
        smoothness = self.calculate_smoothness(game)
        monotonicity = self.calculate_monotonicity(game)
        
        return (empty_cells * 10) + (max_tile * 2) + smoothness + (monotonicity * 2) + game.score

    def calculate_smoothness(self, game):
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if j < 3 and game.grid[i][j] != 0:
                    smoothness -= abs(game.grid[i][j] - game.grid[i][j+1])
                if i < 3 and game.grid[i][j] != 0:
                    smoothness -= abs(game.grid[i][j] - game.grid[i+1][j])
        return smoothness

    def calculate_monotonicity(self, game):
        monotonicity = 0
        for i in range(4):
            monotonicity += self.direction_monotonicity(game.grid[i])
        for j in range(4):
            column = [game.grid[i][j] for i in range(4)]
            monotonicity += self.direction_monotonicity(column)
        return monotonicity

    def direction_monotonicity(self, line):
        increasing = decreasing = 0
        for i in range(3):
            if line[i] and line[i+1]:
                if line[i] < line[i+1]:
                    increasing += 1
                elif line[i] > line[i+1]:
                    decreasing += 1
        return max(increasing, decreasing)

    def clone_game(self, game):
        new_game = Game2048()
        new_game.grid = [row[:] for row in game.grid]
        new_game.score = game.score
        return new_game
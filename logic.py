import random

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.last_new_tile = None
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            self.last_new_tile = (i, j)

    def move(self, direction):
        # 0: up, 1: right, 2: down, 3: left
        moved = False
        merged = []
        if direction in [0, 2]:  # up or down
            for j in range(4):
                column = [self.grid[i][j] for i in range(4)]
                merged_column, score, merge_positions = self.merge(column if direction == 0 else column[::-1])
                if merged_column != column:
                    moved = True
                    self.score += score
                    for i in range(4):
                        self.grid[i][j] = merged_column[i] if direction == 0 else merged_column[3-i]
                    merged.extend([(i, j) for i in merge_positions])
        else:  # left or right
            for i in range(4):
                row = self.grid[i]
                merged_row, score, merge_positions = self.merge(row if direction == 3 else row[::-1])
                if merged_row != row:
                    moved = True
                    self.score += score
                    self.grid[i] = merged_row if direction == 3 else merged_row[::-1]
                    merged.extend([(i, j) for j in merge_positions])
        
        if moved:
            self.add_new_tile()
        return moved, merged

    def merge(self, line):
        merged = [x for x in line if x != 0]
        score = 0
        merge_positions = []
        i = 0
        while i < len(merged) - 1:
            if merged[i] == merged[i+1]:
                merged[i] *= 2
                score += merged[i]
                merge_positions.append(i)
                merged.pop(i+1)
            i += 1
        merged += [0] * (4 - len(merged))
        return merged, score, merge_positions

    def is_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for i in range(4):
            for j in range(4):
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        return True

    def get_max_tile(self):
        return max(max(row) for row in self.grid)

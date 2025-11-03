from typing import Any
import yaml
import numpy as np
import matplotlib.pyplot as plt
import time



class Game:
    def __init__(self, config):
        self.grid_size = config["grid_size"]
        self.max_steps = config["max_steps"]
        self.visualization_mode = config["visualization"]["mode"]

    def init_grid(self):
        if isinstance(self.grid_size, int):
            grid = np.random.choice([0, 1], size=(self.grid_size, self.grid_size))
        elif isinstance(self.grid_size, tuple) and len(self.grid_size) == 2:
            grid = np.random.choice([0, 1], size=self.grid_size)
        else:
            raise ValueError("Invalid grid size")
        
        return grid

    def start(self):
        print(f"Starting Game of Life with grid size: {self.grid_size}, max steps: {self.max_steps}, visualization mode: {self.visualization_mode}")
        grid = self.init_grid()
        self.visualize(grid)
        for _ in range(self.max_steps):
            grid = self.update_grid(grid)
            self.visualize(grid)

    def visualize(self, grid):
        if self.visualization_mode == "text":
            print(grid)
        elif self.visualization_mode == "graphical":
            plt.imshow(grid, cmap='binary')
            plt.show()
        else:
            raise ValueError("Unknown visualization mode")
        
    def update_grid(self, grid):
        # 1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # 2. Any live cell with two or three live neighbours lives on to the next generation.
        # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        new_grid = grid.copy()
        
        
        return new_grid
    

if __name__ == "__main__":
    config = yaml.safe_load(open("config.yaml", "r"))
    game = Game(config)
    game.start()
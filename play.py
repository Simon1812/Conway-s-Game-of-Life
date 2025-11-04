from typing import Any
import yaml
import numpy as np
import matplotlib.pyplot as plt
import time

class Game:
    def __init__(self, config):
        grid_size = config["grid_size"]
        if isinstance(grid_size, int):
            self.grid_size = (grid_size, grid_size)
        elif isinstance(grid_size, list) and len(grid_size) == 2:
            self.grid_size = (grid_size[0], grid_size[1])
        else:
            raise ValueError("Invalid grid size in config")
        self.alive_char = "███" # config["alive_char"]
        self.dead_char = " ‧ " # config["dead_char"]
        self.max_steps = config["max_steps"]
        self.visualization_mode = config["visualization"]["mode"]
        self.sleep_duration = config["sleep_duration"]

    def init_grid(self):
        tmp = np.zeros((self.grid_size[0]+2, self.grid_size[1]+2), dtype=int)
        grid = np.random.choice([0, 1], size=self.grid_size)
        tmp[1:-1, 1:-1] = grid
        return tmp

    def start(self):
        print(f"Starting Game of Life with grid size: {self.grid_size}, max steps: {self.max_steps}, visualization mode: {self.visualization_mode}")
        grid = self.init_grid()
        self.visualize(grid)
        for _ in range(self.max_steps):
            grid = self.update_grid(grid)
            self.visualize(grid[1:-1, 1:-1])
            time.sleep(0.5)

        plt.show()

    def visualize(self, grid):
        if self.visualization_mode == "text":
            for row in grid:
                print("".join([self.alive_char if cell else self.dead_char for cell in row]))
        elif self.visualization_mode == "graphical":
            plt.imshow(grid, cmap="binary")
            plt.pause(0.05)
        else:
            raise ValueError("Unknown visualization mode")
        
    def update_grid(self, grid):
        # 1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # 2. Any live cell with two or three live neighbours lives on to the next generation.
        # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        new_grid = grid.copy()
        for i in range(1, grid.shape[0]-1):
            for j in range(1, grid.shape[1]-1):
                #neighbours_sum = grid[i-1:i+2, j-1:j+2].sum() - grid[i, j]
                neighbours_sum = 0
                neighbours_sum += grid[(i-1), (j-1)] + grid[(i-1), j] + grid[(i-1), (j+1)]  #top left, center and right neighbours
                neighbours_sum += grid[i, (j-1)]                      + grid[i, (j+1)]      #left and right neighbours
                neighbours_sum += grid[(i+1), (j-1)] + grid[(i+1), j] + grid[(i+1), (j+1)]  #bottom left, center and right neighbours

                
                if grid[i, j] == 1:
                    # rule 1 or rule 3
                    if neighbours_sum < 2 or neighbours_sum > 3:
                        new_grid[i, j] = 0
                    # rule 2 is implicit, no change needed
                else:
                    # rule 4
                    if neighbours_sum == 3:
                        new_grid[i, j] = 1
        
        return new_grid
    
    

if __name__ == "__main__":
    config = yaml.safe_load(open("config.yaml", "r"))
    game = Game(config)
    game.start()
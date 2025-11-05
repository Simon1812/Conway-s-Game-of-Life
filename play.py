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
        self.update_mode = config["update_mode"]
        
        self.initialization_mode = config["initialization_mode"]
        if self.initialization_mode == "random":
            self.alive_cell_probability = config["alive_cell_probability"]
        elif self.initialization_mode == "file":
            self.input_file = config["input_file"]
            
        self.first_run = True
        self.alive_cell_coords = []
    
    def get_input_coordinates_from_console(self):
        """ this Methode gets the alive cells base on user inputs entered in the console

        Returns:
            np.array: the playing grid with the alive cells set by the user
        """
        print("Input the alive cells in the format: x1,y1 or [x1,y1,x2,y2,.....] or \"done\" to finish")
        coords = []
        while True:
            input_str = input("Enter coordinates: ")
            if input_str.lower() == "done":
                break
            try:
                if "[" in input_str and "]" in input_str:
                    tmp_coords = []
                    parts = input_str.strip("[]").split(",")
                    for i in range(0, len(parts), 2):
                        x, y = int(parts[i]), int(parts[i+1])
                        # use tmp_coords to avoid modifying coords while iterating
                        # it is possible that later inputs are invalid
                        # => only modify coords if all inputs are valid
                        tmp_coords.append((x, y))
                    coords.extend(tmp_coords)
                elif "," in input_str:
                    x, y = input_str.split(",")
                    coords.append((int(x), int(y)))
                else:
                    print("Invalid input format")
            except Exception as e:
                print(f"Error parsing input: {e}")
        grid = np.zeros(self.grid_size, dtype=int)
        for x, y in coords:
            if 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]:
                grid[y, x] = 1
            else:
                print(f"Coordinates ({x},{y}) are outside the boundaries of the grid")
        return grid
                    
    def init_grid(self):
        """ this Methode initializes the playing grid based on the configuration file

        Raises:
            ValueError: if the initialization mode is not supported

        Returns:
            np.array: the initial playing grid
        """
        grid = np.zeros((self.grid_size[0]+2, self.grid_size[1]+2), dtype=int)
        if self.initialization_mode == "file":
            playgrid = np.load(self.input_file)
        elif self.initialization_mode == "input":
            playgrid = self.get_input_coordinates_from_console()
        elif self.initialization_mode == "random":
            probabilities = [1 - self.alive_cell_probability, self.alive_cell_probability]
            playgrid = np.random.choice([0, 1], size=self.grid_size, p=probabilities)
        else:
            raise ValueError(f"Initialization mode {self.initialization_mode} is not supported")
        
        grid[1:-1, 1:-1] = playgrid
        return grid

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
        """ This Methode visualizes the current playing grid

        Args:
            grid (np.array): the current playing grid

        Raises:
            ValueError: if the visualization mode is unknown
        """
        if self.visualization_mode == "text":
            for row in grid:
                print("".join([self.alive_char if cell else self.dead_char for cell in row]))
        elif self.visualization_mode == "graphical":
            plt.imshow(grid, cmap="binary")
            plt.pause(0.05)
        elif self.visualization_mode == "none":
            return
        else:
            raise ValueError("Unknown visualization mode")
     
    def get_neighbour_sum(self, grid, x, y):
        """ This Methode calculates the sum of alive neighbours for a given cell

        Args:
            grid (np.array): the current playing grid
            x (int): the x coordinate of the cell
            y (int): the y coordinate of the cell
        Returns:  
            (int): the sum of all alive neighbours
        """
        
        neighbours_sum = 0
        # numpy arrays are accessed as [height, width] => [y,x]
        neighbours_sum += grid[(y-1), (x-1)] + grid[(y-1), x] + grid[(y-1), (x+1)]  #top left, center and right neighbours
        neighbours_sum += grid[y, (x-1)]                      + grid[y, (x+1)]      #left and right neighbours
        neighbours_sum += grid[(y+1), (x-1)] + grid[(y+1), x] + grid[(y+1), (x+1)]  #bottom left, center and right neighbours

        return neighbours_sum
        
    def update_cell_state(self, old_grid, new_grid, x, y, neighbours_sum):
        """ this methodes updates one cell based on the sum of alive neighbours and the game Rule

        Args:
            old_grid (np.array): the current playing grid
            new_grid (np.array): the playing grid after this evaluation step
            x (int): the x coordinate of the cell
            y (int): the y coordinate of the cell
            neighbours_sum (int): number of alive neighbours
        """
        # 1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # 2. Any live cell with two or three live neighbours lives on to the next generation.
        # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        
        if old_grid[y, x] == 1:
            # rule 1 or rule 3
            if neighbours_sum < 2 or neighbours_sum > 3:
                new_grid[y, x] = 0
            else:
                self.alive_cell_coords.append((x, y))
                
            # rule 2 is implicit, no change needed
        else:
            # rule 4
            if neighbours_sum == 3:
                new_grid[y, x] = 1
                self.alive_cell_coords.append((x, y))
        
        
    def update_grid(self, grid):
        """ This Methode makes one evaluation step

        Args:
            grid (np.array): the current playing grid

        Raises:
            ValueError: if the update mode is unknown

        Returns:
            np.array: the updated playing grid
        """      
        new_grid = grid.copy()
        
        if self.update_mode == "alive_based":
            # get the coordinates of all alive cells only once
            if self.first_run:
                self.first_run = False
                for y in range(1, grid.shape[0]-1): #height
                    for x in range(1, grid.shape[1]-1): #width
                        # numpy arrays are accessed as [height, width] => [y,x]
                        if grid[y, x] == 1:
                            self.alive_cell_coords.append((x, y))

            # Collect all neighboring coordinates of alive cells
            if len(self.alive_cell_coords) > 0:
                coords_to_check = set()
                for coord in self.alive_cell_coords:
                    x, y = coord
                    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                        new_X, new_Y = x + dx, y + dy
                        if 0 < new_X < grid.shape[1]-1 and 0 < new_Y < grid.shape[0]-1:
                            # coordinates need to be in the initial grid boundaries
                            if (new_X, new_Y) not in coords_to_check:
                                coords_to_check.add((new_X, new_Y))
                    if (x, y) not in coords_to_check:
                        coords_to_check.add((x, y))  # also check the cell itself
                           
                self.alive_cell_coords = []  # reset for the next iteration
                for x, y in coords_to_check:
                    neighbours_sum = self.get_neighbour_sum(grid, x, y)
                    self.update_cell_state(grid, new_grid, x, y, neighbours_sum)   

        elif self.update_mode == "all":
            # iterate over all cells
            for y in range(1, grid.shape[0]-1): #height
                for x in range(1, grid.shape[1]-1): #width
                    neighbours_sum = self.get_neighbour_sum(grid, x, y)
                    self.update_cell_state(grid, new_grid, x, y, neighbours_sum)
        else:
            raise ValueError(f"Update mode {self.update_mode} is not supported")
        
        return new_grid
    
    

if __name__ == "__main__":
    config = yaml.safe_load(open("config.yaml", "r"))
    game = Game(config)
    game.start()
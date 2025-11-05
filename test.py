import numpy as np
from play import Game
import yaml
import unittest


class testgame(unittest.TestCase):
    def setUp(self):
        with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
        self.game = Game(config)
            
            
    def test_setup(self):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.game = Game(config)
        self.assertIsInstance(self.game, Game)
    
    def test_update_grid1(self):
        # Test case create block pattern
        initial_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0]])
        
        expected_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 0],
                                  [0, 1, 1, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0]])
        updated_grid = self.game.update_grid(initial_grid)
        np.testing.assert_array_equal(updated_grid, expected_grid)
    
    def test_update_grid2(self):
        # Test case with death by underpopulation, death by overpopulation, and reproduction
        grid =np.zeros((7,7))
        initial_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 1, 1, 1, 0],
                                  [0, 0, 1, 1, 0],
                                  [0, 1, 0, 1, 0],
                                  [0, 0, 0, 0, 0]])
        
        expected_grid = np.array([[0, 0, 1, 0, 0],
                                  [0, 1, 0, 1, 0],
                                  [0, 0, 0, 0, 1],
                                  [0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0]])
        grid[1:-1, 1:-1] = initial_grid
        updated_grid = self.game.update_grid(grid)
        np.testing.assert_array_equal(updated_grid[1:-1, 1:-1], expected_grid)
    
    def test_update_grid3(self):
        # Test cell death by underpopulation
        grid =np.zeros((7,7))
        initial_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0]])
        
        expected_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0]])
        grid[1:-1, 1:-1] = initial_grid
        updated_grid = self.game.update_grid(grid)
        np.testing.assert_array_equal(updated_grid[1:-1, 1:-1], expected_grid)

    def test_update_grid3(self):
        # Test still life Tub pattern
        grid =np.zeros((7,7))
        initial_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 1, 0, 1, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0]])
        
        expected_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 1, 0, 1, 0],
                                  [0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0]])
        grid[1:-1, 1:-1] = initial_grid
        updated_grid = self.game.update_grid(grid)
        np.testing.assert_array_equal(updated_grid[1:-1, 1:-1], expected_grid)
        updated_grid = self.game.update_grid(updated_grid)
        np.testing.assert_array_equal(updated_grid[1:-1, 1:-1], expected_grid)

    def test_update_grid4(self):
        # Test Oscillators Beacon (period 2)
        grid =np.zeros((7,7))
        initial_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 0],
                                  [0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 1],
                                  [0, 0, 0, 1, 1]])
        
        expected_grid = np.array([[0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 0],
                                  [0, 1, 1, 0, 0],
                                  [0, 0, 0, 1, 1],
                                  [0, 0, 0, 1, 1]])
        grid[1:-1, 1:-1] = initial_grid
        updated_grid = self.game.update_grid(grid)
        np.testing.assert_array_equal(updated_grid[1:-1, 1:-1], expected_grid)
        updated_grid = self.game.update_grid(updated_grid)
        np.testing.assert_array_equal(updated_grid[1:-1, 1:-1], grid[1:-1, 1:-1])


if __name__ == "__main__": 
    unittest.main()
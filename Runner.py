from Algorithms.golGenerator import gol
import numpy as np

if __name__ == '__main__':
    # Set the current working dir to grids > gol
    cwd = 'grids\gol'

    rows = 75
    cols = 75
    
    grid = np.random.choice(a = [True, False], size = (rows, cols))
    
    golObj = gol(startGrid = grid, generations = 30, cwd = cwd)

    golObj.start()
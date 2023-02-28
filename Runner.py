from Algorithms.golGenerator import gol
import numpy as np
import sys
import os

if __name__ == '__main__':
    # Set the current working dir to grids > gol
    cwd = sys.path[0]
    fPath = os.path.join(cwd, 'grids', 'gol')

    rows = 200
    cols = 200
    
    grid = np.random.choice(a = [True, False], size = (rows, cols))
    
    golObj = gol(startGrid = grid, generations = 30, cwd = fPath)

    golObj.start()
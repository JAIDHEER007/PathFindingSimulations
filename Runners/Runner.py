import sys
import os
import pandas as pd
import numpy as np

# Defining the current working directory 
cwd = sys.path[0]

# Adding the previous folder to sys.path to import the required modules
sys.path.append(os.path.join(cwd, '..'))

from Helpers import helper
# from Helpers import ImageGenerator
from Helpers import VideoGenerator_v2

from GridCollection import Grid1

from Algorithms import isValid
from Algorithms import recursive_backtracker

import Links

from copy import deepcopy

sys.setrecursionlimit(10**5)


# Redundant Code
# Path to a foldercontaining the csv files
# csvStatesPath = os.path.join(cwd, '..', 'csvStates')

# CSV File Name
# csvFileName = 'State175_13.csv'

# This Contains the final path to the csv file
# csvFilePath = os.path.join(csvStatesPath, csvFileName)

# Online Link can also be provided
csvFilePath = Links.state_75_75_17_1

# Reading the csv file
# initialState = pd.read_csv(csvFilePath, header=None, dtype=int).to_numpy()
# print('Read the CSV')

shape = (201, 201)
initialState = np.zeros(shape = shape, dtype=int)

# Final File Path 
fPath = helper.createFolder(os.path.join(cwd, '..', 'TestRuns'), initialState, directories = ["Images", "Videos"])

gridObj = Grid1(initialState)

runnerObject = recursive_backtracker(grid=gridObj)
runnerObject.start()

print('Completed Maze Generation')

gridObj.saveStateMatrix(fPath=fPath)

for i in range(shape[0]):
  for j in range(shape[1]):
    gridState = gridObj.get(coordinates = (i, j))
    if gridState == 4: 
      gridObj.set(coordinates = (i, j), value = 0)

gridObj.saveGrid(fPath = fPath)



for zoomFactor in [3]:
  VideoGenerator_v2.saveVideo(fPath = fPath, fps = 300, stateMatrix = gridObj.stateMatrix(), 
                              zoomFactor = zoomFactor, videoName = f"Output_z{zoomFactor}")
  print("Video Generated")





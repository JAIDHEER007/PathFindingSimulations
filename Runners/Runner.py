import sys
import os
import pandas as pd

# Defining the current working directory 
cwd = sys.path[0]

# Adding the previous folder to sys.path to import the required modules
sys.path.append(os.path.join(cwd, '..'))

from Helpers import helper
# from Helpers import ImageGenerator
from Helpers import VideoGenerator_v2

from GridCollection import Grid1

from Algorithms import isValid
from Algorithms import BFS

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
# csvFilePath = Links.state_75_75_17_1
csvFilePath = 'grid_151_151.csv'

# Reading the csv file
initialState = pd.read_csv(csvFilePath, header=None, dtype=int).to_numpy()
print('Read the CSV')

# Final File Path 
savePath = '/content/drive/MyDrive/PathFindingSimulations'
fPath = helper.createFolder(os.path.join(savePath, 'TestRuns'), initialState, directories = ["Images", "Videos"])

# Creating the grid object
grid = Grid1(npgrid = initialState)

# Set the Starting Location
startingLocation = (1, 1)

# Set the ending Location
endingLocation = (149, 149)

if not isValid(grid.getShape(), startingLocation):
  raise Exception("Starting Location Outside the grid")
if not isValid(grid.getShape(), endingLocation):
  raise Exception("Ending Location Outside the grid")

# Setting the starting Location
grid.set(startingLocation, 2)
grid.set(endingLocation, 3)

bfsObject = BFS(grid, startingLocation, corners = False, backtracking = True)

assert endingLocation == bfsObject.start()
print("Found the ending Location")


# for zoomFactor in [11]:
#   VideoGenerator_v2.saveVideo(fPath = fPath, fps = 200, stateMatrix = grid.stateMatrix(), 
#                               zoomFactor = zoomFactor, videoName = f"Output_z{zoomFactor}")
#   print("Video Generated")





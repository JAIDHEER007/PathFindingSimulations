from functools import cached_property
import numpy as np
import os

class Grid1:
    def __init__(self, npgrid):
      self.__npgrid = npgrid 
      self.__stateMatrix = []

    def get(self, coordinates):
      return self.__npgrid[coordinates]

    def set(self, coordinates, value):
      self.__npgrid[coordinates] = value
      self.__stateMatrix.append((coordinates, value))
    
    def stateMatrix(self):
      # Coloring the start coordinate to same color even if it gets visited
      coordinate = None
      for i in range(len(self.__stateMatrix)):
        if self.__stateMatrix[i][1] == 2:
          coordinate = self.__stateMatrix[i][0]
        elif self.__stateMatrix[i][0] == coordinate:
          self.__stateMatrix[i] = (coordinate, 2)
      return self.__stateMatrix
    
    def saveStateMatrix(self, fPath):
      # stateMatrix = [[state[0][0], state[0][1], state[1]] for state in self.__stateMatrix]
      np.savetxt(fname = os.path.join(fPath, 'stateMatrix.csv'), 
                   X = [[state[0][0], state[0][1], state[1]] for state in self.__stateMatrix], 
                   delimiter = ',', fmt='%d')

      
    # @cached_property
    def getShape(self): 
      return self.__npgrid.shape
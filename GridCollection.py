from functools import cached_property

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
      return self.__stateMatrix
      
    # @cached_property
    def getShape(self): 
      return self.__npgrid.shape
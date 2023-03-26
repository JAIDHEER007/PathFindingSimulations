import random

directionLambdas = [
  lambda x, y: (x + 0, y + 1),  # right
  lambda x, y: (x + 1, y + 0),  # bottom
  lambda x, y: (x + 0, y - 1),  # left
  lambda x, y: (x - 1, y + 0),  # top
  lambda x, y: (x - 1, y + 1),  # top-right
  lambda x, y: (x + 1, y + 1),  # bottom-right 
  lambda x, y: (x + 1, y - 1),  # bottom-left
  lambda x, y: (x - 1, y - 1),  # top-left
]

directionLambdas2 = [
  lambda x, y: (x + 0, y + 2),  # right
  lambda x, y: (x + 2, y + 0),  # bottom
  lambda x, y: (x + 0, y - 2),  # left
  lambda x, y: (x - 2, y + 0),  # top
  lambda x, y: (x - 2, y + 2),  # top-right
  lambda x, y: (x + 2, y + 2),  # bottom-right 
  lambda x, y: (x + 2, y - 2),  # bottom-left
  lambda x, y: (x - 2, y - 2),  # top-left
]

# A Function to check if the point of interest is inside or outside the grid
def isValid(shape, coordinates) -> bool:
    rows, cols = shape
    i, j = coordinates
    return (i >= 0) and (i < rows) and (j >= 0) and (j < cols)

# Depth First Search
class DFS:
  def __init__(self, grid, startCoordinates, corners = False, backtracking = False):
    self.__grid = grid
    self.__startCoordinates = startCoordinates
    self.__endCoordinates = None
    self.__corners = corners
    self.__backtracking = backtracking
  
  def __recur(self, coordinates):
    # If the coordinates are out of maze then return false
    if not isValid(self.__grid.getShape(), coordinates): return False

    # Get the self.__grid state
    gridState = self.__grid.get(coordinates)

    # Check if the coordinates are end point
    if gridState == 3:
        self.__endCoordinates = coordinates

        # Setting the backtracking corner as orange
        if self.__backtracking:
          self.__grid.set(coordinates, 5)
        
        return True

    # if the coordinates are representing a wall then return False
    if gridState == 1: return False

    # if the coordinates are previously visited then return False
    if gridState == 4: return False

    # Now make the element at specified coordinates visited
    self.__grid.set(coordinates, 4)

    # Traverse the grid
    for directionLambda in directionLambdas[:8 if self.__corners else 4]:
      if self.__recur(directionLambda(*coordinates)):
        
        # Setting the backtracking corner as orange
        if self.__backtracking:
          self.__grid.set(coordinates, 5)
        
        return True
      
    return False
  
  def start(self):
    self.__recur(self.__startCoordinates)
    return self.__endCoordinates

# Breadth First Search
class BFS:
  def __init__(self, grid, startCoordinates, corners = False, backtracking = False):
    self.__grid = grid
    self.__startCoordinates = startCoordinates
    self.__endCoordinates = None
    self.__corners = corners
    self.__backtracking = backtracking

  def __traverse(self, startCoordinates):
    # Queue to perform Queue operations in BFS
    queue = []

    # PrevHash to store the previous node of the current node
    prev = {}

    # Initially store the starting coordinates in the queue
    queue.append(startCoordinates)

    prev[startCoordinates] = (-1, -1)

    # Run the loop until the queue is empty 
    while len(queue) > 0:

      # Pop the first element and work on it
      top = queue.pop(0)

      # If the coordinates are out of maze then return false
      if not isValid(self.__grid.getShape(), top): 
        prev.pop(top, None)
        continue

      # Get the self.__grid state
      gridState = self.__grid.get(top)

      # Check if the coordinates are end point
      if gridState == 3:
        self.__endCoordinates = top
        break

      # if the coordinates are representing a wall then return False
      if gridState == 1: 
        prev.pop(top, None)
        continue

      # if the coordinates are previously visited then return False
      if gridState == 4: 
        # prev.pop(top, None)
        continue

      # Now make the element at specified coordinates visited
      self.__grid.set(top, 4)

      # Traverse the grid
      for directionLambda in directionLambdas[:8 if self.__corners else 4]:
        newCoordinates = directionLambda(*top)
        queue.append(newCoordinates)

        if newCoordinates not in prev:
          prev[newCoordinates] = top

    if self.__endCoordinates is not None and self.__backtracking:
      currCordinate = self.__endCoordinates
      while(currCordinate != (-1, -1)):
        self.__grid.set(currCordinate, 5)
        currCordinate = prev[currCordinate]


  def start(self):
    self.__traverse(self.__startCoordinates)
    return self.__endCoordinates

class recursive_backtracker:
  def __init__(self, grid, corners = False):
    self.__grid = grid
    self.__corners = corners

  def __recur(self, coordinates):
    # If the coordinates are out of maze then return false
    if not isValid(self.__grid.getShape(), coordinates): return False

    # Get the self.__grid state
    gridState = self.__grid.get(coordinates)

    # if the coordinates are representing a wall then return False
    if gridState == 1: return False

    # if the coordinates are previously visited then return False
    if gridState == 4: return False

    # Now make the element at specified coordinates visited
    self.__grid.set(coordinates, 4)

    for directionIndex in random.sample(list(range(8)), 8):
      if self.__recur(directionLambdas2[directionIndex](*coordinates)):
        self.__grid.set(directionLambdas[directionIndex](*coordinates), 4)

    return True


  def start(self):
    gridShape = self.__grid.getShape()
    lambdaIndex, startFlag = 0, True
    coordinates = (0, 0)
    while (coordinates != (0, 0)) or startFlag:
      # The loop started. Make the start flag as false
      startFlag = False

      # Set the grid location as wall
      self.__grid.set(coordinates, 1)

      # Calculate the new coordinates
      newCoordinates = directionLambdas[lambdaIndex](*coordinates)

      # Check if the new coordinate is valid or not
      # if not valid move to next direction lambda and re calculate the grid
      if not isValid(gridShape, newCoordinates):
        lambdaIndex += 1
        newCoordinates = directionLambdas[lambdaIndex](*coordinates)

      coordinates = newCoordinates
    
    # Creating the cross walls
    vwCoordinates, hwCoordinates = (0,2), (2,0)
    while True:
      vwFlag, hwFlag = False, False
      if vwFlag := isValid(gridShape, vwCoordinates):
        coordinates = vwCoordinates
        while isValid(gridShape, coordinates):
          self.__grid.set(coordinates, 1)
          coordinates = directionLambdas[1](*coordinates)
        vwCoordinates = directionLambdas2[0](*vwCoordinates)
      if hwFlag := isValid(gridShape, hwCoordinates):
        coordinates = hwCoordinates
        while isValid(gridShape, coordinates):
          self.__grid.set(coordinates, 1)
          coordinates = directionLambdas[0](*coordinates)
        hwCoordinates = directionLambdas2[1](*hwCoordinates)

      if not (vwFlag or hwFlag):
        break

    startCoordinates = (0, 0)
    while self.__grid.get(startCoordinates) != 0:
      startCoordinates = (random.randrange(gridShape[0]), random.randrange(gridShape[1]))

    print(startCoordinates)
    self.__recur(startCoordinates)

class Runner:
  def create(algorithm, kwargs):
    if algorithm == 'DFS':
      return DFS(grid = kwargs['grid'], 
                 startCoordinates = kwargs['startCoordinates'], 
                 corners = kwargs['corners'], 
                 backtracking = kwargs['backtracking'])
    elif algorithm == 'BFS':
      return BFS(grid = kwargs['grid'], 
                 startCoordinates = kwargs['startCoordinates'], 
                 corners = kwargs['corners'], 
                 backtracking = kwargs['backtracking'])
      

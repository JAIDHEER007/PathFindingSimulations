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
      

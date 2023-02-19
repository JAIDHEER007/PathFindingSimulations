# A Function to check if the point of interest is inside or outside the grid
def isValid(shape, coordinates) -> bool:
    rows, cols = shape
    i, j = coordinates
    return (i >= 0) and (i < rows) and (j >= 0) and (j < cols)

class dfs:
    def __init__(self, grid, startCoordinates):
        self.__grid = grid
        self.__startCoordinates = startCoordinates
        self.__endCoordinates = None
    
    def __recur(self, coordinates):
        # If the coordinates are out of maze then return false
        if not isValid(self.__grid.getShape(), coordinates): return False

        # Get the self.__grid state
        gridState = self.__grid.get(coordinates)

        # Check if the coordinates are end point
        if gridState == 3:
            self.__endCoordinates = coordinates
            return True

        # if the coordinates are representing a wall then return False
        if gridState == 1: return False

        # if the coordinates are previously visited then return False
        if gridState == 4: return False

        # Now make the element at specified coordinates visited
        self.__grid.set(coordinates, 4)

        # Traverse the grid in 4 directions
        
        #left 
        if self.__recur((coordinates[0] + 0, coordinates[1] + 1)): return True

        # right
        if self.__recur((coordinates[0] + 0, coordinates[1] - 1)): return True
        
        # up
        if self.__recur((coordinates[0] + 1, coordinates[1] + 0)): return True
        
        # down
        if self.__recur((coordinates[0] - 1, coordinates[1] + 0)): return True

        return False
    
    def start(self):
        self.__recur(self.__startCoordinates)
        return self.__endCoordinates

class dfs_corner:
    def __init__(self, grid, startCoordinates):
        self.__grid = grid
        self.__startCoordinates = startCoordinates
        self.__endCoordinates = None
    
    def __recur(self, coordinates):
        # If the coordinates are out of maze then return false
        if not isValid(self.__grid.getShape(), coordinates): return False

        # Get the self.__grid state
        gridState = self.__grid.get(coordinates)

        # Check if the coordinates are end point
        if gridState == 3:
            self.__endCoordinates = coordinates
            return True

        # if the coordinates are representing a wall then return False
        if gridState == 1: return False

        # if the coordinates are previously visited then return False
        if gridState == 4: return False

        # Now make the element at specified coordinates visited
        self.__grid.set(coordinates, 4)

        # Traverse the grid in 4 directions
        
        #left 
        if self.__recur((coordinates[0] + 0, coordinates[1] + 1)): return True

        # right
        if self.__recur((coordinates[0] + 0, coordinates[1] - 1)): return True
        
        # up
        if self.__recur((coordinates[0] + 1, coordinates[1] + 0)): return True
        
        # down
        if self.__recur((coordinates[0] - 1, coordinates[1] + 0)): return True

        # top-left 
        if self.__recur((coordinates[0] + 1, coordinates[1] + 1)): return True

        # top-right
        if self.__recur((coordinates[0] + 1, coordinates[1] - 1)): return True
        
        # bottom-left 
        if self.__recur((coordinates[0] - 1, coordinates[1] + 1)): return True

        # bottom-right
        if self.__recur((coordinates[0] - 1, coordinates[1] - 1)): return True

        return False


    def start(self):
        self.__recur(self.__startCoordinates)
        return self.__endCoordinates

class dfs_backtracking:
  def __init__(self, grid, startCoordinates):
    self.__grid = grid
    self.__startCoordinates = startCoordinates
    self.__endCoordinates = None
    
  def __recur(self, coordinates):
    # If the coordinates are out of maze then return false
    if not isValid(self.__grid.getShape(), coordinates): return False

    # Get the self.__grid state
    gridState = self.__grid.get(coordinates)

    # Check if the coordinates are end point
    if gridState == 3:
        self.__endCoordinates = coordinates

        # Setting the backtracking corner as orange
        self.__grid.set(coordinates, 5)
        return True

    # if the coordinates are representing a wall then return False
    if gridState == 1: return False

    # if the coordinates are previously visited then return False
    if gridState == 4: return False

    # Now make the element at specified coordinates visited
    self.__grid.set(coordinates, 4)

    # Traverse the grid in 4 directions
    
    #left 
    if self.__recur((coordinates[0] + 0, coordinates[1] + 1)): 
      self.__grid.set(coordinates, 5)
      return True

    # right
    if self.__recur((coordinates[0] + 0, coordinates[1] - 1)): 
      self.__grid.set(coordinates, 5)
      return True
    
    # up
    if self.__recur((coordinates[0] + 1, coordinates[1] + 0)): 
      self.__grid.set(coordinates, 5)
      return True
    
    # down
    if self.__recur((coordinates[0] - 1, coordinates[1] + 0)): 
      self.__grid.set(coordinates, 5)
      return True

    return False

  def start(self):
      self.__recur(self.__startCoordinates)
      return self.__endCoordinates

class bfs:
  def __init__(self, grid, startCoordinates):
    self.__grid = grid
    self.__startCoordinates = startCoordinates
    self.__endCoordinates = None

  def __traverse(self, startCoordinates):
    queue = []

    # Initially store the starting coordinates in the queue
    queue.append(startCoordinates)

    # Run the loop until the queue is empty 
    while len(queue) > 0:

      # Pop the first element and work on it
      top = queue.pop(0)

      # If the coordinates are out of maze then return false
      if not isValid(self.__grid.getShape(), top): continue

      # Get the self.__grid state
      gridState = self.__grid.get(top)

      # Check if the coordinates are end point
      if gridState == 3:
        self.__endCoordinates = top
        break

      # if the coordinates are representing a wall then return False
      if gridState == 1: continue

      # if the coordinates are previously visited then return False
      if gridState == 4: continue

      # Now make the element at specified coordinates visited
      self.__grid.set(top, 4)

      # Traverse the grid in 4 directions

      #left 
      queue.append((top[0] + 0, top[1] + 1))

      # right
      queue.append((top[0] + 0, top[1] - 1))
      
      # up
      queue.append((top[0] + 1, top[1] + 0))
       
      # down
      queue.append((top[0] - 1, top[1] + 0))

  def start(self):
    self.__traverse(self.__startCoordinates)
    return self.__endCoordinates

class bfs_backtracking:
  def __init__(self, grid, startCoordinates):
    self.__grid = grid
    self.__startCoordinates = startCoordinates
    self.__endCoordinates = None

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

      # Traverse the grid in 4 directions

      #left 
      queue.append((top[0] + 0, top[1] + 1))
      if (top[0] + 0, top[1] + 1) not in prev:
        prev[(top[0] + 0, top[1] + 1)] = top

      # right
      queue.append((top[0] + 0, top[1] - 1))
      if (top[0] + 0, top[1] - 1) not in prev:
        prev[(top[0] + 0, top[1] - 1)] = top
      
      # up
      queue.append((top[0] + 1, top[1] + 0))
      if (top[0] + 1, top[1] + 0) not in prev:
        prev[(top[0] + 1, top[1] + 0)] = top
       
      # down
      queue.append((top[0] - 1, top[1] + 0))
      if (top[0] - 1, top[1] + 0) not in prev:
        prev[(top[0] - 1, top[1] + 0)] = top

    if self.__endCoordinates is not None:
      currCordinate = self.__endCoordinates
      while(currCordinate != (-1, -1)):
        self.__grid.set(currCordinate, 5)
        currCordinate = prev[currCordinate]

  def start(self):
    self.__traverse(self.__startCoordinates)
    return self.__endCoordinates

class bfs_corner:
  def __init__(self, grid, startCoordinates):
    self.__grid = grid
    self.__startCoordinates = startCoordinates
    self.__endCoordinates = None

  def __traverse(self, startCoordinates):
    queue = []

    # Initially store the starting coordinates in the queue
    queue.append(startCoordinates)

    # Run the loop until the queue is empty 
    while len(queue) > 0:

      # Pop the first element and work on it
      top = queue.pop(0)

      # If the coordinates are out of maze then return false
      if not isValid(self.__grid.getShape(), top): continue

      # Get the self.__grid state
      gridState = self.__grid.get(top)

      # Check if the coordinates are end point
      if gridState == 3:
        self.__endCoordinates = top
        break

      # if the coordinates are representing a wall then return False
      if gridState == 1: continue

      # if the coordinates are previously visited then return False
      if gridState == 4: continue

      # Now make the element at specified coordinates visited
      self.__grid.set(top, 4)

      # Traverse the grid in 8 directions

      #left 
      queue.append((top[0] + 0, top[1] + 1))

      # right
      queue.append((top[0] + 0, top[1] - 1))
      
      # up
      queue.append((top[0] + 1, top[1] + 0))
       
      # down
      queue.append((top[0] - 1, top[1] + 0))

      # top-left 
      queue.append((top[0] + 1, top[1] + 1))

      # top-right
      queue.append((top[0] + 1, top[1] - 1))
      
      # bottom-left
      queue.append((top[0] - 1, top[1] + 1))
       
      # down
      queue.append((top[0] - 1, top[1] - 1))


  def start(self):
    self.__traverse(self.__startCoordinates)
    return self.__endCoordinates
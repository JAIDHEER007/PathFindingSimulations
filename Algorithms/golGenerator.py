import numpy as np
from PIL import Image
from time import perf_counter
import os
from os.path import join
import datetime
import cv2
import re

from Helper import helper

class gol:
    def isValid(i:int, j:int, rows:int, cols:int) -> bool:
        return (i >= 0) and (i < rows) and (j >= 0) and (j < cols)
    
    def rules(lives:int, currState:bool) -> bool:
        if currState:
            if lives > 3 or lives < 2:
                return False
            else: return True  
        return (lives == 3)
    
    def generationUpdate(grid):
        rows, cols = grid.shape
        # print(rows, cols)
        nextGeneration = np.zeros((rows, cols), dtype = bool)
        for i in range(rows):
            for j in range(cols):

                # Finding the Live Neighbours
                lives = 0
                for m in [-1, 0, 1]:
                    for n in [-1, 0, 1]:
                        if m == 0 and n == 0: continue
                        lives += int(grid[(((i + m) + rows) % rows), (((j + n) + cols) % cols)]);
                            
                nextGeneration[i, j] = gol.rules(lives, grid[i, j])

        return nextGeneration
        
    def __init__(self, startGrid, generations, cwd):
        self.__rows, self.__cols = startGrid.shape 
        self.__grid = startGrid
        self.__cwd = cwd
        self.__generations = generations

        #Folder Path
        self.__fPath = helper.createFolder(cwd = self.__cwd, 
                                          initialState = self.__grid, 
                                          extraInfo = {
                                            "Algorithm": "JC Game of Life", 
                                            "generations": self.__generations
                                          }, 
                                          directories = ["Images", "CSVs"])
    
    def start(self):
        if self.__rows > 200 or self.__cols > 200:
            raise Exception("Grid Limit Reached")
        
        imgPath = join(self.__fPath, 'Images')
        csvPath = join(self.__fPath, 'CSVs')
        for generation in range(self.__generations):
            img = Image.fromarray(self.__grid)
            img = img.resize((self.__rows * 10, self.__cols * 10))

            # Save the Image
            img.save(join(imgPath, f'State_{self.__rows}__{self.__cols}__{generation}.png'))
            
            # Save the csv file
            np.savetxt(fname = join(csvPath, f'State_{self.__rows}__{self.__cols}__{generation}.csv'), 
                       X = self.__grid, delimiter = ',', fmt='%d')

            self.__grid = gol.generationUpdate(self.__grid)
        
    

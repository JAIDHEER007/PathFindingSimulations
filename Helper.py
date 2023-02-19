import datetime
import re
import os
import json 

import copy

import numpy as np
import pandas as pd

import cv2
from PIL import Image

class helper:
    info = {
      "author": "S.Jaidheer", 
      "github_id": "JAIDHEER007", 
      "iteration_info":{
        "directory_name": None,
        "Date": None, 
        "Time": None, 
        "Rows": None, 
        "Cols": None
      },
      "directories_created": None,
      "extra_info": None
    }

    def createFolder(cwd, initialState, extraInfo = {}, directories = []) -> str:
        # Getting Current Time
        curr = datetime.datetime.now()
        dateStr = str(curr.date())
        timeStr = str(curr.time())

        # Folder Name
        directory = "Run_" + re.sub('\D', '', dateStr) + "_" + re.sub('\D', '', timeStr)

        # Final Path
        fPath = os.path.join(cwd, directory)

        # Creating a Directory
        os.mkdir(fPath)

        # Making the extra Directories if Needed
        for _directory in directories:
            dirPath = os.path.join(fPath, _directory)
            os.mkdir(dirPath)

        # Writing the useful files

        # Saving the initial grid state
        np.savetxt(fname = os.path.join(fPath, 'initialState.csv'), 
                   X = initialState, delimiter = ',', fmt='%d')

        rows, cols = initialState.shape
        info = copy.deepcopy(helper.info)
        info["iteration_info"]["Date"] = dateStr
        info["iteration_info"]["Time"] = timeStr
        info["iteration_info"]["Rows"] = rows
        info["iteration_info"]["Cols"] = cols
        info["iteration_info"]["directory_name"] = directory
        info["directories_created"] = directories
        info["extra_info"] = extraInfo

        with open(os.path.join(fPath, 'info.json'), 'w') as fileHandle:
          json.dump(info, fileHandle, indent = 2)

        return fPath 

class ImageGenerator:
  colors = [(0,0,0), (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)]
  def __init__(self, fPath, stateMatrix = None):
    self.__count = 0
    self.__stateMatrix = stateMatrix
    self.__fPath = fPath

  def resetCount(self):
    self.__count = 0

  def getStateMatrix(self):
    stateMatrixFilePath = os.path.join(self.__fPath, "StateMatrix.csv")
    self.__stateMatrix = pd.read_csv(stateMatrixFilePath, header=None, dtype=int).to_numpy()

  def __saveImage(self, dPath, npGrid):
    img = Image.fromarray(npGrid, mode="RGB")

    # Saving the Image to Images subfolder
    img.save(os.path.join(dPath, 'Img{cnt}.png'.format(cnt = self.__count)))

    self.__count += 1

  def generate(self, zoomFactor):
    if self.__stateMatrix is None:
      raise Exception("Missing State Matrix or invoke Get StateMatrix function to get from file")
    
    # Reading the InitialState
    initialStateFilePath = os.path.join(self.__fPath, "initialState.csv")
    initalState = pd.read_csv(initialStateFilePath, header=None, dtype=int).to_numpy()
    
    # Path to the Images Sub Folder
    imagesFolder = os.path.join(self.__fPath, 'Images')

    # Creating a new directory in Images folder
    curr = datetime.datetime.now()
    dateStr = str(curr.date())
    timeStr = str(curr.time())
    imgPath = os.path.join(imagesFolder, 'Imgs_z{zf}_d{d}_t{t}'.format(
                            zf = zoomFactor,
                            d = re.sub('\D', '', dateStr),
                            t = re.sub('\D', '', timeStr)
                          ))

    # Creating a Directory
    os.mkdir(imgPath)

    oldShape = initalState.shape
    newGrid = np.zeros((oldShape[0] * zoomFactor, oldShape[1] * zoomFactor, 3), dtype=np.uint8)
    newShape = newGrid.shape

    # Coordinate Mapping
    cMap = {}

    # Populating the new grid
    for i in range(newShape[0]):
        for j in range(newShape[1]):
          # Populating the Color Map
          isCoordinate = (i // zoomFactor , j // zoomFactor)
          cMapLst = cMap.get(isCoordinate)
          if cMapLst is None:
            cMap[isCoordinate] = [(i, j)]
          else:
            cMapLst.append((i, j))
            cMap[isCoordinate] = cMapLst

          newGrid[(i, j)] = ImageGenerator.colors[initalState[isCoordinate]]

    # Saving the initial Image as Img0
    self.__saveImage(imgPath, newGrid)

    for state in self.__stateMatrix:
      oldCoordinates = state[0]
      colorIndex = state[1]
      for coordinate in cMap[oldCoordinates]:
        newGrid[coordinate] = ImageGenerator.colors[colorIndex]
      
      self.__saveImage(imgPath, newGrid)
      
    return imgPath
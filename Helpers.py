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

    def getDThash():
      curr = datetime.datetime.now()
      return {
              'date': re.sub('\D', '', str(curr.date())), 
              'time': re.sub('\D', '', str(curr.time()))
             }

    def createFolder(cwd, initialState, extraInfo = {}, directories = []) -> str:
        # Getting Current Time
        dtHash = helper.getDThash()

        # Folder Name
        directory = "Run_" + dtHash['date'] + "_" + dtHash['time']

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
        info["iteration_info"]["Date"] = dtHash['date']
        info["iteration_info"]["Time"] = dtHash['time']
        info["iteration_info"]["Rows"] = rows
        info["iteration_info"]["Cols"] = cols
        info["iteration_info"]["directory_name"] = directory
        info["directories_created"] = directories
        info["extra_info"] = extraInfo

        with open(os.path.join(fPath, 'info.json'), 'w') as fileHandle:
          json.dump(info, fileHandle, indent = 2)

        return fPath 
    
    
    

colorCodesRGB = [(0,0,0), (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)]
colorCodesBRG = [(0,0,0), (255, 255, 255), (0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 165)]

class ImageGenerator:
  def __init__(self, fpath, stateMatrix = None):
    self.__count = 0
    self.__stateMatrix = stateMatrix
    self.__fPath = fpath

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
    dtHash = helper.getDThash()

    imgPath = os.path.join(imagesFolder, f'Imgs_z{zoomFactor}_d{dtHash["date"]}_t{dtHash["time"]}')

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

          newGrid[(i, j)] = colorCodesRGB[initalState[isCoordinate]]

    # Saving the initial Image as Img0
    self.__saveImage(imgPath, newGrid)

    for state in self.__stateMatrix:
      oldCoordinates = state[0]
      colorIndex = state[1]
      for coordinate in cMap[oldCoordinates]:
        newGrid[coordinate] = colorCodesRGB[colorIndex]
      
      self.__saveImage(imgPath, newGrid)
      
    return imgPath

class VideoGenerator_v1:
  def saveVideo(fPath, imgPath, fps, videoName = "Output"):    
    video_name = os.path.join(fPath, "Videos", f"{videoName}.mp4")

    images = [img for img in os.listdir(imgPath) if img.endswith(".png")]

    if len(images) == 0: 
        raise Exception("No Images were created. Call start() method")

    pattern = re.compile(r'[0-9]+')
    images.sort(key = lambda image: int(pattern.findall(image)[-1]))

    frame = cv2.imread(os.path.join(imgPath, images[0]))

    height, width = frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height)) 

    for image in images:
        video.write(cv2.imread(os.path.join(imgPath, image)))

    cv2.destroyAllWindows() 
    video.release()

class VideoGenerator_v2:
  def saveVideo(fPath, fps, stateMatrix = None, zoomFactor = 3, videoName = "Output"):    
    if stateMatrix is None:
      raise Exception("State Matrix Can't be None")
    
    # Reading the InitialState
    initialStateFilePath = os.path.join(fPath, "initialState.csv")
    initalState = pd.read_csv(initialStateFilePath, header=None, dtype=int).to_numpy()

    # Video Name
    videoName = os.path.join(fPath, "Videos", f"{videoName}.mp4")

    # Zooming the frame
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

        newGrid[(i, j)] = colorCodesBRG[initalState[isCoordinate]]

    # Creating a Video Writer
    height, width = newShape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(videoName, fourcc, fps, (width, height)) 

    # Writing the initial state
    video.write(newGrid)

    # Modifiy the grid for each state and write it to video writer
    for state in stateMatrix:
      oldCoordinates = state[0]
      colorIndex = state[1]
      for coordinate in cMap[oldCoordinates]:
        newGrid[coordinate] = colorCodesBRG[colorIndex]

      video.write(newGrid)
    
    # Release the resources
    cv2.destroyAllWindows() 
    video.release()
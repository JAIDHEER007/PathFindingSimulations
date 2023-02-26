import sys
import os
import pandas as pd

import argparse
import urllib.request
import json 
import datetime
import re

# Defining the current working directory 
cwd = sys.path[0]

# Setting the recursion depth
sys.setrecursionlimit(10**5)

# Adding the previous folder to sys.path to import the required modules
sys.path.append(os.path.join(cwd, '..'))

from Helpers import helper
# from Helpers import ImageGenerator
from Helpers import VideoGenerator_v2

from GridCollection import Grid1

import Algorithms

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(
        description = "Runn Path finding Simuations using json test data",
        epilog = "Created with ❤ by Jaidheer"
    )
    parser.add_argument(
        '--jsonPath', '-p',
        metavar = 'jsonPath', 
        nargs = '?',
        type = str,
        default = '', 
        required = True,
        help = 'Enter the json file path',
    )
    
    parser.add_argument(
        '--is_url', '-u',
        metavar = 'isUrl', 
        nargs = '?',
        type = bool,
        const = True,
        default = False, 
        required = False,
        help = 'Consider the path passed as the online link for JSON',
    )

    args = parser.parse_args()

    jsonPath, isUrl= args.jsonPath, args.is_url

    # Reading the json file
    testJson = None
    if isUrl:
      # if the file path is provided as a url
      # read the json data from url 
      with urllib.request.urlopen(jsonPath) as url:
        testJson = json.load(url)
    else:
      # open it with fileHandling
      with open(os.path.join(cwd, jsonPath)) as fileHandle:
        testJson = json.load(fileHandle)  

    # parsing the recieved test json file
    savePath = testJson['savePath']      # final path to save the generated files
    
    # Creating a batch run folder to store all the batch runs in it
    dtHash = helper.getDThash()

    # Folder Name
    directory = "Batch_Run_" + dtHash['date'] + "_" + dtHash['time']

    # Final Path
    fPath = os.path.join(savePath, directory)

    # Creating a Directory
    os.mkdir(fPath)

    # # creating the batch folders and storing the filepaths in testJson
    # for i in range(len(testJson['testData'])):
    #   testJson['batches'][i]['fPath'] = helper.createFolder(cwd = fPath, 
    #                                                 initialState = initialState, 
    #                                                 extraInfo = testJson['testData'][i], 
    #                                                 directories = ["Images", "Videos"])

    # storing the test json in batch run folder
    # with open(os.path.join(fPath, 'test.json'), 'w') as fileHandle:
    #   json.dump(testJson, fileHandle, indent = 2)

    # Logger Function
    def logger(log: list, info: str) -> None:
      log.append(info)
      print(info)

    # parsing the test data and executing for each test case
    for i, testCase in enumerate(testJson['batches']):
      try:
        # Logger list to store the logs
        log = []

        csvFilePath = testCase['gridCSV']     # file path to recieve the initial grid

         # Reading the csv file
        initialState = pd.read_csv(csvFilePath, header=None, dtype=int).to_numpy()
        logger(log, 'CSV grid reading successful')

        # Creating the Run folder
        testCase_fPath = helper.createFolder(cwd = fPath, 
                                             initialState = initialState, 
                                             extraInfo = testCase, 
                                             directories = ["Images", "Videos"])
        
        # Adding the testCase_fPath to testJson file
        testCase['fPath'] = testCase_fPath

        logger(log, 'Created the running directory')

        # parsing the starting and ending locations
        str2int = lambda coordinate: int(coordinate.strip())
        startingLocation = tuple(map(str2int, testCase['startingLocation'].strip().split(',')))
        endingLocation = tuple(map(str2int, testCase['endingLocation'].strip().split(',')))

        logger(log, 'Parsed the starting and ending location')

        # Creating the grid object
        grid = Grid1(npgrid = initialState)

        logger(log, 'Created the grid object')

        # checking if the starting location and ending location are valid
        if not Algorithms.isValid(grid.getShape(), startingLocation):
          raise Exception("Starting Location Outside the grid")
        if not Algorithms.isValid(grid.getShape(), endingLocation):
          raise Exception("Ending Location Outside the grid")
        
        logger(log, 'Starting and Ending Locations validations completed')

        # Setting the starting Location
        grid.set(startingLocation, 2)
        grid.set(endingLocation, 3)

        runnerObject = Algorithms.Runner.create(algorithm = testCase['algorithm'], kwargs = 
                                      {
                                        'grid': grid,
                                        'startCoordinates': startingLocation,
                                        'endingCoordinates': endingLocation,
                                        'corners': testCase['corners'],
                                        'backtracking': testCase['backtracking']
                                      }
                                    )
        logger(log, 'Created the Runner object')

        # Run the simulation
        assert endingLocation == runnerObject.start(), 'Ending Location could not be found'
        logger(log, 'Found the ending location')

        # Saving the stateMatrix
        grid.saveStateMatrix(fPath = testCase_fPath)
        logger(log, 'Saved the state matrix to file')

        # saving the video files
        if testCase['videoRequired']:
          logger(log, 'Started video processing')
          videoDetails = testCase['videoDetails']
          for vedioData in zip(videoDetails['zoomFactors'], videoDetails['fpsLst']):
            zoomFactor, fps = vedioData[0], vedioData[1]
            dtHash = helper.getDThash()
            
            outputVedioName = f"Output_z{zoomFactor}_f{fps}_d{dtHash['date']}_t{dtHash['time']}"
            VideoGenerator_v2.saveVideo(fPath = testCase_fPath, fps = fps, stateMatrix = grid.stateMatrix(), 
                              zoomFactor = zoomFactor, videoName = outputVedioName)
            logger(log, 'Saved a video')

      except Exception as exp:
        logger(log, exp.args.__repr__())
      finally:
        testCase['log'] = log

        # Write the new testCase file to info.json
        with open(os.path.join(testCase_fPath, 'info.json'), 'w') as fileHandle:
          json.dump(testCase, fileHandle, indent = 2)

    # Finally save the main testCase json again
    with open(os.path.join(fPath, 'test.json'), 'w') as fileHandle:
      json.dump(testJson, fileHandle, indent = 2)

        



      

      
    


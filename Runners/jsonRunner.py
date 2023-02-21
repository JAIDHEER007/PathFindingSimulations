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
    csvFilePath = testJson['csvFile']     # file path to recieve the initial grid
    fpath = testJson['savePath']      # final path to save the generated files
    
    # Reading the csv file
    initialState = pd.read_csv(csvFilePath, header=None, dtype=int).to_numpy()
    print('Read the CSV')

    # parsing the starting and ending locations
    startingLocation = tuple(map(int, testJson['startingLocation'].strip().split(',')))
    endingLocation = tuple(map(int, testJson['endingLocation'].strip().split(',')))

    # Creating a batch run folder to store all the batch runs in it

    # Getting Current Time
    curr = datetime.datetime.now()
    dateStr = str(curr.date())
    timeStr = str(curr.time())

    # Folder Name
    directory = "Batch_Run_" + re.sub('\D', '', dateStr) + "_" + re.sub('\D', '', timeStr)

    # Final Path
    fPath = os.path.join(fpath, directory)

    # Creating a Directory
    os.mkdir(fPath)

    # creating the batch folders and storing the filepaths in testJson
    for i in range(len(testJson['testData'])):
      testJson['testData'][i]['fPath'] = helper.createFolder(cwd = fPath, 
                                                    initialState = initialState, 
                                                    extraInfo = testJson['testData'][i], 
                                                    directories = ["Images", "Videos"])

    # storing the test json in batch run folder
    with open(os.path.join(fPath, 'test.json'), 'w') as fileHandle:
      json.dump(testJson, fileHandle, indent = 2)

    # parsing the test data and executing for each test case
    for i, testCase in enumerate(testJson['testData']):
      try:
        # folder path for each test case
        testCase_fPath = testCase['fPath']

        # Creating the grid object
        grid = Grid1(npgrid = initialState)

        # checking if the starting location and ending location are valid
        if not Algorithms.isValid(grid.getShape(), startingLocation):
          raise Exception("Starting Location Outside the grid")
        if not Algorithms.isValid(grid.getShape(), endingLocation):
          raise Exception("Ending Location Outside the grid")

        # Setting the starting Location
        grid.set(startingLocation, 2)
        grid.set(endingLocation, 3)

        runnerObject = Algorithms.Runner.create(algorithm = testCase['name'], kwargs = 
                                      {
                                        'grid': grid,
                                        'startCoordinates': startingLocation,
                                        'corners': testCase['corners'],
                                        'backtracking': testCase['backtracking']
                                      }
                                    )

        # Run the simulation
        assert endingLocation == runnerObject.start(), 'Ending Location could not be found'
        print('Found the ending location')

        # saving the video files
        if testCase['videoRequired']:
          print('Started video processing')
          videoDetails = testCase['videoDetails']
          for vedioData in zip(videoDetails['zoomFactors'], videoDetails['fpsLst']):
            zoomFactor, fps = vedioData[0], vedioData[1]
            curr = datetime.datetime.now()
            currDate = re.sub('\D', '', str(curr.date()))
            currTime = re.sub('\D', '', str(curr.time()))
            
            outputVedioName = f"Output_z{zoomFactor}_f{fps}_d{currDate}_t{currTime}"
            VideoGenerator_v2.saveVideo(fPath = testCase_fPath, fps = fps, stateMatrix = grid.stateMatrix(), 
                              zoomFactor = zoomFactor, videoName = outputVedioName)
            print('Saved a video')
            


      except Exception as exp:
        print(exp)
        testCase['result'] = exp.args.__repr__()
        testJson['testData'][i]['result'] = exp.args.__repr__()
      else:
        testCase['result'] = 'Found the ending location'
      finally:
        # Write the new testCase file to info.json
        with open(os.path.join(testCase_fPath, 'info.json'), 'w') as fileHandle:
          json.dump(testCase, fileHandle, indent = 2)

    # Finally save the main testCase json again
    with open(os.path.join(fPath, 'test.json'), 'w') as fileHandle:
      json.dump(testJson, fileHandle, indent = 2)

        



      

      
    


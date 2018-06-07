# -*- coding: utf-8 -*-

import json, csv
import numpy as np
import pandas as pd


DUMP_FILE   = 'pluginText.dump'
INPUT_FILE  = 'programs.txt'
OUTPUT_FILE = 'results.html'


# 		loadData()
#
# Function to load JSON information from a file stream
# Input  - none
# Output - Python dictionary with data
def loadData():
    f       = open(DUMP_FILE, 'r')
    rawData = json.load(f)
    f.close()
    return rawData


# 		readInput()
#
# Function to load JSON information from a file stream
# Input  - none
# Output - Python dictionary with data
def readInput():
    f    = open(INPUT_FILE, 'r')
    data = f.read().splitlines()
    return data


# 		createMatrix()
#
# Creates and populates a table containing software information about desired
# software from given hosts
# Input  - data: Host data dict object, dict with host IP, DNS, Repository, and
#                Content
#          inputData: List of programs to search for
# Output - Numpy matrix object, where each row represents a different host, and
#          each column represents a different software. This means matrix
#          elements at row row index [i] will have software information about
#          the host with ID = i + 1. Elements along column [j] will be lists of
#          the software on line number j + 1 in the INPUT_FILE. E.G. if the
#          second line of my input file is 'ssh', resultMat[0][1] will be all
#          ssh programs installed on host with ID 1.
def createMatrix(data, inputData):
    resultMat = np.empty((len(data), len(inputData)), dtype=object)
    for i, host in enumerate(data):
        for j, inputProgram in enumerate(inputData):
            tempList = ''
            for program in host['CONTENT']:
                if inputProgram.lower() in program.lower():
                    tempList += program + '<br>'

            resultMat[i][j] = tempList
    return resultMat


def getHostInfo(hostData):
    hostInfo = []
    for host in hostData:
        temp = str(host['DNS'] + '<br>' + host['IP'] + '<br>' + host['REPO'])
        hostInfo.append(temp)

    return hostInfo

# 		writeToHTML()
#
# Writes the given numpy matrix to a table in a HTML file
# Input  - data: Installed program information about each requested program. m rows by n columns, where each row is a
#                host, and each column is a program that was specified to search for
#          inputData: List of programs to search for
# Output - none, out to file
def writeToHTML(data, inputData, hostData):
    hostFrame = pd.DataFrame(hostData, index=range(1,len(data) + 1), columns=['Host Info:'])
    progFrame = pd.DataFrame(data, index=range(1,len(data) + 1), columns=inputData)

    pdFrame = pd.concat([hostFrame, progFrame], axis=1)
    pd.set_option('display.max_colwidth', -1)
    pdFrame.to_html(OUTPUT_FILE, escape = False)

    return


def main():
    data        = loadData()
    inputData   = readInput()
    resultMat   = createMatrix(data, inputData)
    hostInfo    = getHostInfo(data)
    writeToHTML(resultMat, inputData, hostInfo)

    return 0


# # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()

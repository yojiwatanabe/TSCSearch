#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import numpy as np
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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
def readInput(infile):
    f    = open(infile, 'r')
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
    if inputData:
        resultMat = np.empty((len(data), len(inputData)), dtype=object)
    else:
        resultMat = np.empty((len(data), 1), dtype=object)
    if inputData:
        for i, host in enumerate(data):
            for j, inputProgram in enumerate(inputData):
                tempList = ''
                for program in host['CONTENT']:
                    if inputProgram.lower() in program.lower():
                        tempList += program + '<br>'
                resultMat[i][j] = tempList
    else:
        print 'no input!!!'
        for i, host in enumerate(data):
            tempList = ''
            for program in host['CONTENT']:
                tempList += program + '<br>'
            resultMat[i] = tempList
    return resultMat


# 		getHostInfo()
#
# Returns information from the host in a pd.to_html friendly format (string)
# Input  - hostData: Dictionary array with host info like DNS, IP, and REPO
# Output - String array with all of the hosts' information
def getHostInfo(hostData):
    hostInfo = []
    for host in hostData:
        temp = (host['DNS'] + '<br>' + host['IP'] + '<br>' + host['REPO']).encode('utf-8')
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
    if inputData:
        progFrame = pd.DataFrame(data, index=range(1,len(data) + 1), columns=inputData)
    else:
        progFrame = pd.DataFrame(data, index=range(1,len(data) + 1), columns=['Plugin Output:'])
    pdFrame = pd.concat([hostFrame, progFrame], axis=1)
    pd.set_option('display.max_colwidth', -1)
    pdFrame.to_html(OUTPUT_FILE, escape = False)

    return

def createTable(pluginID, infile=''):
    data        = loadData()
    inputData = ''
    if infile:
        inputData   = readInput(infile)
    resultMat   = createMatrix(data, inputData)
    hostInfo    = getHostInfo(data)

    writeToHTML(resultMat, inputData, hostInfo)
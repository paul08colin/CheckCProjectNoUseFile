import os
import os.path
import fileinput
import math
import re
g = os.walk("../../Desktop/server")
mainFileName = 'main'
def CheckCanOpenFile(canOpenFile):
    for dirpath, dirname,filename in g:
            for fn in filename:
                name = dirpath + '/' + fn
                theFileCanOpen = True
                fp = open(name, "r")
                try:
                    for line in fp:
                        num = 100
                    theFileCanOpen = True
                except:
                    continue
                fp.close()
                if name[-2:] == '.h' or name[-4:] == '.cpp':
                    canOpenFile.append(name)
def GetShortestName(longName):
    nameList = longName.split('/')
    includeFileName = nameList[-1]
    includeFileName = includeFileName.split('.')[0]
    return includeFileName

def dijkstra(graphV, graphE):
    currentLen = len(graphV)
    finishV = []
    for i in range(0, len(graphV)):
        finishV.append(False)
    while(currentLen > 0):
        currentLen = currentLen - 1
        minV = math.inf
        minVindex = 0
        for i in range(0, len(graphV)):
            if (graphV[i] < minV and finishV[i] == False):
                minVindex = i
                minV = graphV[i] 
        finishV[minVindex] = True
        for i in range(0, len(graphE[minVindex])):
            if (graphE[minVindex][i] + graphV[minVindex] < graphV[i]):
                graphV[i] = graphE[minVindex][i] + graphV[minVindex];

def buildGraph(fileNameToNum, graphE, graphV):
    if (mainFileName in fileNameToNum):
        rootNum = fileNameToNum[mainFileName];
    else:
        print ("root file can't find: ", mainFileName)
        return
    for i in range(0, len(fileNameToNum)):
        subE = []
        for j in range(0, len(fileNameToNum)):
            subE.append(math.inf)
        graphE.append(subE)
        graphV.append(math.inf)
    graphV[rootNum - 1] = 0
    for file in canOpenFile:
        shortName = GetShortestName(file)
        if (shortName not in fileNameToNum):
            continue
        theFileNum = fileNameToNum[shortName]
        for theLine in fileinput.FileInput(file, inplace = 0):
            if (theLine.find("#include") != -1):
                tempRe = re.search("[a-zA-Z0-9_]+(\.h)", theLine);
                if (tempRe == None):
                    continue
                tempStr = tempRe.group(0)
                tempStr = tempStr.split('.')
                if (tempStr[-2] in fileNameToNum):
                    graphE[theFileNum - 1][fileNameToNum[tempStr[-2]] - 1] = 1


def CalcUselessFile(canOpenFile):
    fileNameToNum = {}
    numToFileName = {}
    graphE = [] 
    graphV = []
    dropFile = []
    fileNum = 0
    rootNum = 0
    ShortNameToLongName = {}
    for file in canOpenFile:
            includeFileName = GetShortestName(file)
            ShortNameToLongName[includeFileName] = file;
            if (includeFileName not in fileNameToNum):
                fileNum = fileNum + 1 
                fileNameToNum[includeFileName]  = fileNum
                numToFileName[fileNum] =  includeFileName
    buildGraph(fileNameToNum, graphE, graphV)
    dijkstra(graphV, graphE)
    print ("output useless file")
    for i in range(0, len(graphV)):
            if (graphV[i] == math.inf):
                print (ShortNameToLongName[numToFileName[i + 1]])


canOpenFile = []
CheckCanOpenFile(canOpenFile)
shortNameOpenFile = []
for file in canOpenFile:
    nameList = file.split('/')
    shortName = nameList[-1]
    shortNameOpenFile.append(shortName)
CalcUselessFile(canOpenFile)





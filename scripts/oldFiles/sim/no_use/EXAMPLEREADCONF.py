import yaml
import sys
import os

def readConfFile(pathToFile):
    dictConf = {}
    with open(pathToFile, "r") as fileConf:
        lines = fileConf.readlines()
        lines = [line.rstrip().split("=") for line in lines]
        for line in lines:
            dictConf[line[0]] = line[1]
    return dictConf




dictTemp = readConfFile("tasksExecutables.conf")
print(dictTemp)





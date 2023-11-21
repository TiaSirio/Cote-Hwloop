import sys
from itertools import zip_longest
import statistics

fileSingle = ""
fileToCheck = ""

PLUS_X_V = 0
PLUS_X_A = 1
PLUS_Y_V = 2
PLUS_Y_A = 3
BAT_V = 4
BAT_A = 5
BUS_V = 6
BUS_A = 7
MINUS_X_V = 8
MINUS_X_A = 9
MINUS_Y_V = 10
MINUS_Y_A = 11
PLUS_Z_V = 12
PLUS_Z_A = 13
MINUS_Z_V = 14
MINUS_Z_A = 15
IHU_TEMP = 16

variables = [name for name, value in globals().items() if value in range(17)]



if len(sys.argv) == 3:
    fileSingle = sys.argv[1]
    fileToCheck = sys.argv[2]
else:
    print("Usage: python3 benchmarkProcessing.py /full/path/to/singleBenchmark/ /full/path/to/fileToCheck/")
    exit()

totalList = []

with open(fileSingle, 'r') as file1, open(fileToCheck, 'r') as file2:
    for line1, line2 in zip_longest(file1, file2, fillvalue=''):
        line1 = line1.rstrip('\n')
        line2 = line2.rstrip('\n')

        if not line1 or not line2:
            break

        tempList1 = line1.split(",")
        tempList2 = line2.split(",")
        tempList1.pop(0)
        tempList2.pop(0)
        tempList1 = [float(elem) for elem in tempList1]
        tempList2 = [float(elem) for elem in tempList2]

        tempSubtractionList = [abs(x - y) for x, y in zip(tempList2, tempList1)]

        totalList.append(tempSubtractionList)

meanList = [statistics.mean(sublist) for sublist in zip(*totalList)]

for idx, val in enumerate(meanList):
    if "BUS_V" in variables[idx]:
        print("---BUS_WATT---: " + str(meanList[idx] * (meanList[idx + 1]/1000)))
    if "_A" in variables[idx]:
        print(variables[idx] + ": " + str(meanList[idx]/1000))
    else:
        print(variables[idx] + ": " + str(meanList[idx]))
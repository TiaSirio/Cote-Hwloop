import subprocess
import os
import json
import re
from json import JSONEncoder
from enum import Enum
import math
import sys


class TotalIterations:
	def __init__(self, iterations, allResults):
		self.iterations = iterations
		self.allResults = allResults

	def toJson(self):
		return json.dumps(self, default=lambda o: o.__dict__)

class Sensors:
	def __init__(self, sensors):
		self.positiveX = sensors[0]
		self.negativeX = sensors[5]
		self.positiveY = sensors[1]
		self.negativeY = sensors[6]
		self.positiveZ = sensors[4]
		self.negativeZ = sensors[7]
		self.battery = sensors[2]
		self.bus = sensors[3]

class GenericElement:
	def __init__(self, voltage, current):
		self.voltage = voltage
		self.current = current

	def setVoltage(self, voltage):
		self.voltage = float(voltage)

	def setCurrent(self, current):
		if float(current) < 0:
			self.current = 0
		else:
			self.current = float(current)

class SensorsEncoder(JSONEncoder):
	def default(self, s):
		return s.__dict__



if len(sys.argv) == 2:
	iters = int(sys.argv[1])
else:
	print("Setting the default number of iterations -> 10")
	iters = 10

numOfSensors = 8

os.chdir("/home/pi/CubeSatSim")
subprocess.run(["gcc", "myTelemTest.c", "-o", "myTelemTest"])
os.chdir("/home/pi/")

results = []
allResults = []
for k in range(numOfSensors):
	results.append(GenericElement(0.0, 0.0))

for i in range(iters):
	result = subprocess.run(["CubeSatSim/myTelemTest"], stdout=subprocess.PIPE, encoding="utf-8")
	#print(result.stdout)
	finalString = result.stdout[1:-3]
	#print(finalString)
	finalString = re.sub(" +", ",", finalString)
	#print(finalString)
	splittedArray = finalString.split(",")
	#print(splittedArray)
	j = 0

	for j in range(len(splittedArray)):
		if j % 2 == 0:
			results[math.floor(j/2)].setVoltage(splittedArray[j])
		else:
			results[math.floor(j/2)].setCurrent(splittedArray[j])

	temp = results.copy()
	sensorsData = Sensors(temp)

	json_str = SensorsEncoder().encode(sensorsData)
	allResults.append(json_str)

totalResults = TotalIterations(iters, allResults)

tempt = SensorsEncoder().encode(totalResults).replace("\\", "")
print(tempt.replace("\"{", "{").replace("}\"", "}"))

#finalJSON = json.dumps(totalResults.toJson(), indent=4)
#print(finalJSON)

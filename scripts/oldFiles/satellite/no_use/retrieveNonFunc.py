#!/usr/bin/env python3

import subprocess
import os
import re
import time
import fcntl


# Return timestamp in ms
def timestamp_ms():
	return str(round(time.time() * 1000))



fileName = "CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt"
os.chdir("/home/pi/CubeSatSim/")
subprocess.run(["gcc", "myTelemTest.c", "-o", "myTelemTest"])
os.chdir("/home/pi/")

try:
	while True:
		# Open the file and store a new line for non-func data
		with open(fileName, "a") as file:
			result = subprocess.run(["CubeSatSim/myTelemTest"], stdout=subprocess.PIPE, encoding="utf-8")
			finalString = result.stdout[1:-3]
			finalString = re.sub(" +", ",", finalString)
			#splittedArray = finalString.split(",")
			#print(splittedArray)
			timestampString = timestamp_ms() + "," + finalString + "\n"
			#print(timestampString)
			fcntl.flock(file, fcntl.LOCK_EX)
			file.write(timestampString)
			fcntl.flock(file, fcntl.LOCK_UN)
		time.sleep(0.1)

except KeyboardInterrupt:
	# print("Exiting")
	# Close file
	file.close()

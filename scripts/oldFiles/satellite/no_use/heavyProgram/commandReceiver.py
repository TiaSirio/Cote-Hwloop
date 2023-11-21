import paho.mqtt.client as mqtt
import time
import os
import subprocess
import fcntl
import sys

fileNonFunc = "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt"
#mqttTopic = [("cubesatsim/nonfuncdata/#", 0), ("cubesatsim/appdata/#", 0)]
mqttTopic = "cubesatsim/commands/"
mqttDuration = "cubesatsim/duration/"
mqttNonFunc = "cubesatsim/nonfuncdata/"
mqttAppData = "cubesatsim/appdata/"
programDir = "/home/pi/CubeSatSim/simulationFiles/cexec"
fileMapper = "mapper.txt"
#fileName = "cexec/mapper.txt"
msg = ""
sat = 0
nonFuncList = []
tasks = []
resultsOfTasks = []

maxTasks = []
minTasks = []
powerTasks = []


# Calculate the mean in a list of list [[1,2], [3,4], [5,6]] -> [[3,4]]
def calculate_mean(list):
	# print(list)
	nonFuncAvg = [round(sum(subList) / len(subList), 2) for subList in zip(*list)]
	return nonFuncAvg



# Calculate the max in a list of list [[8,2], [3,4], [5,0]] -> [[1,0]]
def calculate_min(list):
	# print(list)
	nonFuncMin = [min(idx) for idx in zip(*list)]
	return nonFuncMin



# Calculate the max in a list of list [[8,2], [3,4], [5,6]] -> [[8,6]]
def calculate_max(list):
	# print(list)
	nonFuncMax = [max(idx) for idx in zip(*list)]
	return nonFuncMax



# Calculate the power in a list of list [[1,2], [3,4], [5,6]] -> [[2 + 12 + 30]]
def calculate_pow(list):
	# print(list)
	tempVolt = 0
	powElem = []
	powList = []
	for elem in list:
		for i in range(len(elem)):
			if i % 2 == 0:
				tempVolt = elem[i]
			else:
				powElem.append(tempVolt * elem[i])
		powList.append(powElem)
	powerSum = [sum(i) for i in zip(*powList)]
	return powerSum



# Return timestamp in ms
def timestamp_ms():
	return round(time.time() * 1000)



# Search in the mapper file if there is the job for the satellite and retrieve the tasks to execute
def search_in_mapper_single(sat):
	file = open(fileMapper, "r")
	for line in file:
		# Reading programs to execute from the mapper
		values = line.rstrip("\n").split(",")
		if sat == int(values[0]):
			values.pop(0)
			file.close()
			return values
		values = []
	file.close()
	print("Instance of satellite not found!")
	return []



# Search in the mapper file if there is the job for the satellite and retrieve the tasks to execute.
# Once the instance of satellite is found -> delete the job line
def search_in_mapper_multiple(sat):
	file = open(fileMapper, "r+")
	returnVal = []
	linesFile = file.readlines()
	file.seek(0)
	file.truncate()
	firstJobFound = False
	for line in linesFile:
		# Reading programs to execute from the mapper
		values = line.rstrip("\n").split(",")
		# Delete the line of the programs we are going to execute
		if sat == int(values[0]) and not firstJobFound:
			values.pop(0)
			returnVal = values.copy()
			firstJobFound = True
		else:
			file.write(line)
		values = []
	file.close()
	if not firstJobFound:
		print("Instance of satellite not found!")
	return returnVal



def on_connect(cl, userdata, flags, rc):
	if rc == 0:
		cl.subscribe(mqttTopic + str(phSat) + "/#")
		print("Connected to broker")
	else:
		print("Connection failed")



def on_message(cl, userdata, message):
	#print("Received message: " + str(msg.payload.decode("utf-8") + ", on topic: " + msg.topic))
	global msg
	global sat
	
	msg = message.payload.decode("utf-8")
	sat = int("".join(message.topic.split("/")[-1:]))




if len(sys.argv) < 3:
	print("Missing argument: \"s for SingleJob or m for MultipleJobs\" and \"Number of Physical satellite\"!")
	sys.exit()

if sys.argv[1] == "s":
	single = True
else:
	single = False

phSat = sys.argv[2]

mqttBroker = "broker.hivemq.com"

os.chdir(programDir)

# Connect to MQTT broker
client = mqtt.Client("commandReceiver")
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBroker, port=1883)
client.loop_start()
resultsOfTask = []
durations = []

try:
	while True:
		# Possible extend to other commands if needed
		if msg == "execute":
			resultsOfTasks = []
			tasks = []
			durations = []
			minTask = []
			maxTasks = []
			powerTasks = []
			nonFuncList = []
			msg = ""

			# Search if the instance of satellite needs to execute some programs
			if single:
				programsToExecute = search_in_mapper_single(sat)
			else:
				programsToExecute = search_in_mapper_multiple(sat)
			# print(programsToExecute)

			if not programsToExecute:
				# Instance of satellite has finished to work
				client.publish(mqttDuration + str(phSat) + "/" + str(sat), "nodata")
				print("Skipping instance of satellite!")
			else:
				client.loop_stop()
				for program in programsToExecute:
					startingTimestamp = str(timestamp_ms())
					#print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat))
					arguments = []

					# Divide the arguments
					if ";" in program:
						arguments = program.split(";")
					else:
						arguments.append(program)

					# Exec python or c programs
					if arguments[0].endswith(".py"):
						execString = "python3"
						arguments.insert(0, execString)
					else:
						arguments.pop(0)
						execString = "./" + program
						arguments.insert(0, execString)

					# Start subprocess and wait of results
					proc = subprocess.Popen(arguments, stdout=subprocess.PIPE, encoding="utf-8")
					proc.wait()

					endingTimestamp = str(timestamp_ms())

					resultsOfTask = []

					# Handle all output of a program
					while True:
						# totalResultOfTask = []
						line = proc.stdout.readline()
						if not line:
							break
						resultsOfTask.append(line.rstrip())
					resultsOfTaskString = ",".join(resultsOfTask)
					resultsOfTasks.append(resultsOfTaskString)

					# Single result
					# resultsOfTasks.append(proc.stdout.readline())

					# result = subprocess.run([execString], stdout=subprocess.PIPE, encoding="utf-8")
					# resultsOfTasks.append(result)
					# print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat) + " - Ending at " + endingTimestamp + " with results " + proc.stdout.readline())

					# Send duration of the program to the simulation through MQTT
					# duration = int(endingTimestamp) - int(startingTimestamp)
					# client.publish(mqttDuration + str(sat), str(duration))
					durations.append(str(int(endingTimestamp) - int(startingTimestamp)))

					# Read non-func data and store it to do the computation here and send the computed data at the end
					with open(fileNonFunc, "r") as file:
						# print("Reading non functional values")
						lines = file.readlines()
						fcntl.flock(file, fcntl.LOCK_EX)
						for line in reversed(lines):
							nonFuncValues = []
							nonFuncValues = line.rstrip("\n").split(",")
							# if int(nonFuncValues[0]) <= int(1684154133480) and int(nonFuncValues[0]) >= int(1684154131347):
							if int(nonFuncValues[0]) <= int(endingTimestamp) and int(nonFuncValues[0]) >= int(startingTimestamp):
								nonFuncValues.pop(0)
								nonFuncValues = list(map(float, nonFuncValues))
								nonFuncList.append(nonFuncValues)
							# elif int(nonFuncValues[0]) < int(1684154131347):
							elif int(nonFuncValues[0]) < int(startingTimestamp):
								tasks.append(calculate_mean(nonFuncList.copy()))

								minTasks.append(calculate_min(nonFuncList.copy()))
								maxTasks.append(calculate_max(nonFuncList.copy()))
								powerTasks.append(calculate_pow(nonFuncList.copy()))

								nonFuncList = []
								break
						fcntl.flock(file, fcntl.LOCK_UN)
				# print(tasks)

				# Format the data in a string separated by commas and send them through MQTT
				tasks = [[str(insel) for insel in elem] for elem in tasks]
				tasks = [",".join(elem) for elem in tasks]
				finalTasks = ";".join(tasks)
				# print(finalTasks)

				
				minTasks = [[str(insel) for insel in elem] for elem in minTasks]
				minTasks = [",".join(elem) for elem in minTasks]
				finalMinTasks = ";".join(minTasks)
				maxTasks = [[str(insel) for insel in elem] for elem in maxTasks]
				maxTasks = [",".join(elem) for elem in maxTasks]
				finalMaxTasks = ";".join(maxTasks)
				powerTasks = [[str(insel) for insel in elem] for elem in powerTasks]
				powerTasks = [",".join(elem) for elem in powerTasks]
				finalPowerTasks = ";".join(powerTasks)
				

				# print(resultsOfTasks)
				finalResultsOfTasks = ";".join(resultsOfTasks)
				# print(finalResultsOfTasks)

				finalResultsOfDuration = ";".join(durations)
				# print(finalResultsOfDuration)

				client.publish(mqttNonFunc + str(phSat) + "/" + str(sat), finalTasks)
				client.publish(mqttNonFunc + str(phSat) + "/" + str(sat), finalMinTasks)
				client.publish(mqttNonFunc + str(phSat) + "/" + str(sat), finalMaxTasks)
				client.publish(mqttNonFunc + str(phSat) + "/" + str(sat), finalPowerTasks)
				client.publish(mqttAppData + str(phSat) + "/" + str(sat), finalResultsOfTasks)
				client.publish(mqttDuration + str(phSat) + "/" + str(sat), finalResultsOfDuration)
				client.loop_start()
		
		time.sleep(1)

except KeyboardInterrupt:
	print("exiting")
	client.disconnect()
	client.loop_stop()

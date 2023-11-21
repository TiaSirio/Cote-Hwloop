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

try:
	while True:
		# Possible extend to other commands if needed
		if msg == "execute":
			# tasks = []
			msg = ""
			taskCount = 0

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
					taskCount += 1
					startingTimestamp = str(timestamp_ms())
					#print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat))
					arguments = []

					# Divide the arguments
					if ";" in program:
						arguments = program.split(";")
						for i in range(0, len(arguments)):
							if not arguments[i]:
								arguments[i] = "".join(resultsOfTask)
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
						#totalResultOfTask = []
						line = proc.stdout.readline()
						if not line:
							break
						resultsOfTask.append(line.rstrip())
					resultsOfTaskString = ",".join(resultsOfTask)
					client.publish(mqttAppData + str(phSat) + "/" + str(taskCount) + "/" + str(sat), resultsOfTaskString)

					# For only one result, do a for loop and then join to send all results to mqtt
					# resultOfTasks = proc.stdout.readline()
					# client.publish(mqttNonFunc + str(sat), "".join(resultOfTasks))

					# resultsOfTasks.append(proc.stdout.readline())
					# result = subprocess.run([execString], stdout=subprocess.PIPE, encoding="utf-8")
					# resultsOfTasks.append(result)
					# print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat) + " - Ending at " + endingTimestamp + " with results " + proc.stdout.readline())

					# Send duration of the program to the simulation through MQTT
					duration = int(endingTimestamp) - int(startingTimestamp)
					client.publish(mqttDuration + str(phSat) + "/" + str(taskCount) + "/" + str(sat), str(duration))

					# Read non-func data and directly send each saved instance of non-func data to the simulation through MQTT
					with open(fileNonFunc, "r") as file:
						#print("Reading non functional values")
						lines = file.readlines()
						fcntl.flock(file, fcntl.LOCK_EX)
						for line in reversed(lines):
							# nonFuncValues = []
							nonFuncValues = line.rstrip("\n").split(",")
							# if int(nonFuncValues[0]) <= int(1684154133480) and int(nonFuncValues[0]) >= int(1684154131347):
							if int(nonFuncValues[0]) <= int(endingTimestamp) and int(nonFuncValues[0]) >= int(startingTimestamp):
								nonFuncValues.pop(0)
								# print(nonFuncValues)
								client.publish(mqttNonFunc + str(phSat) + "/" + str(taskCount) + "/" + str(sat), ",".join(nonFuncValues))
								# nonFuncValues = list(map(float, nonFuncValues))
								# nonFuncList.append(nonFuncValues)
							# elif int(nonFuncValues[0]) < int(1684154131347):
							elif int(nonFuncValues[0]) < int(startingTimestamp):
								# tasks.append(calculate_mean(nonFuncList))
								# nonFuncList = []
								break
						fcntl.flock(file, fcntl.LOCK_UN)
				# print(tasks)

				# tasks = [[str(insel) for insel in elem] for elem in tasks]
				# tasks = [",".join(elem) for elem in tasks]
				# finalTasks = ";".join(tasks)
				# print(finalTasks)
				# print(resultsOfTasks)
				# finalResultsOfTasks = ",".join(resultsOfTasks)
				# print(finalResultsOfTasks)
				# client.publish(mqttAppData + str(sat), finalTasks)
				# client.publish(mqttNonFunc + str(sat), finalResultsOfTasks)
				client.loop_start()
		
		time.sleep(1)

except KeyboardInterrupt:
	print("exiting")
	client.disconnect()
	client.loop_stop()

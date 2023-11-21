import paho.mqtt.client as mqtt
import time
import os
import subprocess
import fcntl
import sys
import random


msg = ""
sat = 0
nonFuncList = []
payloadList = []
tasks = []
dataSent = False



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
# Once the instance of satellite is found -> add a - at the start of the line
def search_in_mapper_multiple(sat, jobMultiple):
    file = open(fileMapper, "r+")
    returnVal = []
    linesFile = file.readlines()
    file.seek(0)
    file.truncate()
    firstJobFound = False
    jobAlreadyExecuted = False
    counterJob = -1
    for line in linesFile:
        # Reading programs to execute from the mapper
        values = line.rstrip("\n").split(",")
        if values[0] == "-":
            if sat == int(values[1]):
                counterJob += 1
            if counterJob == jobMultiple:
                jobAlreadyExecuted = True
            file.write(line)
        else:
            # Delete the line of the programs we are going to execute
            if sat == int(values[0]):
                counterJob += 1
            if sat == int(values[0]) and not firstJobFound and counterJob == jobMultiple and not jobAlreadyExecuted:
                values.pop(0)
                returnVal = values.copy()
                firstJobFound = True
                file.write("-," + line)
            else:
                file.write(line)
            #values = []
    file.close()
    if not firstJobFound:
        print("Instance of satellite not found!")
    if jobAlreadyExecuted:
        print("Job already executed!")
        returnVale = []
    return returnVal



def on_connect(cl, userdata, flags, rc):
    if rc == 0:
        cl.subscribe(mqttTopic + str(phSat) + "/#")
        #print(mqttTopic + str(phSat) + "/#")
        print("Connected to broker")
    else:
        print("Connection failed")



def flip_bytes(data, encoding='utf-8'):
    data_bytes = data.encode(encoding)
    flipped_data = bytearray(data_bytes)

    for i in range(len(flipped_data)):
        flipped_data[i] ^= 0xFF  # XOR each byte with 0xFF to flip its bits

    return flipped_data.decode(encoding)



def flip_bytes_program(task, errorRatio):
    with open(task, "rb") as file:
        data = bytearray(file.read())

    for i in range(len(data)):
        if random.uniform(0.00001, 1) < errorRatio:
            data[i] = random.randint(0, 255)

    with open(task, "wb") as file:
        file.write(data)



def on_message(cl, userdata, message):
    #print("Received message: " + str(msg.payload.decode("utf-8") + ", on topic: " + msg.topic))
    global msg
    global sat
    global jobMultiple

    msg = message.payload.decode("utf-8")
    print(msg)
    if single:
        sat = int("".join(message.topic.split("/")[-1:]))
    else:
        sat = int("".join(message.topic.split("/")[-2]))
        jobMultiple = int("".join(message.topic.split("/")[-1:]))



if len(sys.argv) != 18:
    print("Missing argument: \"s for SingleJob or m for MultipleJobs\", \"Number of Physical satellite\", \"MQTT address\", \"MQTT port\", \"MQTT topic commands\", \"MQTT topic duration\","
          "\"MQTT topic non-functional data\", \"MQTT topic payload\", \"MQTT topic appdata\", \"Mapper file name\", \"Client ID\", \"Execute commands\", \"No data message\""
          ", \"File non-functional\", \"File payload\", \"Tasks directory\" and \"radiationErrorRatio\"!")
    sys.exit()

jobMultiple = -1
if sys.argv[1] == "s":
    single = True
else:
    single = False

phSat = sys.argv[2]

mqttBroker = sys.argv[3]
mqttPort = int(sys.argv[4])

mqttTopic = sys.argv[5]
mqttDuration = sys.argv[6]
mqttNonFunc = sys.argv[7]
mqttPayload = sys.argv[8]
mqttAppData = sys.argv[9]

fileMapper = sys.argv[10]
clientName = sys.argv[11]
executeCommand = sys.argv[12]

noDataMessage = sys.argv[13]

fileNonFunc = sys.argv[14]
filePayload = sys.argv[15]
tasksDir = sys.argv[16]
radiationErrorRatio = float(sys.argv[17])


os.chdir(tasksDir)

# Connect to MQTT broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBroker, port=mqttPort)
client.loop_start()
resultsOfTask = []

outputsOfPrograms = {}
errorFound = False

try:
    while True:
        # Possible extend to other commands if needed
        if msg == executeCommand:
            # tasks = []
            msg = ""
            taskCount = 0
            errorFound = False
            # New job is started
            outputsOfPrograms = {}

            # Search if the instance of satellite needs to execute some programs
            if single:
                programsToExecute = search_in_mapper_single(sat)
            else:
                programsToExecute = search_in_mapper_multiple(sat, jobMultiple)

            if not programsToExecute:
                # Instance of satellite has finished to work
                client.publish(mqttDuration + str(phSat) + "/" + str(sat), noDataMessage)
                print("Skipping instance of satellite!")
            else:
                client.loop_stop()
                for program in programsToExecute:
                    taskCount += 1
                    if errorFound:
                        client.publish(mqttDuration + str(phSat) + "/" + str(sat), noDataMessage)
                    else:
                        startingTimestamp = str(timestamp_ms())
                        #print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat))
                        arguments = []

                        # Divide the arguments
                        if ";" in program:
                            # Write the regex to split except when double quotes
                            arguments = program.split(";")
                            for i in range(1, len(arguments)):
                                if '"' in arguments[i]:
                                    temp = arguments[i]
                                    arguments[i] = temp[1:-1]
                                else:
                                    # Given the topological sorting, there is always the task
                                    # If I need as argument, the output of a previous task, I search it in the map and then add it to the arguments
                                    if arguments[i] in outputsOfPrograms:
                                        arguments[i] = outputsOfPrograms[arguments[i]]
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

                        # Send only the last result
                        resultsOfTaskString = resultsOfTask[-1]

                        # Flip the bytes of the output based on a radiationErrorRatio
                        if random.random() < radiationErrorRatio:
                            #resultsOfTaskString = flip_bytes(resultsOfTaskString)
                            errorFound = True

                        client.publish(mqttAppData + str(phSat) + "/" + str(sat) + "/" + str(taskCount), resultsOfTaskString)
                        resultsOfTask = []

                        # Adding result to a map
                        outputsOfPrograms[program] = resultsOfTaskString

                        # For only one result, do a for loop and then join to send all results to mqtt
                        # resultOfTasks = proc.stdout.readline()
                        # client.publish(mqttNonFunc + str(sat), "".join(resultOfTasks))

                        # resultsOfTasks.append(proc.stdout.readline())
                        # result = subprocess.run([execString], stdout=subprocess.PIPE, encoding="utf-8")
                        # resultsOfTasks.append(result)
                        # print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat) + " - Ending at " + endingTimestamp + " with results " + proc.stdout.readline())

                        # Send duration of the program to the simulation through MQTT
                        duration = int(endingTimestamp) - int(startingTimestamp)
                        client.publish(mqttDuration + str(phSat) + "/" + str(sat) + "/" + str(taskCount), str(duration))

                        # Read non-func data and directly send the non-func data during the task execution to the simulation through MQTT
                        with open(fileNonFunc, "r+") as file:
                            #print("Reading non functional values")
                            lines = file.readlines()

                            # Remove all lines in the file, otherwise the memory fills up too quickly
                            file.seek(0)
                            file.truncate()

                            fcntl.flock(file, fcntl.LOCK_EX)
                            for line in reversed(lines):
                                # nonFuncValues = []
                                nonFuncValues = line.rstrip("\n").split(",")
                                # if int(nonFuncValues[0]) <= int(1684509377453) and int(nonFuncValues[0]) >= int(1684509376974):
                                if int(nonFuncValues[0]) <= int(endingTimestamp) and int(nonFuncValues[0]) >= int(startingTimestamp):
                                    nonFuncList.append(",".join(nonFuncValues))
                                # elif int(nonFuncValues[0]) < int(1684509376974):
                                elif int(nonFuncValues[0]) < int(startingTimestamp):
                                    client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount), ";".join(nonFuncList))
                                    # print(";".join(nonFuncList))
                                    nonFuncList = []
                                    dataSent = True
                                    break
                            fcntl.flock(file, fcntl.LOCK_UN)
                            if not dataSent:
                                client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount), ";".join(nonFuncList))
                                nonFuncList = []
                            else:
                                dataSent = False
                        #print("\n")
                        # Read payload data and directly send the payload data during the task execution to the simulation through MQTT
                        with open(filePayload, "r+") as file:
                            #print("Reading non functional values")
                            lines = file.readlines()

                            # Remove all lines in the file, otherwise the memory fills up too quickly
                            file.seek(0)
                            file.truncate()

                            fcntl.flock(file, fcntl.LOCK_EX)
                            for line in reversed(lines):
                                # nonFuncValues = []
                                nonFuncPayload = line.rstrip("\n").split(",")
                                # if int(nonFuncPayload[0]) <= int(1684516312623) and int(nonFuncPayload[0]) >= int(1684516312466):
                                if int(nonFuncPayload[0]) <= int(endingTimestamp) and int(nonFuncPayload[0]) >= int(startingTimestamp):
                                    payloadList.append(",".join(nonFuncPayload))
                                # elif int(nonFuncPayload[0]) < int(1684516312466):
                                elif int(nonFuncPayload[0]) < int(startingTimestamp):
                                    client.publish(mqttPayload + str(phSat) + "/" + str(sat) + "/" + str(taskCount), ";".join(payloadList))
                                    # print(";".join(payloadList))
                                    payloadList = []
                                    dataSent = True
                                    break
                            fcntl.flock(file, fcntl.LOCK_UN)
                            if not dataSent:
                                client.publish(mqttPayload + str(phSat) + "/" + str(sat) + "/" + str(taskCount), ";".join(payloadList))
                                payloadList = []
                            else:
                                dataSent = False
                client.loop_start()

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    client.disconnect()
    client.loop_stop()

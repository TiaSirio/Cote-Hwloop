import paho.mqtt.client as mqtt
import time
import os
import subprocess
import fcntl
import sys
import random
import signal

msg = ""
sat = 0
nonFuncList = []
payloadList = []
tasks = []
dataSent = False
map_sequential = {}


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


def updateSequentialConfFile(target_key):
    if target_key in map_sequential:
        map_sequential[target_key] += 1
    else:
        map_sequential[target_key] = 1


def readSequentialConfFile(target_key):
    return target_key[map_sequential] if target_key in map_sequential else 0


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
            # values = []
    file.close()
    if not firstJobFound:
        print("Instance of satellite not found!")
    if jobAlreadyExecuted:
        print("Job already executed!")
        returnVale = []
    return returnVal


# Read conf file for position of the input file
def readConfFile(pathToFile):
    dictConf = {}
    with open(pathToFile, "r") as fileConf:
        lines = fileConf.readlines()
        lines = [line.rstrip().split("=") for line in lines]
        for line in lines:
            dictConf[line[0]] = line[1]
    return dictConf


def on_connect(cl, userdata, flags, rc):
    if rc == 0:
        cl.subscribe(mqttTopic + str(phSat) + "/#")
        # print(mqttTopic + str(phSat) + "/#")
        print("Connected to broker")
    else:
        print("Connection failed")


def on_message(cl, userdata, message):
    # print("Received message: " + str(msg.payload.decode("utf-8") + ", on topic: " + msg.topic))
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


if len(sys.argv) != 33:
    print("Missing argument: \"s for SingleJob or m for MultipleJobs\", \"Number of Physical satellite\""
          ", \"MQTT address\", \"MQTT port\", \"MQTT topic commands\", \"MQTT topic duration\""
          ", \"MQTT topic non-functional data\", \"MQTT topic payload\", \"MQTT topic appdata\", \"Mapper file name\""
          ", \"Client ID\", \"Execute commands\", \"No data message\", \"File non-functional\", \"File payload\""
          ", \"Tasks directory\", \"radiationErrorRatio\", \"errorMessage\", \"conf file tasksExecutables\""
          ", \"conf file tasksDataset\", \"conf file tasksResults\", \"conf type of file\""
          ", \"Fault choice\", \"Output cleaner bash\", \"Fault creator\", \"Execute faulted task\""
          ", \"Execute faulted task for all inputs\", \"Execute faulted task for sequential inputs\""
          ", \"Execute task for all inputs\", \"Execute task for sequential inputs\""
          ", \"Max time to wait\", and \"Task to repeat configuration file\"!")
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
errorMessage = sys.argv[18]
confFileExecutable = sys.argv[19]
confFileDataset = sys.argv[20]
confFileResult = sys.argv[21]
confTypeOfFile = sys.argv[22]
faultChoice = sys.argv[23]
outputCleanerBash = sys.argv[24]
faultCreatorBash = sys.argv[25]
executeFaultedTaskBash = sys.argv[26]
executeFaultedTaskAllInputsBash = sys.argv[27]
executeFaultedTaskSequentialInputsBash = sys.argv[28]
executeTaskAllInputsBash = sys.argv[29]
executeTaskSequentialInputsBash = sys.argv[30]
maxTimeBeforeStopRadiatedProgram = int(sys.argv[31])
confRepeatProgram = sys.argv[32]

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

allInputs = False

confMapExecutable = readConfFile(confFileExecutable)
confMapDataset = readConfFile(confFileDataset)
confMapResult = readConfFile(confFileResult)
confMapTypeOfFile = readConfFile(confTypeOfFile)
confMapRepeatProgram = readConfFile(confRepeatProgram)

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
                #client.loop_stop()

                # Clean previous execution
                cleanList = ["./" + outputCleanerBash]
                procClean = subprocess.Popen(cleanList, stdout=subprocess.PIPE, encoding="utf-8")
                procClean.wait()

                for program in programsToExecute:
                    allInputs = False
                    errorFound = False
                    taskCount += 1
                    # print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat))
                    arguments = []
                    temp = ''

                    # Divide the arguments
                    if ";" in program:
                        # Write the regex to split except when double quotes
                        arguments = program.split(";")
                        for i in range(1, len(arguments)):
                            if '"' in arguments[i]:
                                temp = arguments[i]
                                arguments[i] = temp[1:-1]
                            else:
                                # Given the topological sorting, there is always the task If I need as argument
                                # the output of a previous task
                                # I search it in the map and then add it to the arguments
                                if arguments[i] in outputsOfPrograms:
                                    arguments[i] = outputsOfPrograms[arguments[i]]
                    else:
                        arguments.append(program)

                    savedProgramOutputName = arguments[0]

                    # Exec python or c programs
                    if arguments[0].endswith(".py"):
                        arguments[0] = confMapExecutable[arguments[0]]
                        if arguments[0] in confMapResult:
                            if confMapResult[arguments[0]] is not None:
                                arguments.insert(1, confMapResult[arguments[0]])
                        if arguments[0] in confMapDataset:
                            if confMapDataset[arguments[0]] is not None:
                                arguments.insert(1, confMapDataset[arguments[0]])
                        execString = "python3"
                        arguments.insert(0, execString)
                    # Execute the task using a script
                    elif arguments[0].startswith("?"):
                        # Delete input and output name files
                        arguments.pop(1)
                        arguments.pop(1)
                        temp = arguments[0]
                        typeOfScriptToUse = int(temp[1])
                        temp = temp[2:]
                        arguments.pop(0)
                        # Simulate radiation error
                        if random.random() < radiationErrorRatio:
                            errorFound = True
                            createTaskFault = ["./" + faultCreatorBash, faultChoice, confMapExecutable[temp]]

                            # Create faulty tasks caused by radiation.
                            procFault = subprocess.Popen(createTaskFault, stdout=subprocess.PIPE, encoding="utf-8")
                            procFault.wait()

                            # Execute the task for all the images present in the database
                            if typeOfScriptToUse == 1:
                                allInputs = True
                                execString = "./" + executeFaultedTaskAllInputsBash
                            # Execute the task for sequential images present in the database
                            else:
                                execString = "./" + executeFaultedTaskSequentialInputsBash
                                sequential_input = readSequentialConfFile(str(phSat) + str(sat) + str(temp))
                                updateSequentialConfFile(str(phSat) + str(sat) + str(temp))
                            arguments.insert(0, execString)
                            if temp in confMapResult:
                                if confMapResult[temp] is not None:
                                    arguments.insert(1, confMapResult[temp])
                            if temp in confMapDataset:
                                if confMapDataset[temp] is not None:
                                    arguments.insert(1, confMapDataset[temp])
                            if typeOfScriptToUse != 1:
                                arguments.insert(1, sequential_input)
                            if temp in confMapTypeOfFile:
                                if confMapTypeOfFile[temp] is not None:
                                    arguments.insert(1, confMapTypeOfFile[temp])
                        # Same as above but without radiation errors
                        else:
                            programToExec = confMapExecutable[temp]
                            arguments.insert(0, programToExec)
                            if typeOfScriptToUse == 1:
                                execString = "./" + executeTaskAllInputsBash
                                arguments.insert(0, execString)
                            else:
                                execString = "./" + executeTaskSequentialInputsBash
                                arguments.insert(0, execString)
                                sequential_input = readSequentialConfFile(str(phSat) + str(sat) + str(temp))
                                updateSequentialConfFile(str(phSat) + str(sat) + str(temp))
                                arguments.insert(2, sequential_input)
                            if temp in confMapTypeOfFile:
                                if confMapTypeOfFile[temp] is not None:
                                    arguments.insert(2, confMapTypeOfFile[temp])
                            if temp in confMapResult:
                                if confMapResult[temp] is not None:
                                    arguments.insert(2, confMapResult[temp])
                            if temp in confMapDataset:
                                if confMapDataset[temp] is not None:
                                    arguments.insert(2, confMapDataset[temp])
                    # Same as above but following the input given to the task
                    else:
                        temp = arguments[0]
                        arguments.pop(0)
                        if random.random() < radiationErrorRatio:
                            errorFound = True
                            createTaskFault = ["./" + faultCreatorBash, faultChoice, confMapExecutable[temp]]

                            procFault = subprocess.Popen(createTaskFault, stdout=subprocess.PIPE, encoding="utf-8")
                            procFault.wait()

                            execString = "./" + executeFaultedTaskBash
                            # arguments.insert(0, confMapExecutable[temp])
                        else:
                            execString = "./" + confMapExecutable[temp]
                        arguments.insert(0, execString)
                        if temp in confMapResult:
                            if confMapResult[temp] is not None:
                                arguments.insert(1, confMapResult[temp])
                        if temp in confMapDataset:
                            if confMapDataset[temp] is not None:
                                arguments.insert(1, confMapDataset[temp])

                    time.sleep(2)
                    startingTimestamp = str(timestamp_ms())

                    programRepeated = False

                    if temp in confMapRepeatProgram:
                        if confMapRepeatProgram[temp] is not None:
                            programRepeated = True
                            for t in range(int(confMapRepeatProgram[temp])):
                                try:
                                    # Start subprocess and wait for the results
                                    proc = subprocess.Popen(arguments, start_new_session=True, stdout=subprocess.PIPE, encoding="utf-8")
                                    # Wait more if we have to execute the program for all input in the database
                                    if allInputs:
                                        timeToWaitTimeout = maxTimeBeforeStopRadiatedProgram * 3
                                    else:
                                        timeToWaitTimeout = maxTimeBeforeStopRadiatedProgram
                                    allInputs = False
                                    proc.wait(timeout=timeToWaitTimeout)
                                except Exception as e:
                                    # errorFound = True
                                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                    if not programRepeated:
                        try:
                            # Start subprocess and wait for the results
                            proc = subprocess.Popen(arguments, start_new_session=True, stdout=subprocess.PIPE, encoding="utf-8")
                            # Wait more if we have to execute the program for all input in the database
                            if allInputs:
                                timeToWaitTimeout = maxTimeBeforeStopRadiatedProgram * 3
                            else:
                                timeToWaitTimeout = maxTimeBeforeStopRadiatedProgram
                            allInputs = False
                            proc.wait(timeout=timeToWaitTimeout)
                        except Exception as e:
                            # errorFound = True
                            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

                    endingTimestamp = str(timestamp_ms())
                    time.sleep(2)
                    resultsOfTask = []


                    # Handle all output of a program
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        resultsOfTask.append(line.rstrip())

                    # If an error of the task or a radiation error has occurred, return error for the task
                    # if proc.returncode != 0 or errorFound:
                    if errorFound:
                        resultsOfTaskString = errorMessage
                        errorFound = False
                    # Send only the last result
                    else:
                        if len(resultsOfTask) == 0:
                            resultsOfTaskString = ""
                        resultsOfTaskString = resultsOfTask[-1]

                    # Send the applicative data in output from the task
                    client.publish(mqttAppData + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                   resultsOfTaskString)
                    resultsOfTask = []

                    # Adding result to a map
                    outputsOfPrograms[savedProgramOutputName] = resultsOfTaskString

                    # Send duration of the program to the simulation through MQTT
                    if programRepeated:
                        duration = (int(endingTimestamp) - int(startingTimestamp))/int(confMapRepeatProgram[temp])
                    else:
                        duration = int(endingTimestamp) - int(startingTimestamp)
                    client.publish(mqttDuration + str(phSat) + "/" + str(sat) + "/" + str(taskCount), str(duration))

                    # Read non-func data and directly send the non-func data during the task execution to the simulation through MQTT
                    with open(fileNonFunc, "r+") as file:
                        # print("Reading non functional values")
                        lines = file.readlines()

                        # Remove all lines in the file, otherwise the memory fills up too quickly
                        file.seek(0)
                        file.truncate()

                        #fcntl.flock(file, fcntl.LOCK_EX)
                        for line in reversed(lines):
                            nonFuncValues = line.rstrip("\n").split(",")
                            # if int(nonFuncValues[0]) <= int(1684509377453) and int(nonFuncValues[0]) >= int(1684509376974):
                            if int(nonFuncValues[0]) <= int(endingTimestamp) and int(nonFuncValues[0]) >= int(
                                    startingTimestamp):
                                nonFuncList.append(",".join(nonFuncValues))
                            # elif int(nonFuncValues[0]) < int(1684509376974):
                            elif int(nonFuncValues[0]) < int(startingTimestamp):
                                # Added a value to consider fraction of time in which the program is still working
                                nonFuncList.append(",".join(nonFuncValues))
                                # Sending non functional data
                                if programRepeated:
                                    nonFuncListToModify = []
                                    for elem in nonFuncList:
                                        split_elements = elem.split(',')
                                        float_elements = [float(e) for e in split_elements]
                                        nonFuncListToModify.append(float_elements)
                                    initialNonFuncTimestamp = str(nonFuncListToModify[-1][0])[:-2]
                                    finalNonFuncTimestamp = str(nonFuncListToModify[0][0])[:-2]
                                    transposed_matrix = list(map(list, zip(*nonFuncListToModify)))
                                    column_means = [sum(column) / len(column) for column in transposed_matrix]
                                    column_means.pop(0)
                                    finalNonFuncListToTransfer = [[finalNonFuncTimestamp], [initialNonFuncTimestamp]]
                                    for q in range(2):
                                        for elem in column_means:
                                            finalNonFuncListToTransfer[q].append(elem)
                                    finalNonFuncListToTransfer = [[str(subelement) for subelement in sublist] for sublist in finalNonFuncListToTransfer]
                                    listNonFuncWithStrings = [",".join(sublist) for sublist in finalNonFuncListToTransfer]

                                    client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                                   ";".join(listNonFuncWithStrings))
                                else:
                                    client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                                   ";".join(nonFuncList))
                                nonFuncList = []
                                dataSent = True
                                break
                        #fcntl.flock(file, fcntl.LOCK_UN)
                        if not dataSent:
                            # Sending non functional data
                            client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                           ";".join(nonFuncList))
                            nonFuncList = []
                        else:
                            dataSent = False
                    # Read payload data and directly send the payload data during the task execution to the simulation through MQTT
                    with open(filePayload, "r+") as file:
                        # print("Reading non functional values")
                        lines = file.readlines()

                        # Remove all lines in the file, otherwise the memory fills up too quickly
                        file.seek(0)
                        file.truncate()

                        #fcntl.flock(file, fcntl.LOCK_EX)
                        for line in reversed(lines):
                            nonFuncPayload = line.rstrip("\n").split(",")
                            # if int(nonFuncPayload[0]) <= int(1684516312623) and int(nonFuncPayload[0]) >= int(1684516312466):
                            if int(nonFuncPayload[0]) <= int(endingTimestamp) and int(nonFuncPayload[0]) >= int(
                                    startingTimestamp):
                                payloadList.append(",".join(nonFuncPayload))
                            # elif int(nonFuncPayload[0]) < int(1684516312466):
                            elif int(nonFuncPayload[0]) < int(startingTimestamp):
                                # Added a value to consider fraction of time in which the program is still working
                                payloadList.append(",".join(nonFuncPayload))
                                # Sending payload data
                                if programRepeated:
                                    payloadListToModify = []
                                    for elem in payloadList:
                                        split_elements = elem.split(',')
                                        float_elements = [float(e) for e in split_elements]
                                        payloadListToModify.append(float_elements)
                                    initialPayloadTimestamp = str(payloadListToModify[-1][0])[:-2]
                                    finalPayloadTimestamp = str(payloadListToModify[0][0])[:-2]
                                    transposed_matrix = list(map(list, zip(*payloadListToModify)))
                                    column_means = [sum(column) / len(column) for column in transposed_matrix]
                                    column_means.pop(0)
                                    finalPayloadListToTransfer = [[finalPayloadTimestamp], [initialPayloadTimestamp]]
                                    for q in range(2):
                                        for elem in column_means:
                                            finalPayloadListToTransfer[q].append(elem)
                                    finalPayloadListToTransfer = [[str(subelement) for subelement in sublist] for sublist in finalPayloadListToTransfer]
                                    listPayloadWithStrings = [",".join(sublist) for sublist in finalPayloadListToTransfer]

                                    client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                                   ";".join(listPayloadWithStrings))
                                else:
                                    client.publish(mqttPayload + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                                   ";".join(payloadList))
                                # print(";".join(payloadList))
                                payloadList = []
                                dataSent = True
                                break
                        #fcntl.flock(file, fcntl.LOCK_UN)
                        if not dataSent:
                            # Sending payload data
                            client.publish(mqttPayload + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                           ";".join(payloadList))
                            payloadList = []
                        else:
                            dataSent = False
                #client.loop_start()

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    client.disconnect()
    client.loop_stop()

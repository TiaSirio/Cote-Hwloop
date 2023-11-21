import paho.mqtt.client as mqtt
import time
import sys
from random import randint
import yaml
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
def search_in_mapper_multiple(sat, jobMultiple):
    file = open(fileMapper, "r")
    returnVal = []
    linesFile = file.readlines()
    for line in linesFile:
        # Reading programs to execute from the mapper
        values = line.rstrip("\n").split(",")
        if sat == int(values[0]) and int(values[1]) == jobMultiple:
            values.pop(0)
            values.pop(0)
            returnVal = values.copy()
    file.close()
    return returnVal


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
    print("TOPIC: " + message.topic)
    if single:
        sat = int("".join(message.topic.split("/")[-1:]))
    else:
        sat = int("".join(message.topic.split("/")[-2]))
        jobMultiple = int("".join(message.topic.split("/")[-1:]))


if len(sys.argv) == 16:
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
    radiationErrorRatio = float(sys.argv[14])
    defaultErrorString = sys.argv[15]
elif len(sys.argv) == 2:
    single = True
    phSat = sys.argv[1]

    mqttBroker = "broker.hivemq.com"
    mqttPort = 1883

    mqttTopic = "cubesatsim/commands/"
    mqttDuration = "cubesatsim/duration/"
    mqttNonFunc = "cubesatsim/nonfuncdata/"
    mqttPayload = "cubesatsim/payload/"
    mqttAppData = "cubesatsim/appdata/"

    fileMapper = "mapper.txt"
    clientName = "cubesat" + str(phSat)
    executeCommand = "execute"
    noDataMessage = "nodata"
    radiationErrorRatio = 0.01
    defaultErrorString = "ERROR"
else:
    print(
        "Missing argument: \"s for SingleJob or m for MultipleJobs\", \"Number of Physical satellite\", "
        "\"MQTT address\", \"MQTT port\", \"MQTT topic commands\", \"MQTT topic duration\","
        "\"MQTT topic non-functional data\", \"MQTT topic payload\", \"MQTT topic appdata\", \"Mapper file name\", "
        "\"Client ID\", \"Execute commands\", \"No data message\"!")
    print("Inserting default...")
    single = True
    phSat = 1

    mqttBroker = "broker.hivemq.com"
    mqttPort = 1883

    mqttTopic = "cubesatsim/commands/"
    mqttDuration = "cubesatsim/duration/"
    mqttNonFunc = "cubesatsim/nonfuncdata/"
    mqttPayload = "cubesatsim/payload/"
    mqttAppData = "cubesatsim/appdata/"

    fileMapper = "mapper.txt"
    clientName = "cubesat" + str(phSat)
    executeCommand = "execute"
    noDataMessage = "nodata"
    radiationErrorRatio = 0.01
    defaultErrorString = "ERROR"



# Read the YAML file

with open('tasksMeanValue.yaml', 'r') as file:
    data = yaml.safe_load(file)
taskMean = []
# Process each program
for task in data:
    for key, elementInTask in task.items():
        taskMean.append(elementInTask)

jobMultiple = -1

'''
app_data = "test"
duration = 0
non_func_data = "1684916665207,3.308,-0.200,3.536,0.000,3.936,0.000,5.028,-1.900,2.884,-0.100,0.984,-0.100,1.044,-0.300,2.968,-0.200,40.780;1684916665110,3.312,-0.200,3.528,0.000,3.936,0.000,5.028,-1.800,2.900,-0.100,0.984,-0.100,1.044,-0.300,2.944,-0.100,41.318;1684916665014,3.328,-0.100,3.524,0.000,3.936,0.100,5.012,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.932,-0.200,41.318;1684916664917,3.336,-0.100,3.516,0.000,3.936,0.000,5.032,-1.800,2.888,-0.100,0.988,-0.100,1.044,-0.300,2.944,-0.200,41.318;1684916664821,3.332,-0.100,3.508,0.000,3.936,0.000,5.032,-1.600,2.884,-0.100,0.988,-0.200,1.044,-0.300,2.968,-0.200,41.318;1684916664726,3.316,-0.100,3.504,0.000,3.936,0.000,5.024,-1.700,2.896,-0.100,0.988,-0.100,1.044,-0.300,2.940,-0.100,40.780;1684916664629,3.308,-0.200,3.516,0.000,3.936,0.000,5.032,-1.700,2.912,-0.100,0.988,-0.100,1.044,-0.300,2.928,-0.200,41.318;1684916664533,3.308,-0.100,3.524,0.000,3.936,0.000,5.032,-1.700,2.912,-0.100,0.988,-0.200,1.044,-0.300,2.948,-0.100,41.318;1684916664437,3.320,-0.100,3.532,0.000,3.936,0.000,5.008,-1.800,2.896,-0.200,0.984,-0.200,1.044,-0.300,2.972,-0.200,40.780;1684916664341,3.332,-0.100,3.536,0.000,3.936,0.000,5.016,-1.700,2.884,-0.100,0.984,-0.100,1.044,-0.300,2.972,-0.200,41.318;1684916664245,3.336,-0.100,3.540,0.000,3.936,0.000,5.004,-1.800,2.888,-0.100,0.984,-0.100,1.044,-0.300,2.948,-0.100,40.780;1684916664149,3.304,-0.100,3.540,0.000,3.936,0.000,5.008,-1.800,2.904,-0.100,0.984,-0.100,1.044,-0.300,2.932,-0.200,41.318;1684916664053,3.308,-0.200,3.540,0.000,3.936,0.000,5.000,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.940,-0.200,41.318;1684916663956,3.324,-0.100,3.536,0.000,3.936,0.000,5.008,-1.800,2.908,0.000,0.988,-0.100,1.044,-0.300,2.968,-0.200,40.780;1684916663860,3.336,-0.100,3.532,0.000,3.936,0.000,5.008,-1.800,2.888,-0.100,0.988,-0.100,1.044,-0.300,2.972,-0.200,41.318;1684916663764,3.332,-0.200,3.528,0.000,3.936,0.000,5.016,-1.800,2.880,-0.100,0.988,-0.100,1.044,-0.300,2.952,-0.200,40.780;1684916663667,3.320,-0.100,3.496,0.000,3.936,0.000,5.012,-1.800,2.892,-0.100,0.988,-0.100,1.044,-0.300,2.928,-0.200,41.318;1684916663571,3.308,-0.100,3.500,0.000,3.936,0.100,5.000,-1.800,2.912,-0.100,0.988,-0.200,1.044,-0.300,2.936,-0.200,41.318;1684916663475,3.308,-0.100,3.504,0.000,3.936,0.000,5.012,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.964,-0.200,40.780;1684916663379,3.316,-0.200,3.512,0.000,3.936,0.000,5.012,-1.800,2.880,-0.100,0.984,-0.100,1.044,-0.300,2.976,-0.200,41.318;1684916663283,3.332,-0.100,3.520,0.000,3.936,0.000,5.012,-1.800,2.892,-0.200,0.984,-0.100,1.044,-0.300,2.960,-0.200,41.318;1684916663187,3.336,-0.100,3.528,0.000,3.936,0.000,5.012,-1.800,2.912,-0.100,0.984,-0.100,1.044,-0.300,2.940,-0.200,40.780;1684916663091,3.324,-0.200,3.532,0.000,3.936,0.000,5.008,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.968,-0.200,41.318;1684916662995,3.312,-0.100,3.536,0.000,3.936,0.000,5.012,-1.800,2.900,-0.100,0.988,-0.100,1.044,-0.300,2.976,-0.100,40.780;1684916662899,3.308,-0.100,3.540,0.000,3.936,0.100,5.004,-1.800,2.884,-0.100,0.988,-0.200,1.044,-0.300,2.956,-0.200,40.780;1684916662802,3.312,-0.100,3.540,0.000,3.936,0.000,5.012,-1.900,2.884,-0.100,0.988,-0.100,1.044,-0.300,2.932,-0.200,41.856;1684916662706,3.336,-0.100,3.504,0.000,3.936,0.000,5.028,-1.600,2.900,-0.100,0.988,-0.100,1.044,-0.300,2.936,-0.200,40.780;1684916662610,3.320,-0.100,3.500,0.000,3.936,0.000,5.032,-1.600,2.916,-0.100,0.988,-0.200,1.044,-0.300,2.960,-0.100,40.780;1684916662514,3.308,-0.200,3.496,0.000,3.936,0.000,5.032,-1.600,2.912,-0.100,0.984,-0.200,1.044,-0.300,2.976,-0.200,41.318;1684916662418,3.308,-0.100,3.496,0.000,3.936,0.000,5.028,-1.600,2.892,-0.100,0.984,-0.200,1.044,-0.300,2.960,-0.200,41.856;1684916662321,3.312,-0.100,3.500,0.000,3.936,0.000,5.016,-1.800,2.880,-0.100,0.988,-0.100,1.044,-0.300,2.936,-0.100,41.318;1684916662225,3.328,-0.200,3.504,0.000,3.936,0.000,5.008,-1.600,2.888,-0.100,0.988,-0.100,1.044,-0.300,2.932,-0.200,41.318;1684916662129,3.336,-0.100,3.508,0.000,3.936,0.000,5.016,-1.600,2.908,-0.100,0.988,-0.100,1.044,-0.400,2.952,-0.200,41.318;1684916662032,3.324,-0.200,3.516,0.000,3.936,0.000,5.016,-1.600,2.916,-0.100,0.988,-0.100,1.044,-0.300,2.976,-0.200,40.780;1684916661936,3.308,-0.100,3.524,0.000,3.936,0.000,5.012,-1.800,2.904,-0.100,0.984,-0.100,1.044,-0.400,2.964,-0.200,40.780;1684916661839,3.300,-0.200,3.528,0.000,3.936,0.000,5.008,-1.800,2.888,-0.100,0.988,-0.200,1.044,-0.300,2.940,-0.200,40.780;1684916661675,3.332,-0.200,3.536,0.000,3.936,0.000,4.996,-1.800,2.904,-0.100,0.988,-0.100,1.044,-0.300,2.928,-0.200,41.318;1684916661578,3.316,-0.200,3.500,0.000,3.936,0.000,5.004,-1.800,2.904,-0.100,0.984,-0.200,1.044,-0.300,2.960,-0.200,40.780;1684916661482,3.304,-0.100,3.508,0.000,3.936,0.000,5.012,-1.800,2.884,-0.100,0.984,-0.200,1.044,-0.300,2.936,-0.100,40.780;1684916661385,3.300,-0.100,3.512,0.000,3.936,0.000,5.004,-1.800,2.904,-0.100,0.984,-0.100,1.044,-0.300,2.932,-0.100,40.780;1684916661287,3.308,-0.100,3.520,0.000,3.936,0.000,4.964,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.952,-0.200,40.780"
payload_data = "1684916665259,0.000,0.000,24.530,1001.110,101.540,49.340,0.000,-0.240,0.470,-0.070,0.040,0.980,-0.090,0.000,22.230,0.000,101.560;1684916665102,0.000,0.000,24.530,1001.140,101.310,49.340,0.000,0.310,-0.200,0.280,0.040,0.990,-0.100,0.000,22.620,0.000,101.560;1684916664945,0.000,0.000,24.530,1001.150,101.190,49.360,0.000,0.380,0.430,-0.060,0.040,0.990,-0.090,0.000,22.230,0.000,101.560;1684916664788,0.000,0.000,24.530,1001.140,101.310,49.360,0.000,-0.210,-0.200,-0.330,0.040,0.990,-0.100,0.000,22.620,0.000,101.560;1684916664630,0.000,0.000,24.530,1001.150,101.190,49.360,0.000,0.440,0.290,-0.100,0.040,0.990,-0.100,0.000,22.230,0.000,101.560;1684916664473,0.000,0.000,24.520,1001.130,101.380,49.360,0.000,-0.180,0.030,0.020,0.040,0.990,-0.100,0.000,21.830,0.000,101.560;1684916664316,0.000,0.000,24.530,1001.110,101.570,49.360,0.000,-0.140,-0.350,-0.320,0.040,0.990,-0.100,0.000,22.230,0.000,101.560;1684916664159,0.000,0.000,24.530,1001.170,101.050,49.360,0.000,-0.430,0.000,0.080,0.050,0.990,-0.100,0.000,21.830,0.000,101.560;1684916664002,0.000,0.000,24.530,1001.130,101.420,49.370,0.000,0.320,-0.050,0.260,0.040,0.990,-0.100,0.000,22.230,0.000,101.560;1684916663844,0.000,0.000,24.530,1001.130,101.420,49.360,0.000,0.340,0.370,-0.230,0.040,0.990,-0.090,0.000,21.830,0.000,101.560;1684916663688,0.000,0.000,24.530,1001.150,101.230,49.370,0.000,-0.430,-0.550,0.610,0.040,0.990,-0.100,0.000,22.230,0.000,101.560;1684916663530,0.000,0.000,24.530,1001.150,101.190,49.370,0.000,-0.120,-0.580,0.250,0.040,0.980,-0.090,0.000,22.620,0.000,101.560;1684916663373,0.000,0.000,24.530,1001.130,101.420,49.370,0.000,-0.070,-0.350,0.030,0.040,0.990,-0.090,0.000,22.230,0.000,101.560;1684916663216,0.000,0.000,24.530,1001.160,101.120,49.370,0.000,0.050,-0.430,-0.120,0.040,0.990,-0.100,0.000,21.830,0.000,101.560;1684916663059,0.000,0.000,24.530,1001.120,101.460,49.380,0.000,0.060,0.640,0.260,0.040,1.000,-0.090,0.000,21.440,0.000,101.560;1684916662902,0.000,0.000,24.530,1001.100,101.650,49.380,0.000,-0.150,-0.290,0.320,0.040,0.990,-0.090,0.000,22.230,0.000,101.560;1684916662745,0.000,0.000,24.530,1001.140,101.340,49.380,0.000,-0.490,0.270,-0.090,0.040,0.990,-0.080,0.000,21.830,0.000,101.560;1684916662587,0.000,0.000,24.530,1001.120,101.460,49.380,0.000,-0.200,-0.260,0.110,0.040,0.990,-0.100,0.000,21.440,0.000,101.560;1684916662430,0.000,0.000,24.530,1001.100,101.680,49.380,0.000,-0.060,0.600,-0.260,0.040,0.990,-0.090,0.000,21.830,0.000,101.560;1684916662273,0.000,0.000,24.520,1001.110,101.530,49.380,0.000,0.370,-0.260,0.060,0.050,0.990,-0.100,0.000,22.230,0.000,101.560;1684916662116,0.000,0.000,24.520,1001.060,101.980,49.380,0.000,-0.200,-0.350,0.190,0.040,0.990,-0.090,0.000,22.230,0.000,101.560;1684916661959,0.000,0.000,24.520,1001.100,101.640,49.380,0.000,-0.320,-0.060,0.050,0.040,0.990,-0.100,0.000,22.230,0.000,101.560;1684916661802,0.000,0.000,24.520,1001.130,101.410,49.380,0.000,-0.210,-0.030,0.200,0.050,0.990,-0.100,0.000,21.830,0.000,101.560;1684916661644,0.000,0.000,24.520,1001.090,101.750,49.380,0.000,0.190,-0.030,0.060,0.040,0.990,-0.100,0.000,21.830,0.000,101.560;1684916661487,0.000,0.000,24.520,1001.080,101.790,49.380,0.000,0.190,0.340,0.220,0.040,0.990,-0.080,0.000,21.830,0.000,101.560;1684916661330,0.000,0.000,24.520,1001.110,101.530,49.380,0.000,0.310,0.370,-0.200,0.040,0.990,-0.090,0.000,22.230,0.000,101.560"
'''

app_data = ""
duration = 0
non_func_data = ""
payload_data = ""

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBroker, port=mqttPort)
client.loop_start()

try:
    while True:
        # Possible extend to other commands if needed
        if msg == executeCommand:
            msg = ""
            taskCount = 0
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
                    # Search for mean value of the program

                    # Divide the arguments
                    if ";" in program:
                        # Write the regex to split except when double quotes
                        arguments = program.split(";")
                        relevantProgram = arguments[0]
                        if relevantProgram.startswith("?"):
                            relevantProgram = relevantProgram[2:]
                    else:
                        relevantProgram = program

                    # Take mean data from calculated data
                    for meanTask in taskMean:
                        if meanTask['name'] == relevantProgram:
                            non_func_data = meanTask['nonFuncData']
                            payload_data = meanTask['payloadData']
                            duration = meanTask['duration']
                            app_data = meanTask['appData']

                    dur = randint(1000, 5000)

                    taskCount += 1

                    time.sleep(dur/1000)

                    if random.random() < radiationErrorRatio:
                        app_data = "ERROR"

                    client.publish(mqttAppData + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                   str(app_data))

                    time.sleep(0.5)

                    client.publish(mqttDuration + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                   str(duration))

                    time.sleep(0.5)

                    client.publish(mqttNonFunc + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                   non_func_data)

                    time.sleep(0.5)

                    client.publish(mqttPayload + str(phSat) + "/" + str(sat) + "/" + str(taskCount),
                                   payload_data)

                    time.sleep(0.5)

                client.loop_start()

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    client.disconnect()
    client.loop_stop()

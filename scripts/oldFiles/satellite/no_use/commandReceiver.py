import paho.mqtt.client as mqtt
import time
import os
import subprocess

#mqttTopic = [("cubesatsim/nonfuncdata/#", 0), ("cubesatsim/appdata/#", 0)]
mqttTopic = "cubesatsim/commands/#"
mqttNonFunc = "cubesatsim/nonfuncdata/"
mqttAppData = "cubesatsim/appdata/"
fileName = "mapper.txt"
#fileName = "cexec/mapper.txt"
msg = ""
sat = 0



def timestamp_ms():
	return round(time.time() * 1000)




def search_in_mapper(sat):
	file = open(fileName, "r")
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




def on_connect(cl, userdata, flags, rc):
	if rc == 0:
		cl.subscribe(mqttTopic)
		print("Connected to broker")
	else:
		print("Connection failed")



def on_message(cl, userdata, message):
	#print("Received message: " + str(msg.payload.decode("utf-8") + ", on topic: " + msg.topic))
	global msg
	global sat
	
	msg = message.payload.decode("utf-8")
	sat = int("".join(message.topic.split("/")[-1:]))




mqttBroker = "broker.hivemq.com"

client = mqtt.Client("commandReceiver")
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBroker, port=1883)
client.loop_start()

try:
	while True:
		# Possible extend to other commands if needed
		if msg == "execute":
			msg == ""
			programsToExecute = search_in_mapper(sat)
			# print(programsToExecute)
			if not programsToExecute:
				print("Skipping instance of satellite!")
			else:
				client.loop_stop()
				for program in programsToExecute:
					startingTimestamp = str(timestamp_ms())
					print("Starting at " + startingTimestamp + " to exec " + program + " for instance " + str(sat))
					# Exec the programs
					
				client.loop_start()
		
		time.sleep(1)

except KeyboardInterrupt:
	print("exiting")
	client.disconnect()
	client.loop_stop()

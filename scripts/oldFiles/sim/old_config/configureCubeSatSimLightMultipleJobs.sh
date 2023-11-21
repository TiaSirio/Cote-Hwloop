#!/bin/bash

source simulation.conf

# Add rsync here
rsync -avh --delete cexec/ cubesatsim:/home/pi/CubeSatSim/simulationFiles/cexec/

# Compile programs
ssh cubesatsim "cd ~/CubeSatSim/simulationFiles/cexec && make && ./startSatelliteScripts.sh m 1 $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $satelliteNonFuncData $satellitePayloadData $satelliteTasksDir"
echo "Programs compiled"


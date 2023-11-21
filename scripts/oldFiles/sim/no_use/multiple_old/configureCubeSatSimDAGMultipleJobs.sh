#!/bin/bash

source simulation.conf

numberOfSatellite=$1
satVal="satellite${numberOfSatellite}"

sshToSat=$(grep "^$satVal=" phSatToUse.conf | cut -d'=' -f2)

# Rsync
#rsync -avh --delete cexec/ cubesatsim:/home/pi/CubeSatSim/simulationFiles/cexec/
if ! rsync -avh --delete cexec/ cubesatsim:/home/pi/CubeSatSim/simulationFiles/cexec/
then
  echo "rsync operation failed!"
  exit 1
fi

# Compile programs and execute satellite programs
#ssh cubesatsim "cd ~/CubeSatSim/simulationFiles/cexec && make && ./stopSatelliteScripts.sh && ./startSatelliteScriptsDAG.sh m 1 $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $satelliteNonFuncData $satellitePayloadData $satelliteTasksDir"
if ! ssh "$sshToSat" "cd ~/CubeSatSim/simulationFiles/cexec && make && ./startSatelliteScriptsDAG.sh m 1 $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $satelliteNonFuncData $satellitePayloadData $satelliteTasksDir $radiationErrorRatio" "$errorMessage"
then
  echo "SSH connection or remote command failed!"
  exit 1
fi

echo "Programs compiled"
exit 0
#!/bin/bash

cd ../cube_sat_scripts/sim
source simulation.conf

satDirString="$(printf "%03d" $satellite)/"
fromInnerScriptsToSimulationString="../../${dirSims}${simulationMMul}${scriptsDir}"
fromInnerScriptsToSimulationDataString="../../${dirSims}${simulationMMul}${dirData}${satDirString}"
fromSimulationToMapper="../../../${scriptsDir}${fromScriptsToSimScripts}${execDir}${mapperFileName}"

previous_position=$(pwd)

# Run simulation
cd "$fromInnerScriptsToSimulationString"
echo "HWLoop simulation is running."
./hwloopMMul.sh "$satellite" "$jobs" "$mapperType" "$fromSimulationToMapper" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopic" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload" "$noDataMessage" "$orbitDuration" "$errorMessage" "$energyHarvestMaximumVolt" "$energyHarvestMaximumCurrent" "$energyStorageMaximumCapacity" "$energyStorageEsr" "$timeToUpdateTheSimulation"

sleep 2

cd "$previous_position"

cp "${execDir}${mapperFileName}" "${fromInnerScriptsToSimulationDataString}"
cp "${simulationConfFileName}" "${fromInnerScriptsToSimulationDataString}"
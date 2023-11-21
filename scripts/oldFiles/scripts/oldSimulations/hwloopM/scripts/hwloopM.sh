#!/bin/bash
#
# A bash scripts that runs the simulation with a defined instances of satellites,
# a defined number of jobs and a maximum number of tasks per job.
# The instances of satellite will always have the same job.
# All the calculation are done at the simulation side and each task is sent back singularly using mqtt.

# Set up simulation parameters and configure physical satellite
cd cube_sat_scripts/sim
source simulation.conf

cd "$execDir"
./makeInEverySubdir.sh
./tasksConfGenerator.sh
./cleanInEverySubdir.sh
cd ../

./DAGMapperGenerator.sh
resultMapper=$?

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

if [ "$resultMapper" -gt 0 ]
then
  echo "Error while generating the mapper"
  exit 1
fi

phFile="physicalSatellite.conf"
usePhFile="phSatToUse.conf"

# Copy physical satellites to use in a new conf file
head -n "$physicalInstances" "$phFile" > "$usePhFile"

# Clean the satellite if a previous execution didn't clean them
#new_conf_file="cleanPhysicalSatellite.conf"
#if [ -s "$new_conf_file" ]; then
#    ./hwloopStopPhysicalSatellites.sh "$stopCubeSatSimPrograms"
#    resultStopping=$?
#    if [ "$resultStopping" -gt 0 ]
#    then
#      echo "Error while stopping the satellite"
#      exit 1
#    fi
#fi


./hwloopConfigurePhysicalSatellites.sh "$configureCubeSatSim"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while starting in the simulation"
  exit 1
fi

# $HOME/git-repos/cote-hwloop/scripts/cube_sat_scripts/sim/
# Create records of satellites to clean
#./createConfSatelliteToClean.sh

satDirString="$(printf "%03d" $satellite)/"
fromInnerScriptsToSimulationString="../../${dirSims}${simulationM}${scriptsDir}"
fromInnerScriptsToSimulationDataString="../../${dirSims}${simulationM}${dirData}${satDirString}"
fromSimulationToMapper="../../../${scriptsDir}${fromScriptsToSimScripts}${execDir}${mapperFileName}"

previous_position=$(pwd)

# Run simulation
cd "$fromInnerScriptsToSimulationString"
echo "HWLoop simulation is running."
./hwloopM.sh "$satellite" "$jobs" "$mapperType" "$fromSimulationToMapper" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopic" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload" "$noDataMessage" "$orbitDuration" "$errorMessage" "$energyHarvestMaximumVolt" "$energyHarvestMaximumCurrent" "$energyStorageMaximumCapacity" "$energyStorageEsr"

sleep 2

cd "$previous_position"

cp "${execDir}${mapperFileName}" "${fromInnerScriptsToSimulationDataString}"
cp "${simulationConfFileName}" "${fromInnerScriptsToSimulationDataString}"

# Stop running programs on the satellite
#./stopSatellitePrograms.sh
./hwloopStopPhysicalSatellites.sh "$stopCubeSatSimPrograms"
resultStopping=$?
if [ "$resultStopping" -gt 0 ]
then
  echo "Error while stopping the satellite"
  exit 1
fi

# Once cleaned remove them
> "$usePhFile"

cd ../..
echo "Processing logs..."
./process_hwloop_logs_m.sh "$satellite"

echo "Generating plots..."
./plots_generation_m_hwloop.sh "$satellite"
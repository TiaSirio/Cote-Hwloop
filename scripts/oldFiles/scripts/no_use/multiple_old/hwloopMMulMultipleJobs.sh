#!/bin/bash
#
# A bash scripts that runs the simulation with a defined instances of satellites,
# a defined number of jobs and a maximum number of tasks per job.
# The instances of satellite will always have a different job.
# All the calculation are done at the simulation side and each task is sent back singularly using mqtt.


# Set up simulation parameters and configure physical satellite
cd cube_sat_scripts/sim
source simulation.conf
./DAGMapperGeneratorMultipleJobs.sh
resultMapper=$?

if [ "$resultMapper" -gt 0 ]
then
  echo "Error while generating the mapper"
  exit 1
fi

phFile="physicalSatellite.conf"
usePhFile="phSatToUse.conf"

# Copy physical satellites to use in a new conf file
head -n "$physicalInstances" "$phFile" > "$usePhFile"

./hwloopConfigurePhysicalSatellites.sh "$configureCubeSatSimMultipleJobs"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while starting in the simulation"
  exit 1
fi

satDirString="$(printf "%03d" $satellite)/"
fromInnerScriptsToSimulationString="../../${dirSims}${simulationMMul}${scriptsDir}"
fromInnerScriptsToSimulationDataString="../../${dirSims}${simulationMMul}${dirData}${satDirString}$"
fromSimulationToMapper="../../../${scriptsDir}${fromScriptsToSimScripts}${execDir}${mapperFileName}"

previous_position=$(pwd)

# Run simulation
cd "$fromInnerScriptsToSimulationString"
echo "HWLoop simulation is running."
./hwloopDAG.sh "$satellite" "$jobs" "m" "$fromSimulationToMapper" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopic" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload" "$noDataMessage" "$orbitDuration" "$errorMessage"

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
./process_hwloop_logs_m_mul_multiple.sh "$satellite"

echo "Generating plots..."
./plots_generation_m_mul_hwloop.sh "$satellite"
#!/bin/bash
#
# A bash scripts that runs the simulation with a defined instances of satellites,
# a defined number of jobs and a maximum number of tasks per job.
# The instances of satellite will always have the same job.
# All the calculation are done at the simulation side and each task is sent back singularly using mqtt.
for i in {1..4}
do
# Set up simulation parameters and configure physical satellite
cd ../cube_sat_scripts/sim
source simulation.conf

cd "$execDir"
./"$makeForEveryTask"
./"$generateTaskConfFile"
./"$cleanForEveryTask"
cd ../

./"$generateMapperFile"
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

phFile="$physicalSatelliteConf"
usePhFile="$physicalSatelliteToUseConf"

# Copy physical satellites to use in a new conf file
# head -n "$physicalInstances" "$phFile" > "$usePhFile"


./hwloopConfigurePhysicalSatellites.sh "configureCubeSatSimEvaluation.sh"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while starting in the simulation"
  exit 1
fi

satDirString="$(printf "%03d" $satellite)/"
fromInnerScriptsToSimulationString="../../${dirSims}${simulationMMul}${scriptsDir}"
fromInnerScriptsToSimulationDataString="../../${dirSims}${simulationMMul}${dirData}${satDirString}"
fromSimulationToMapper="../../../${scriptsDir}${fromScriptsToSimScripts}${execDir}${mapperFileName}"

previous_position=$(pwd)

echo "Waiting for satellites connection..."
# Give the time to the nanosat to connect to the broker

value_sleep=60

# Check if the value in $temp is greater than 10
# if [ "$satellite" -gt "$value_sleep" ]; then
#     value_sleep=$satellite
# fi

sleep "$value_sleep"

# Run simulation
cd "$fromInnerScriptsToSimulationString"
echo "HWLoop simulation is running."
start_time=$(date +%s)
if ! ./"$hwloopMultiThreadSimulation" "$satellite" "$jobs" "$mapperType" "$fromSimulationToMapper" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopicMultithread" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload" "$noDataMessage" "$orbitDuration" "$errorMessage" "$energyHarvestMaximumVolt" "$energyHarvestMaximumCurrent" "$energyStorageMaximumCapacity" "$energyStorageEsr" "$timeToUpdateTheSimulation"
then
  echo "Execution failed!"
  exit 1
fi
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "The simulation run for $duration seconds."

sleep 2

cd "$previous_position"

echo "$duration" > "${fromInnerScriptsToSimulationDataString}/simulation_duration.txt"
cp "${execDir}${mapperFileName}" "${fromInnerScriptsToSimulationDataString}"
cp "${simulationConfFileName}" "${fromInnerScriptsToSimulationDataString}"

evaluationSat="$(printf "%03d" $physicalInstances)"
# Evaluation
echo "$duration" >> "../../evaluation/results/scalability/system_scalability/$evaluationSat/simulation_duration.txt"

# Stop running programs on the satellite
#./stopSatellitePrograms.sh
./"$stopCubeSatSimProgramsMultipleSatellites" "stopSatelliteProgramsEvaluation.sh"
resultStopping=$?
if [ "$resultStopping" -gt 0 ]
then
  echo "Error while stopping the satellite"
  exit 1
fi

# Once cleaned remove them
> "$usePhFile"

cd ../../hwloopMMul/
# echo "Processing logs..."
# ./"$processMultiThreadSimulation" "$satellite"

# echo "Generating plots..."
# ./"$plotsMultiThreadSimulation" "$satellite"

sleep 2
done
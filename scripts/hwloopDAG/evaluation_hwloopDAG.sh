#!/bin/bash
#
# A bash scripts that runs the simulation with a defined instances of satellites,
# a defined number of jobs and a maximum number of tasks per job.
# The instances of satellite will always have the same job.
# All the calculation are done at the simulation side and each task is sent back singularly using mqtt.

for i in {1..1}
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
head -n "1" "$phFile" > "$usePhFile"

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

./"$configureCubeSatSim" 1
#./hwloopConfigurePhysicalSatellites.sh "$configureCubeSatSimSingleJob"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while starting in the simulation"
  exit 1
fi

#cd $HOME/git-repos/cote-hwloop/scripts/cube_sat_scripts/sim/
# Create records of satellites to clean
#./createConfSatelliteToClean.sh

satDirString="$(printf "%03d" $satellite)/"
fromInnerScriptsToSimulationString="../../${dirSims}${simulationDAG}${scriptsDir}"
fromInnerScriptsToSimulationDataString="../../${dirSims}${simulationDAG}${dirData}${satDirString}"
fromSimulationToMapper="../../../${scriptsDir}${fromScriptsToSimScripts}${execDir}${mapperFileName}"

previous_position=$(pwd)

echo "Waiting for satellite connection..."
# Give the time to the nanosat to connect to the broker
sleep 10

# Run simulation
cd "$fromInnerScriptsToSimulationString"
echo "HWLoop simulation is running."
start_time=$(date +%s)
if ! ./"$hwloopSingleThreadSimulation" "$satellite" "$jobs" "$mapperType" "$fromSimulationToMapper" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopic" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload" "$noDataMessage" "$orbitDuration" "$errorMessage" "$energyHarvestMaximumVolt" "$energyHarvestMaximumCurrent" "$energyStorageMaximumCapacity" "$energyStorageEsr" "$timeToUpdateTheSimulation"
then
  echo "Execution failed!"
  exit 1
fi
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "The simulation run for $duration seconds."

sleep 2

cd "$previous_position"

evaluationSat="$(printf "%03d" $satellite)"
echo "$duration" > "${fromInnerScriptsToSimulationDataString}/simulation_duration.txt"
cp "${execDir}${mapperFileName}" "${fromInnerScriptsToSimulationDataString}"
cp "${simulationConfFileName}" "${fromInnerScriptsToSimulationDataString}"

# Stop running programs on the satellite
./"$stopCubeSatSimPrograms" 1
resultStopping=$?
if [ "$resultStopping" -gt 0 ]
then
  echo "Error while stopping the satellite"
  exit 1
fi

# Once cleaned remove them
> "$usePhFile"

cd ../../hwloopDAG/
echo "Processing logs..."
./"$processSingleThreadSimulation" "$satellite"

source_file="../${dirSims}${simulationDAG}/logsProcessed/$evaluationSat/consumption/hwloop_total_consumption_satellite.csv"
destination_dir="../evaluation/results/accuracy/consumption/"

destination_file="hwloop_total_consumption_satellite.csv"
count=1

while [ -e "${destination_dir}/${destination_file}" ]; do
    destination_file="hwloop_total_consumption_satellite_${count}.csv"
    ((count++))
done

cp "$source_file" "${destination_dir}/${destination_file}"

source_file2="../${dirSims}${simulationDAG}/logsProcessed/$evaluationSat/time/hwloop_total_time.csv"
destination_dir2="../evaluation/results/accuracy/time/"

destination_file2="hwloop_total_time.csv"
count2=1

while [ -e "${destination_dir2}/${destination_file2}" ]; do
    destination_file2="hwloop_total_time_${count2}.csv"
    ((count2++))
done

cp "$source_file2" "${destination_dir2}/${destination_file2}"

# cp "../${dirSims}${simulationDAG}/logsProcessed/$evaluationSat/time/hwloop_total_time.csv" "../evaluation/results/accuracy/time/"
sleep 60

done
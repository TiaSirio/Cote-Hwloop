#!/bin/bash
#
# A bash scripts that runs the simulation with a defined instances of satellites,
# a defined number of jobs and a maximum number of tasks per job.
# The instances of satellite will always have the same job.
# All the calculation are done at the simulation side and each task is sent back singularly using mqtt.


# Set up simulation parameters and configure physical satellite
cd cube_sat_scripts/sim
source simulation.conf
./mapperGeneratorSingleJob.sh
./configureCubeSatSimLightSingleJob.sh
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while configuring the satellite"
  exit 1
fi

# Run simulation
cd $HOME/git-repos/cote-hwloop/artifacts/hwloop/scripts/
echo "HWLoop simulation is running."
./hwloop.sh "$satellite" "$jobs" "s" "$mapperFile" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopic" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload" "$noDataMessage"

# Stop running programs on the satellite
cd $HOME/git-repos/cote-hwloop/scripts/cube_sat_scripts/sim/
./stopSatellitePrograms.sh
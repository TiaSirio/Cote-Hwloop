#!/bin/bash

cd cube_sat_scripts/sim
source simulation.conf

# Run simulation
cd $HOME/git-repos/cote-hwloop/artifacts/hwloop/scripts/
./hwloop.sh "$satellite" "$jobs" "s" "$mapperFile" "$physicalInstances" "$serverMQTT" "$portMQTT" "$subscriberID" "$publisherID" "$subscribeTopic" "$topicCommands" "$commandExecute" "$topicAppData" "$topicDuration" "$topicNonFuncData" "$topicPayload"  "$noDataMessage"
echo "HWLoop simulation is running in the background."
echo "It may be awhile before it complete, check with 'top'."

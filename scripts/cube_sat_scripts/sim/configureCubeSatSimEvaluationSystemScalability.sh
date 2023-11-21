#!/bin/bash

source simulation.conf

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

numberOfSatellite=$1
satVal="fakesatellite${numberOfSatellite}"

sshToSat=$(grep "^$satVal=" fakeSatelliteEvaluation.conf | cut -d'=' -f2)

mapperFilePositionToSCPFakeSat="${execDir}${mapperFileName}"

maxPhysicalNumberOfSatellites=$((numberOfSatellite * maxNumberOfFake))
if [ $maxPhysicalNumberOfSatellites -gt $physicalInstances ]; then
    maxPhysicalNumberOfSatellites=$physicalInstances
fi

startingPhysicalNumberOfSatellites=$((((numberOfSatellite - 1) * maxNumberOfFake) + 1))

fakeSatDirPosition="${reachingHomeInFakeSatellites}${dirOnFakeSatellite}"
echo "Start configuring $sshToSat!"

attempt=0
while [ $attempt -lt "$maxNumberOfAttempts" ]; do
    if scp "$mapperFilePositionToSCPFakeSat" "$sshToSat:$fakeSatDirPosition"
    then
        break
    else
        echo "SCP operation failed! Retrying in 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    fi
done
if [ $attempt -eq "$maxNumberOfAttempts" ]; then
    echo "SCP operation failed after $attempt attempts. Couldn't configure fake nanosatellites. Exiting with code 1."
    exit 1
fi

# Compile programs and execute satellite programs
attemptSSH=0
while [ $attemptSSH -lt "$maxNumberOfAttempts" ]; do
    if ssh "$sshToSat" "cd $dirOnFakeSatellite && ./$startFakeSatelliteScriptsFromSim $maxPhysicalNumberOfSatellites $startingPhysicalNumberOfSatellites $mapperType $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $radiationErrorRatio $errorMessage"
    then
        echo "Configured fake satellites!"
        break
    else
        echo "SSH connection or remote command failed! Retrying in 2 seconds..."
        sleep 2
        attemptSSH=$((attemptSSH + 1))
    fi
done

if [ $attemptSSH -eq "$maxNumberOfAttempts" ]; then
    echo "SSH connection failed after $attemptSSH attempts. Couldn't configure fake nanosatellites. Exiting with code 1."
    exit 1
fi

echo "$sshToSat ready!"
if [ "$maxPhysicalNumberOfSatellites" = "$physicalInstances" ]; then
    echo "All satellites configured!"
    exit 2
fi

exit 0


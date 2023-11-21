#!/bin/bash

source simulation.conf

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

numberOfSatellite=$1

sshToSat=$sshFakeSatellite

mapperFilePositionToSCPFakeSat="${execDir}${mapperFileName}"

if [[ $sshToSat == $sshFakeSatellite ]]; then

    fakeSatDirPosition="${reachingHomeInFakeSatellites}${dirOnFakeSatellite}"

    echo "Start configuring fake nanosatellites..."

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
      if ssh "$sshToSat" "cd $dirOnFakeSatellite && ./$startFakeSatelliteScriptsFromSim $physicalInstances $numberOfSatellite $mapperType $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $radiationErrorRatio $errorMessage"
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

    echo "Fake Cubesatsims ready!"
    exit 2
fi

echo "All satellites configured!"
exit 0


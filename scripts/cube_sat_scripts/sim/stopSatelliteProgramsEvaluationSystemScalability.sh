#!/bin/bash

source simulation.conf

numberOfSatellite=$1
satVal="fakesatellite${numberOfSatellite}"

sshToSat=$(grep "^$satVal=" fakeSatelliteEvaluation.conf | cut -d'=' -f2)

maxPhysicalNumberOfSatellites=$((numberOfSatellite * maxNumberOfFake))
if [ $maxPhysicalNumberOfSatellites -gt $physicalInstances ]; then
    maxPhysicalNumberOfSatellites=$physicalInstances
fi

# Fake nanosatellite
echo "Start stopping programs on $sshToSat"

attempt=0
while [ $attempt -lt "$maxNumberOfAttempts" ]; do
  if ssh "$sshToSat" "cd $dirOnFakeSatellite && ./$stopFakeSatelliteScripts"
  then
      break
  else
      echo "SSH operation failed! Retrying in 2 seconds..."
      sleep 2
      attempt=$((attempt + 1))
    fi
done

if [ $attempt -eq "$maxNumberOfAttempts" ]; then
    echo "SSH operation failed after $attempt attempts. Couldn't stop fake programs. Exiting with code 1."
    exit 1
fi

echo "Stopped programs on $sshToSat!"
if [ "$maxPhysicalNumberOfSatellites" = "$physicalInstances" ]; then
    echo "All satellites stopped!"
    exit 2
fi

exit 0
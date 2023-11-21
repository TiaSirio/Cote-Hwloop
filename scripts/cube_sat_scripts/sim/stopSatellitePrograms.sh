#!/bin/bash

source simulation.conf

numberOfSatellite=$1
satVal="satellite${numberOfSatellite}"

sshToSat=$(grep "^$satVal=" phSatToUse.conf | cut -d'=' -f2)

if [ -z "$sshToSat" ]; then
    sshToSat=$sshFakeSatellite
fi

# Fake nanosatellite
if [[ $sshToSat == $sshFakeSatellite ]]; then

  echo "Start stopping programs on fake nanosatellites..."

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
  # if ! ssh "$sshToSat" "cd simulation/ && ./stopFakeSatelliteScripts.sh"
  # then
  #   echo "ssh operation failed!"
  #   exit 1
  # fi

  echo "Stopped programs on fake nanosatellites!"
  exit 2
fi


# Real nanosatellite
phSatDir=$(grep "^$sshToSat=" execDirPhysicalSatellite.conf | cut -d'=' -f2)

echo "Start stopping programs on $sshToSat..."

# Stop scripts
attemptReal=0
while [ $attemptReal -lt "$maxNumberOfAttempts" ]; do
  if ssh "$sshToSat" "cd $phSatDir && ./$stopSatelliteScripts"
  then
    break
  else
    echo "SSH operation failed! Retrying in 2 seconds..."
    sleep 2
    attemptReal=$((attemptReal + 1))
  fi
done

if [ $attemptReal -eq "$maxNumberOfAttempts" ]; then
  echo "SSH operation failed after $attemptReal attempts. Couldn't stop programs on $sshToSat. Exiting with code 1."
  exit 1
fi

echo "Stopped programs on $sshToSat!"

# if ! ssh "$sshToSat" "cd $phSatDir && ./$stopSatelliteScripts"
# then
#   echo "ssh operation failed!"
#   exit 1
# fi
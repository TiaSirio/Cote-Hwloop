#!/bin/bash

source simulation.conf

sshToSat=$sshFakeSatellite

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
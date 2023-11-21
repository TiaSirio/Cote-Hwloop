#!/bin/bash

source simulation.conf

if [ "$#" -ne 1 ]; then
    echo "Invalid number of arguments. Usage: $0 <satelliteSSH>"
    exit 1
fi

cubesatSSH=$1
pathToSaveData="${pathFromRootToDirectoryBeforeSimulationFiles}${pathFromBeforeSimulationFilesToProcessedData}"
pathToScriptInCexec="${pathFromRootToDirectoryBeforeSimulationFiles}${pathFromBeforeSimulationFilesToSimulationScripts}"
pathToSimulationFilesInSat="${pathFromRootToDirectoryBeforeSimulationFiles}${simulationFilesDirectory}"
pathToChaosDuckInSat="${pathFromRootToDirectoryBeforeSimulationFiles}${simulationFilesDirectory}${faultInjectionProgramDir}"

if grep -q "=${cubesatSSH}$" "$physicalSatelliteConf"; then
    echo "Satellite $cubesatSSH already exists in the conf file."
else
    # Find the last satellite number in the conf file
    last_satellite_number=$(grep -Eo "satellite[0-9]+" "$physicalSatelliteConf" | awk -F'satellite' '{print $2}' | sort -n | tail -1)

    # Increment the last satellite number by 1
    new_satellite_number=$((last_satellite_number + 1))

    # Append the new satellite entry to the conf file
    echo "satellite${new_satellite_number}=${cubesatSSH}" >> "$physicalSatelliteConf"
fi

if grep -q "${cubesatSSH}=" "$execDirPhysicalSatelliteConf"; then
    echo "Satellite $cubesatSSH already exists in the conf file."
else
    # Append the new satellite entry to the conf file
    echo "${cubesatSSH}=$pathToScriptInCexec" >> "$execDirPhysicalSatelliteConf"
fi

if grep -q "${cubesatSSH}=" "$nonFuncPhysicalSatelliteConf"; then
    echo "Satellite $cubesatSSH already exists in the conf file."
else
    # Append the new satellite entry to the conf file
    echo "${cubesatSSH}=$pathToSaveData/$fileToStoreNonFunctionalData" >> "$nonFuncPhysicalSatelliteConf"
fi

if grep -q "${cubesatSSH}=" "$payloadPhysicalSatelliteConf"; then
    echo "Satellite $cubesatSSH already exists in the conf file."
else
    # Append the new satellite entry to the conf file
    echo "${cubesatSSH}=$pathToSaveData/$fileToStorePayloadData" >> "$payloadPhysicalSatelliteConf"
fi

# Copy data scripts
if ! scp "newSatelliteDir/nonFuncSave.py" "newSatelliteDir/payloadRetrieve.c" "$cubesatSSH:$pathFromRootToDirectoryBeforeSimulationFiles"
then
  echo "SCP simulationFiles command failed!"
  exit 1
fi

# Compile c program
if ! ssh "$cubesatSSH" "cd $pathFromRootToDirectoryBeforeSimulationFiles && mkdir simulationFiles/ && gcc payloadRetrieve.c -o payloadRetrieve -lwiringPi && cd simulationFiles/ && mkdir cexec/ && mkdir nonFuncData/"
then
  echo "Compile payload failed!"
  exit 1
fi

# Rsync
if ! rsync -avh --delete "newSatelliteDir/simulationFiles/" "$cubesatSSH:$pathToSimulationFilesInSat"
then
  echo "rsync operation failed!"
  exit 1
fi

# Install ZeroTier - NEED ALSO TO ENTER YOUR NETWORK AND GIVE PUBLIC KEY TO SATELLITE TO CONNECT SSH WITHOUT PASSWORD
if ! ssh "$cubesatSSH" "curl -s https://install.zerotier.com | sudo bash"
then
  echo "ZeroTier installation"
  exit 1
fi

# Install libraries
if ! ssh "$cubesatSSH" "pip3 install paho-mqtt && cd $pathToChaosDuckInSat && pip3 install -r requirements.txt"
then
  echo "Install libraries failed!"
  exit 1
fi


echo "Cubesat configured"
exit 0


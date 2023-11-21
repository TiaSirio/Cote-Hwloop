#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Needed int that defines configuration of overhead!"
    exit 1
fi

if [ $1 -eq 0 ]; then
    destinationFile="non_func_data.txt"
    whatRemove=""
elif [ $1 -eq 1 ]; then
    destinationFile="non_func_data_non_func.txt"
    whatRemove="temp_non_func.txt"
elif [ $1 -eq 2 ]; then
    destinationFile="non_func_data_payload.txt"
    whatRemove="non_func_payload.txt"
elif [ $1 -eq 3 ]; then
    destinationFile="non_func_data_command.txt"
    whatRemove=""
else
    echo "Wrong input."
    exit 1
fi

dirWhereToSave="data"

maxNumberOfAttempts=5
attemptRealSSH=0
while [ $attemptRealSSH -lt "$maxNumberOfAttempts" ]; do
    if ssh "cubesatsim" "cd /home/pi/CubeSatSim/simulationFiles/overhead/ && ./runOverheadScriptOnNanoSat.sh $1"
    then
        echo "Calculated overhead!"
        break
    else
        echo "SSH connection or remote command failed! Retrying in 2 seconds..."
        sleep 2
        attemptRealSSH=$((attemptRealSSH + 1))
    fi
done

if [ $attemptRealSSH -eq "$maxNumberOfAttempts" ]; then
    echo "SSH operation failed after $attemptRealSSH attempts."
    exit 1
fi


attemptRealSSH=0
while [ $attemptRealSSH -lt "$maxNumberOfAttempts" ]; do
    if rsync --backup --remove-source-files -av "cubesatsim:/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt" "$dirWhereToSave/$destinationFile"
    then
        echo "Saved data!"
        break
    else
        echo "SSH connection or remote command failed! Retrying in 2 seconds..."
        sleep 2
        attemptRealSSH=$((attemptRealSSH + 1))
    fi
done

if [ $attemptRealSSH -eq "$maxNumberOfAttempts" ]; then
    echo "SSH operation failed after $attemptRealSSH attempts."
    exit 1
fi


if [ -n "$whatRemove" ]; then
    attemptRealSSH=0
    while [ $attemptRealSSH -lt "$maxNumberOfAttempts" ]; do
        if ssh "cubesatsim" "cd /home/pi/CubeSatSim/simulationFiles/nonFuncData/ && rm $whatRemove"
        then
            echo "Removed data and ready for next program!"
            break
        else
            echo "SSH connection or remote command failed! Retrying in 2 seconds..."
            sleep 2
            attemptRealSSH=$((attemptRealSSH + 1))
        fi
    done
fi

if [ $attemptRealSSH -eq "$maxNumberOfAttempts" ]; then
    echo "SSH operation failed after $attemptRealSSH attempts."
    exit 1
fi
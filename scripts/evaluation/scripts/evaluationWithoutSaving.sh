#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Needed int that defines script to test!"
    exit 1
fi

indexScript="$1"

cd "../results/fidelity/"
# programs=("nonFuncSave" "nonFuncSaveLessSleep" "nonFuncSaveMoreSleep" "nonFuncSaveNoSleep" "nonFuncSaveOnlyBus")
# dirNames=("standard" "less_sleep" "more_sleep" "no_sleep" "only_bus")
programs=("nonFuncSave" "nonFuncSaveLessSleep" "nonFuncSaveMoreSleep" "nonFuncSaveOnlyBus")
dirNames=("standard" "less_sleep" "more_sleep" "only_bus")
len=${#programs[@]}

for ((i = 0; i < 5; i++)); do
    scriptToEvaluate="${programs[$indexScript]}"
    dirWhereToSave="${dirNames[$indexScript]}"

    echo "Evaluating program $scriptToEvaluate!"

    maxNumberOfAttempts=5
    attemptRealSSH=0
    while [ $attemptRealSSH -lt "$maxNumberOfAttempts" ]; do
        if ssh "cubesatsim" "cd /home/pi/CubeSatSim/simulationFiles/evaluation/ && ./evaluationSatelliteScript.sh $scriptToEvaluate.py"
        then
            echo "Evaluated $scriptToEvaluate!"
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

    sleep 10

    attemptRealSSH=0
    while [ $attemptRealSSH -lt "$maxNumberOfAttempts" ]; do
        if ssh "cubesatsim" "cd /home/pi/CubeSatSim/simulationFiles/nonFuncData && rm non_func_payload.txt && rm non_func_data.txt"
        then
            echo "Removed data and ready for next program!"
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

    sleep 10
done
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Needed int to run script!"
    exit 1
fi

if [ $1 -eq 0 ]; then
    echo "No program running."
    scriptToRun=""
elif [ $1 -eq 1 ]; then
    echo "Running only non-functional recorder."
    scriptToRun="python3 nonFuncSaveOverhead.py"
elif [ $1 -eq 2 ]; then
    echo "Running only payload recorder."
    scriptToRun="./payloadRetrieve /home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_payload.txt"
elif [ $1 -eq 3 ]; then
    echo "Running only command receiver."
    scriptToRun="./runCommandReceiver.sh"
else
    echo "Wrong input."
    exit 1
fi

nohup python3 "../../nonFuncSave.py" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt" > /dev/null 2>&1 & nonFuncPID=$!

if [ $1 -eq 2 ]; then
    cd "../../"
fi

if [ -n "$scriptToRun" ]; then
    runProgr=1
    eval nohup "$scriptToRun" > /dev/null 2>&1 & progrPID=$!
fi

sleep 1800

kill $nonFuncPID
if [ $runProgr -eq 1 ]; then
    kill $progrPID
fi
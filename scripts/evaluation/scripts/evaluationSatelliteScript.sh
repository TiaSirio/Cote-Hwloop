#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Insert name of program to run!"
    exit 1
fi

cd basicmath/

nohup ./basicmath_large > /dev/null 2>&1 & progrPID=$!

cd ../

nohup python3 "$1" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt" > /dev/null 2>&1 & nonFuncPID=$!

cd ../..

nohup ./payloadRetrieve "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_payload.txt" > /dev/null 2>&1 & payloadPID=$!

sleep 600

kill $progrPID
kill $nonFuncPID
kill $payloadPID

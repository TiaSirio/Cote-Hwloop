#!/bin/bash

set -- "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data_benchmark_for_payload.txt" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_payload_benchmark_for_payload.txt"

minuteToStop=30
secondsToMinute=60

stopTime=$((minuteToStop * secondsToMinute))

cd ../..

nohup python3 nonFuncSave.py "${1}" > /dev/null 2>&1 & PID1=$!

nohup ./payloadRetrieve "${2}" > /dev/null 2>&1 & PID2=$!

sleep $stopTime

kill $PID1
kill $PID2
echo "Finish benchmark"

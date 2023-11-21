#!/bin/bash

set -- "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data_benchmark_alone.txt"

minuteToStop=30
secondsToMinute=60

stopTime=$((minuteToStop * secondsToMinute))

cd ../..

nohup python3 nonFuncSave.py "${1}" > /dev/null 2>&1 & PID1=$!

sleep $stopTime

kill $PID1
echo "Finish benchmark"

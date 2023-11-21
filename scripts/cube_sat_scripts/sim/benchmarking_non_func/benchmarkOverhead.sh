#!/bin/bash

dirNames=("non_func_data_non_func.txt" "non_func_data_payload.txt" "non_func_data_command.txt")
len=${#dirNames[@]}

for ((i = 0; i < len; i++)); do
    typeOfOverhead="${dirNames[$i]}"
    if python3 benchmarkProcessing.py "data/non_func_data.txt" "data/$typeOfOverhead"
    then
        echo "Calculate overhead for $typeOfOverhead"
    else
        echo "Fails to calculate overhead for $typeOfOverhead"
        #exit 1
    fi
done
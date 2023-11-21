#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Required type of scalability and number of directory!"
    exit 1
fi

inputData="$1"

if [ $inputData -eq 0 ]; then
    typeOfEvaluation="jobs_scalability"
elif [ $inputData -eq 1 ]; then
    typeOfEvaluation="satellites_scalability"
elif [ $inputData -eq 2 ]; then
    typeOfEvaluation="system_scalability"
else
    echo "Missing type of evaluation!"
    exit 1
fi

satellite="$(printf "%03d" $2)"

python3 validate_scalability_evaluation.py "../results/scalability/$typeOfEvaluation/$satellite/simulation_duration.txt"
#!/bin/bash

dirNames=("jobs_scalability" "satellites_scalability" "system_scalability")
len=${#dirNames[@]}

for ((i = 0; i < len; i++)); do
    typeOfEvaluation="${dirNames[$i]}"
    for satellite_dir in ../results/scalability/$typeOfEvaluation/*; do
        if [ -d "$satellite_dir" ]; then
            satellite=$(basename "$satellite_dir")
            if python3 validate_scalability_evaluation.py "../results/scalability/$typeOfEvaluation/$satellite/simulation_duration.txt"
            then
                echo "Validated $typeOfEvaluation/$satellite"
            else
               echo "Fails to validate $typeOfEvaluation/$satellite"
               exit 1
            fi
        fi
    done
done

echo "All data for scalability evaluation are validated!"
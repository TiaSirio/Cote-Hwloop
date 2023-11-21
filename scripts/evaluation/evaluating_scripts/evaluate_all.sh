#!/bin/bash

echo "Evaluate accuracy!"
pathToTime="../results/accuracy/time/"
pathToConsumption="../results/accuracy/consumption/"

python3 consumption_accuracy.py "$pathToTime" "$pathToConsumption"

echo "Evaluate fidelity!"
python3 payload_fidelity.py "../results/fidelity/less_sleep" "../results/fidelity/more_sleep" "../results/fidelity/only_bus" "../results/fidelity/standard"

echo "Evaluate scalability!"
python3 time_scalability.py "../results/scalability/jobs_scalability" "../results/scalability/satellites_scalability" "../results/scalability/system_scalability"

echo "Evaluated all metrics!"
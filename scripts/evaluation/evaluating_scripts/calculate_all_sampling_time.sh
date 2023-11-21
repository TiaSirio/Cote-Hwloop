#!/bin/bash

# dirNames=("standard" "less_sleep" "more_sleep" "no_sleep" "only_bus")
dirNames=("standard" "less_sleep" "more_sleep" "only_bus")
# dirNames=("standard" "more_sleep" "only_bus")
len=${#dirNames[@]}

for ((i = 0; i < len; i++)); do
    typeOfEvaluation="${dirNames[$i]}"
    python3 sampling_time.py "../results/fidelity/$typeOfEvaluation"
    echo "Calculated $typeOfEvaluation"
done

echo "All sampling time calculated!"
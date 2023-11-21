#!/bin/bash

# dirNames=("standard" "less_sleep" "more_sleep" "no_sleep" "only_bus")
dirNames=("standard" "less_sleep" "more_sleep" "only_bus")
# dirNames=("standard" "more_sleep" "only_bus")
len=${#dirNames[@]}

for ((i = 0; i < len; i++)); do
    typeOfEvaluation="${dirNames[$i]}"
    if python3 validate_fidelity_evaluation.py "../results/fidelity/$typeOfEvaluation"
    then
        echo "Validated $typeOfEvaluation"
    else
        echo "Fails to validate $typeOfEvaluation"
        exit 1
    fi
done

echo "All data for fidelity evaluation are validated!"
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Required type of fidelity!"
    exit 1
fi

inputData="$1"

python3 validate_fidelity_evaluation.py "$inputData"
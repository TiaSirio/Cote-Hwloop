#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Required type of sampled time to calculate!"
    exit 1
fi

inputData="$1"

python3 sampling_time.py "$inputData"
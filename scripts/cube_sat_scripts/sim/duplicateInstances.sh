#! /bin/bash

if [ "$#" -ne 1 ]; then
    echo "Invalid number of arguments. Usage: $1 <Starting instance>"
    exit 1
fi

startingInstance=$1

# Generate a new mapper
python3 duplicateSatelliteInstances.py "$startingInstance"
#! /bin/bash

if [ "$#" -ne 2 ]; then
    echo "Invalid number of arguments. Usage: $1 <Starting instance>, $2 <Until instance>"
    exit 1
fi

startingInstance=$1
untilInstances=$2

# Generate a new mapper
python3 duplicateSatelliteInstancesUntil.py "$startingInstance" "$untilInstances"
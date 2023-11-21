#!/bin/bash

# Configure multiple satellites
source simulation.conf

for ((i=1; i<="$physicalInstances"; i++))
do
    ./"$1" "$i"
    result=$?

    if [ "$result" -eq 2 ]
    then
      exit 0
    fi

    if [ "$result" -gt 0 ]
    then
      echo "Error while configuring the satellite"
      exit 1
    fi
done

exit 0
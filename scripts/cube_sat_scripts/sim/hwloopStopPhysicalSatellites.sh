#!/bin/bash

# Stop multiple satellites
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
      echo "Error with satellite communication"
      exit 1
    fi
done

exit 0
#!/bin/bash

# Configure multiple satellites
source simulation.conf

if [ $maxNumberOfFake -ne 0 ]; then
    temp_result=$(awk -v physicalInstances="$physicalInstances" -v maxNumberOfFake="$maxNumberOfFake" 'BEGIN { result = int(physicalInstances / maxNumberOfFake); if (physicalInstances % maxNumberOfFake > 0) result += 1; print result }')
    max_loop=$temp_result
fi

for ((i=1; i<="$max_loop"; i++))
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
#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

# Generate a new mapper
python3 generateYAMLToBeConfigured.py "$satellite" "1" "$mapperType" "$execDir" "$tasksYamlFileName" "$satelliteInstancesYamlFileName" "$tasksUsedConf"
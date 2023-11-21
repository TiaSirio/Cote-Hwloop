#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

# Generate a new mapper
python3 generateYAMLToBeConfigured.py "$satellite" "$jobs" "m" "$mapperFile" "$mapperDir" "$tasksYamlFile" "$tasksYamlDir" "$satelliteInstancesYamlFile" "$satelliteInstancesYamlDir"
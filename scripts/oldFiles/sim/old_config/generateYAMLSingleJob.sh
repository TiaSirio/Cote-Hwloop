#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

# Generate a new mapper
python3 generateYAMLToBeConfigured.py "$satellite" "1" "s" "$mapperFile" "$mapperDir" "$tasksYamlFile" "$tasksYamlDir" "$satelliteInstancesYamlFile" "$satelliteInstancesYamlDir"
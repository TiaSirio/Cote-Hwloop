#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

# Generate a new mapper
python3 DAGGenerateYAMLToBeConfigured.py "$satellite" "$jobs" "m" "$execDir" "$tasksYamlFileName" "$satelliteInstancesYamlFileName"
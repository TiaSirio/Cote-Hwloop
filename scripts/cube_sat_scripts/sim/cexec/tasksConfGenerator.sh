#! /bin/bash

# Run config to retrieve the variables
source ../simulation.conf

# Generate a new mapper
python3 ../tasksConfGenerator.py "../$tasksUsedConf" "$tasksExecutablesConf" "../$tasksYamlFileName"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error!"
  exit 1
fi
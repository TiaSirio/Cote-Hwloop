#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

mapperFileString="${execDir}${mapperFileName}"

# Generate a new mapper
python3 DAGMapperGenerator.py m "$mapperFileString" "$satelliteInstancesYamlFileName"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while creating the mapper!"
  exit 1
fi
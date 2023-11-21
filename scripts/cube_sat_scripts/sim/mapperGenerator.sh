#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

mapperFileString="${execDir}${mapperFileName}"

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

# Generate a new mapper
python3 mapperGenerator.py "$mapperType" "$mapperFileString" "$satelliteInstancesYamlFileName"
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while creating the mapper!"
  exit 1
fi
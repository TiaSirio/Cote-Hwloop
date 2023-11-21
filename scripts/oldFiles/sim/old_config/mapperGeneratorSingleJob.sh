#! /bin/bash

# Run config to retrieve the variables
source simulation.conf

# Generate a new mapper
python3 mapperGenerator.py s "$mapperFile" "$satelliteInstancesYamlFile" "$satelliteInstancesYamlDir"
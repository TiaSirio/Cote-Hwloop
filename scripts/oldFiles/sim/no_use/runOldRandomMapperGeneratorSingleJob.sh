#! /bin/bash

# Run config to retrieve the variables
. simulation.conf

# Generate a new mapper
python3 mapperGeneratorSingleJob.py "$satellite" "$jobs" "$maxNumberOfTasks"
#! /bin/bash

# Run config to retrieve the variables
. simulation.conf

# Generate a new mapper
python3 mapperGeneratorMultipleJobs.py "$satellite" "$jobs" "$maxNumberOfTasks"
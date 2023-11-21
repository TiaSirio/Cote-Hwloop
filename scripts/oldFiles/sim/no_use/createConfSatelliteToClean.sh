#!/bin/bash

source phSatToUse.conf

new_conf_file="cleanPhysicalSatellite.conf"

> "$new_conf_file"

# Loop through all the variables in the sourced conf file
for var in "${!satellite@}"; do
  # Extract the satellite name
  satellite_name="${var#satellite}"

  # Create the new conf line with the satellite name set to true
  line="satellite${satellite_name}=true"

  # Append the new conf line to the new conf file
  echo "$line" >> "$new_conf_file"
done
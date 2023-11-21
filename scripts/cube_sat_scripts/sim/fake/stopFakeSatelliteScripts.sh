#!/bin/bash

file_path="programsExecuted.conf"

while IFS= read -r line; do
  # Extract the left-hand side element before the '=' sign
  pid_key=$(echo "$line" | cut -d '=' -f 1)
  # Extract the PID value after the '=' sign
  pid_value=$(echo "$line" | cut -d '=' -f 2)
  # Kill the PID using the 'kill' function
  kill "$pid_value"
done < "$file_path"
#!/bin/bash

times="$1"
task_to_execute="$2"

command="$task_to_execute"

index=3
while [[ -n "${!index}" ]]; do
    current_param="${!index}"
    command+=" $current_param"
    ((index++))
done

for ((i=1; i<=$times; i++)); do
    eval $command
done
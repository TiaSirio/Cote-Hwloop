#!/bin/bash

current_dir=$(pwd)

task_to_execute="$1"
dataset_dir="$2"
result_dir="$3"
type_of_file="$4"

cd "$dataset_dir"

file_list=(*."$type_of_file")

cd "$current_dir"

for file_name in "${file_list[@]}"
do
    command="./$task_to_execute $dataset_dir $result_dir $file_name output_$file_name"

    index=5
    while [[ -n "${!index}" ]]; do
        current_param="${!index}"
        command+=" $current_param"
        ((index++))
    done

    eval $command
done
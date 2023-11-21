#!/bin/bash

current_dir=$(pwd)

task_to_execute="$1"
dataset_dir="$2"
result_dir="$3"
type_of_file="$4"
index_of_file="$5"

cd "$dataset_dir"

file_list=(*."$type_of_file")

cd "$current_dir"

mod_index_of_file=$((index_of_file % ${#file_list[@]}))

file_name_needed="${file_list[mod_index_of_file]}"

command="./$task_to_execute $dataset_dir $result_dir $file_name_needed output_$file_name_needed"

index=6
while [[ -n "${!index}" ]]; do
    current_param="${!index}"
    command+=" $current_param"
    ((index++))
done

eval $command
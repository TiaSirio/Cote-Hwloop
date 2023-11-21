#!/bin/bash

current_dir=$(pwd)

dataset_dir="$3"
result_dir="$4"
type_of_file="$1"
index_of_file="$2"

cd "$dataset_dir"

file_list=(*."$type_of_file")

cd "$current_dir"
cd ../chaosduck/faulted-binaries

mod_index_of_file=$((index_of_file % ${#file_list[@]}))
file_name_needed="${file_list[mod_index_of_file]}"

for file in *; do
    if [ -x "$file" ]; then
        dataset_dir="../../cexec/${dataset_dir}"
        result_dir="../../cexec/${result_dir}"
        command="valgrind ./$file $dataset_dir $result_dir $file_name_needed output_$file_name_needed"

        index=5
        while [[ -n "${!index}" ]]; do
            current_param="${!index}"
            command+=" $current_param"
            ((index++))
        done

        eval $command
        return_code=$?

        if [ $return_code -ne 0 ]; then
            cd ../
            rm -f faulted-binaries/*
            cd "$current_dir"
            exit $return_code
        fi
    fi
    break
done

cd ../

rm -f faulted-binaries/*

cd "$current_dir"
#!/bin/bash

current_dir=$(pwd)

dataset_dir="$2"
result_dir="$3"
type_of_file="$1"

cd "$dataset_dir"

file_list=(*."$type_of_file")

cd "$current_dir"
cd ../chaosduck/faulted-binaries

for file in *; do
    for file_name in "${file_list[@]}"
    do
        if [ -x "$file" ]; then
            dataset_dir="../../cexec/${dataset_dir}"
            result_dir="../../cexec/${result_dir}"
            command="valgrind ./$file $dataset_dir $result_dir $file_name output_$file_name"

            index=4
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
    done
    break
done

cd ../

rm -f faulted-binaries/*

cd "$current_dir"
#!/bin/bash

for file in ../chaosduck/faulted-binaries/*; do
    if [ -x "$file" ]; then
        #command="./../chaosduck/faulted-binaries/$file"

        #command="valgrind"
        #command+=" ./$file"

        command+="./$file"

        index=1
        while [[ -n "${!index}" ]]; do
            current_param="${!index}"

            command+=" $current_param"
            ((index++))
        done

        eval $command
        return_code=$?

        if [ $return_code -ne 0 ]; then
            rm -f ../chaosduck/faulted-binaries/*
            exit $return_code
        fi
    fi
    break
done

rm -f ../chaosduck/faulted-binaries/*

'''

current_dir=$(pwd)

cd ../chaosduck/faulted-binaries

for file in *; do
    if [ -x "$file" ]; then
        command="./$file"

        index=1
        while [[ -n "${!index}" ]]; do
            current_param="${!index}"

            if [[ $index -eq 1 ]]; then
                current_param="../../cexec/${current_param}"
            elif [[ $index -eq 2 ]]; then
                current_param="../../cexec/${current_param}"
            fi
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
'''
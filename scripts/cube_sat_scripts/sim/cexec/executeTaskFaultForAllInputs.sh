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
            command="./$file $dataset_dir $result_dir $file_name output_$file_name"

            index=4
            while [[ -n "${!index}" ]]; do
                current_param="${!index}"
                command+=" $current_param"
                ((index++))
            done

            #ulimit -v 10240
            #timeout 5 $command
            #res=$!

            eval $command
            res=$?

            : '
            command+=" &"

            eval $command
            PID=$!

            i=1
            while [ $i -le 5 ]
            do
              ps -p $PID >> /dev/null
              if [ $? -ne 0 ]
              then
                wait $PID
                rm -f ../chaosduck/faulted-binaries/*
                exit $? #success, return rc of program
              fi

              i=$(($i+1))
              echo "Waited $i seconds..."
              sleep 1
            done
            '
        fi
    done
    break
done

rm -f ../chaosduck/faulted-binaries/*
exit $res

: '
rm -f ../chaosduck/faulted-binaries/*
echo "Program killed..."
kill $PID
exit 1 #failed
'
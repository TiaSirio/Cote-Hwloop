#!/bin/bash

for file in ../chaosduck/faulted-binaries/*; do
    if [ -x "$file" ]; then
        #command="valgrind"
        #command+=" ./$file"

        command+="./$file"

        index=1
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
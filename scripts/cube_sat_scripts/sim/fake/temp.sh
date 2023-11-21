#!/bin/bash

if [ "$#" -lt 7 ]
then
	echo "Inserting default arguments"
	set -- "s" "1" "broker.hivemq.com" "1883" "cubesatsim/commands/" "cubesatsim/duration/" "cubesatsim/nonfuncdata/" "cubesatsim/payload/" "cubesatsim/appdata/" "mapper.txt" "satellite" "execute" "nodata" "0.0001" "ERROR"

fi

# shellcheck disable=SC1037
python3 fakeCommandReceiver.py "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}"
commandReceiverPID=$!

file_path="programsExecuted.conf"

commandReceiverValue="commandReceiverPID$2"
if grep -q "$commandReceiverValue" "$file_path"; then
    echo "Command receiver PID already exists in $file_path"
    exit 1
else
    # Append the new commandReceiverValue with the PID to the file
    echo "$commandReceiverValue=$commandReceiverPID" >> "$file_path"
fi

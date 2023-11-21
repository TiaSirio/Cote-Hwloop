#!/bin/bash

if [ "$#" -lt 7 ]
then
	echo "Inserting default arguments"
	set -- "$1" "$2" "broker.hivemq.com" "1883" "cubesatsim/commands/" "cubesatsim/duration/" "cubesatsim/nonfuncdata/" "cubesatsim/payload/" "cubesatsim/appdata/" "mapper.txt" "satellite" "execute" "nodata" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_payload.txt" "/home/pi/CubeSatSim/simulationFiles/cexec" "0.0001" "ERROR" "tasksExecutables.conf" "tasksDatasets.conf" "tasksResults.conf" "tasksTypeOfFile.conf" "commandReceiverRadiation.py" "1" "outputsCleaner.sh" "createTaskFault.sh" "executeTaskFault.sh" "executeTaskFaultForAllInputs.sh" "executeTaskFaultForSequentialInputs.sh" "runTaskForAllInputs.sh" "runTaskForSequentialInputs.sh" "5" "tasksRepeating.conf" "runTaskMultipleTimes.sh"

fi

cd ../..

nohup python3 nonFuncSave.py "${14}" > /dev/null 2>&1 & nonFuncPID=$!

nohup ./payloadRetrieve "${15}" > /dev/null 2>&1 & payloadPID=$!

cd simulationFiles/scriptsSim


evaluationToCompare="commandReceiverRadiationEvaluation.py"

# shellcheck disable=SC1037
#nohup python3 commandReceiver.py "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}" "${18}" "${19}" "${20}" "${21}" > /dev/null 2>&1 & commandReceiverPID=$!
if [ "${23}" = "$evaluationToCompare" ]; then
    nohup python3 "${23}" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}" "${18}" "${19}" "${20}" "${21}" "${22}" "${24}" "${25}" "${26}" "${27}" "${28}" "${29}" "${30}" "${31}" "${32}" "${33}" "${34}" > /dev/null 2>&1 & commandReceiverPID=$!
else
    nohup python3 "${23}" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}" "${18}" "${19}" "${20}" "${21}" "${22}" "${24}" "${25}" "${26}" "${27}" "${28}" "${29}" "${30}" "${31}" "${32}" > /dev/null 2>&1 & commandReceiverPID=$!
fi


cd ~/CubeSatSim/simulationFiles/cexec

file_path="programsExecuted.conf"
file_content=$(cat "$file_path")

nonFuncValue="nonFuncPID"
payloadValue="payloadPID"
commandReceiverValue="commandReceiverPID"
fileContent=$(echo "$file_content" | sed "s/^$nonFuncValue=.*/$nonFuncValue=$nonFuncPID/" | sed "s/^$payloadValue=.*/$payloadValue=$payloadPID/" | sed "s/^$commandReceiverValue=.*/$commandReceiverValue=$commandReceiverPID/")
echo "$fileContent" > "$file_path"

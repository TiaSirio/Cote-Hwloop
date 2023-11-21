#!/bin/bash

if [ "$#" -lt 7 ]
then
	echo "Inserting default arguments"
	set -- "s" "10" "broker.hivemq.com" "1883" "cubesatsim/commands/" "cubesatsim/duration/" "cubesatsim/nonfuncdata/" "cubesatsim/payload/" "cubesatsim/appdata/" "mapper.txt" "satellite" "execute" "nodata" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_data.txt" "/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_payload.txt" "/home/pi/CubeSatSim/simulationFiles/cexec" "0" "ERROR" "tasksExecutables.conf" "tasksDatasets.conf" "tasksResults.conf" "tasksTypeOfFile.conf" "commandReceiverRadiation.py" "1" "outputsCleaner.sh" "createTaskFault.sh" "executeTaskFault.sh" "executeTaskFaultForAllInputs.sh" "executeTaskFaultForSequentialInputs.sh" "runTaskForAllInputs.sh" "runTaskForSequentialInputs.sh" "5"
fi

# shellcheck disable=SC1037
python3 "${23}" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}" "${18}" "${19}" "${20}" "${21}" "${22}" "${24}" "${25}" "${26}" "${27}" "${28}" "${29}" "${30}" "${31}" "${32}"

#!/bin/bash

maxInstance=$1
currentInstance=$2

> "programsExecuted.conf"

for ((i=currentInstance; i<=maxInstance; i++))
do
    sleep 0.2
    nohup ./startFakeSatelliteScript.sh "$3" "$i" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" > /dev/null 2>&1 &
done

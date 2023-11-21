#!/bin/bash
#
# process_hwloop_logs.sh

dataNum="$(printf "%03d" $1)/"

source "../artifacts/hwloopDAG/data/${dataNum}simulation.conf"

logNotProcessedString="${dirSims}${simulationDAG}${logNotProcessed}${dataNum}"
logProcessedString="${dirSims}${simulationDAG}${logProcessed}${dataNum}"
mapperDirString="${dirSims}${simulationDAG}${dirData}${dataNum}${mapperFileName}"

target_dir="$simDir"

# Get the current directory
current_dir=$(pwd)

# Check if already in the target directory
if [[ $current_dir == */$target_dir ]]; then
    execFilesDir="$execDir"
else
    execFilesDir="${fromScriptsToSimScripts}${execDir}"
fi

# HWLoop
python3 hwloop_coverage.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$dirToGenerateCoverage"
python3 hwloop_state_cubesat.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$dirToGenerateState"
python3 hwloop_consume.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$execFilesDir" "$mapperDirString" "m" "$jobs" "$dirToGenerateTaskConsume" "$dirToGenerateSatConsume"
python3 hwloop_job_position.py "$logNotProcessedString" "$logProcessedString" "$dirToGenerateJob" "$satellite"
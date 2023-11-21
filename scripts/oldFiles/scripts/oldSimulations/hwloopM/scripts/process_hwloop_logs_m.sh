#!/bin/bash
#
# process_hwloop_logs.sh

dataNum="$(printf "%03d" $1)/"

source "../artifacts/hwloopM/data/${dataNum}simulation.conf"

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

logNotProcessedString="${dirSims}${simulationM}${logNotProcessed}${dataNum}"
logProcessedString="${dirSims}${simulationM}${logProcessed}${dataNum}"
mapperDirString="${dirSims}${simulationM}${dirData}${dataNum}${mapperFileName}"

target_dir="$simDir"

tasksUsedConfFilePosition="${fromScriptsToSimScripts}${tasksUsedConf}"

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
python3 hwloop_jobs_completed.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$dirToGenerateJobsCompleted"
python3 hwloop_state_cubesat.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$dirToGenerateState"
python3 hwloop_consumption.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$execFilesDir" "$mapperDirString" "$mapperType" "$jobs" "$dirToGenerateTaskConsume" "$dirToGenerateSatConsume" "$tasksUsedConfFilePosition"
python3 hwloop_job_position.py "$logNotProcessedString" "$logProcessedString" "$dirToGenerateJob" "$satellite"
python3 hwloop_errors.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$dirToGenerateErrors"
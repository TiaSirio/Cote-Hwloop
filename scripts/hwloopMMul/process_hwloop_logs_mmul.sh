#!/bin/bash
#
# process_hwloop_logs.sh

cd ../

if [ "$#" -ne 1 ]; then
    echo "Invalid number of arguments. Usage: $0 <Number of satellites>"
    exit 1
fi

dataNum="$(printf "%03d" $1)/"

source "../artifacts/hwloopMMul/data/${dataNum}simulation.conf"

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

logNotProcessedString="${dirSims}${simulationMMul}${logNotProcessed}${dataNum}"
logProcessedString="${dirSims}${simulationMMul}${logProcessed}${dataNum}"
mapperDirString="${dirSims}${simulationMMul}${dirData}${dataNum}${mapperFileName}"
lastRunBackupString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${lastRunBackup}"

target_dir="$simDir"

tasksUsedConfFilePosition="${fromScriptsToSimScripts}${tasksUsedConf}"

if [ -d "$logProcessedString" ]; then
    rm -rf "$logProcessedString"/*/
fi

# Get the current directory
current_dir=$(pwd)

# Check if already in the target directory
if [[ $current_dir == */$target_dir ]]; then
    execFilesDir="$execDir"
else
    execFilesDir="${fromScriptsToSimScripts}${execDir}"
fi

# HWLoop
python3 hwloop_coverage.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$logProcessedCoverage"
python3 hwloop_jobs_completed.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$logProcessedJobsCompleted"
python3 hwloop_state_cubesat.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$logProcessedState"
python3 hwloop_consumption.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$execFilesDir" "$mapperDirString" "$mapperType" "$jobs" "$logProcessedTaskConsumption" "$logProcessedSatConsumption" "$tasksUsedConfFilePosition"
python3 hwloop_job_position.py "$logNotProcessedString" "$logProcessedString" "$logProcessedJob" "$satellite"
python3 hwloop_errors.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$logProcessedErrors"
python3 hwloop_time.py "$logNotProcessedString" "$logProcessedString" "$satellite" "$execFilesDir" "$mapperDirString" "$mapperType" "$jobs" "$logProcessedTime" "$tasksUsedConfFilePosition"
#python3 hwloop_time.py "$logNotProcessedString" "$logProcessedString" "$jobs" "$satellite" "$logProcessedTime" "$execFilesDir" "$mapperDirString" "$mapperType" "$tasksUsedConfFilePosition"

mkdir "$lastRunBackupString"

# Create a backup of the current execution
cp "$logNotProcessedString"/* "$lastRunBackupString"
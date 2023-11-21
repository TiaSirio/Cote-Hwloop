#!/bin/bash
#
# generate_f8_plots.sh
# A bash script that generates the latency plots

cd ../

if [ "$#" -ne 1 ]; then
    echo "Invalid number of arguments. Usage: $0 <Number of satellites>"
    exit 1
fi

dataNum="$(printf "%03d" $1)/"

source p3-env/bin/activate
source "../artifacts/hwloopDAG/data/${dataNum}simulation.conf"

logCoverageString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedCoverage}"
logJobCompletedString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedJobsCompleted}"
logStateString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedState}"
logTaskConsumptionString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedTaskConsumption}"
logSatConsumptionString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedSatConsumption}"
logJobString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedJob}"
logErrorString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedErrors}"
logTimeString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${logProcessedTime}"

# logNotProcessedString="${dirSims}${simulationDAG}${logNotProcessed}${dataNum}"
lastRunBackupString="${dirSims}${simulationDAG}${logProcessed}${dataNum}${lastRunBackup}"

plotString="${plotDir}${simulationDAG}${dataNum}"

if [ -d "$plotString" ]; then
    rm -rf "$plotString"/*/
fi

python3 plot_hwloop_coverage.py "$logCoverageString" "$plotDir" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateCoverage}"
python3 plot_hwloop_jobs_completed.py "$logJobCompletedString" "$plotDir" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateJobsCompleted}"
python3 plot_hwloop_state.py "$logStateString" "$plotDir" "$jobs" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateState}" "$lastRunBackupString" "${simulationDAG}${dataNum}${dirToGenerateStatePercentage}"

python3 plot_hwloop_task_consumption.py "$logTaskConsumptionString" "$plotDir" "$jobs" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateTaskConsumption}"
python3 plot_hwloop_sat_consumption.py "$logSatConsumptionString" "$plotDir" "$jobs" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateSatConsumption}"
python3 plot_hwloop_consumption_per_job.py "$logSatConsumptionString" "$plotDir" "$satellite" "$jobs" "${simulationDAG}${dataNum}${dirToGenerateConsumptionPerJob}"
if [ "$singleJob" -eq 1 ]; then
    python3 plot_hwloop_consumption_per_task.py "$logSatConsumptionString" "$plotDir" "$satellite" "$jobs" "${simulationDAG}${dataNum}${dirToGenerateConsumptionPerTask}"
fi

python3 plot_hwloop_job_position.py "$logJobString" "$plotDir" "${simulationDAG}${dataNum}${dirToGenerateJob}" "$satellite" "$orbitDuration"

python3 plot_hwloop_errors_per_satellite.py "$logErrorString" "$plotDir" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateErrors}"
python3 plot_hwloop_errors_percentage.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationDAG}${dataNum}${dirToGenerateErrorsPercentage}"
python3 plot_hwloop_errors_per_job.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationDAG}${dataNum}${dirToGenerateErrorsPerSat}"

python3 plot_hwloop_total_time.py "$logTimeString" "$plotDir" "$jobs" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateTotalTime}"
#python3 plot_hwloop_total_time.py "$logTimeString" "$plotDir" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateTotalTime}"
python3 plot_hwloop_time_per_job.py "$logTimeString" "$plotDir" "$satellite" "$jobs" "${simulationDAG}${dataNum}${dirToGenerateTimePerJob}"
if [ "$singleJob" -eq 1 ]; then
    python3 plot_hwloop_time_per_task.py "$logTimeString" "$plotDir" "$satellite" "$jobs" "${simulationDAG}${dataNum}${dirToGenerateTimePerTask}"
fi
python3 plot_hwloop_time_per_task_mean.py "$logTimeString" "$plotDir" "$jobs" "$satellite" "${simulationDAG}${dataNum}${dirToGenerateMeanTimePerTask}"

deactivate

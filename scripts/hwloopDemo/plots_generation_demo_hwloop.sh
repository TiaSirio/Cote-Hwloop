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
source "../artifacts/hwloopDemo/data/${dataNum}simulation.conf"

logCoverageString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedCoverage}"
logJobCompletedString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedJobsCompleted}"
logStateString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedState}"
logTaskConsumptionString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedTaskConsumption}"
logSatConsumptionString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedSatConsumption}"
logJobString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedJob}"
logErrorString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedErrors}"
logTimeString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${logProcessedTime}"

# logNotProcessedString="${dirSims}${simulationDemo}${logNotProcessed}${dataNum}"
lastRunBackupString="${dirSims}${simulationDemo}${logProcessed}${dataNum}${lastRunBackup}"

plotString="${plotDir}${simulationDemo}${dataNum}"

if [ -d "$plotString" ]; then
    rm -rf "$plotString"/*/
fi

python3 plot_hwloop_coverage.py "$logCoverageString" "$plotDir" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateCoverage}"
python3 plot_hwloop_jobs_completed.py "$logJobCompletedString" "$plotDir" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateJobsCompleted}"
python3 plot_hwloop_state.py "$logStateString" "$plotDir" "$jobs" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateState}" "$lastRunBackupString" "${simulationDemo}${dataNum}${dirToGenerateStatePercentage}"

python3 plot_hwloop_task_consumption.py "$logTaskConsumptionString" "$plotDir" "$jobs" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateTaskConsumption}"
python3 plot_hwloop_sat_consumption.py "$logSatConsumptionString" "$plotDir" "$jobs" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateSatConsumption}"
python3 plot_hwloop_consumption_per_job.py "$logSatConsumptionString" "$plotDir" "$satellite" "$jobs" "${simulationDemo}${dataNum}${dirToGenerateConsumptionPerJob}"
if [ "$singleJob" -eq 1 ]; then
    python3 plot_hwloop_consumption_per_task.py "$logSatConsumptionString" "$plotDir" "$satellite" "$jobs" "${simulationDemo}${dataNum}${dirToGenerateConsumptionPerTask}"
fi

python3 plot_hwloop_job_position.py "$logJobString" "$plotDir" "${simulationDemo}${dataNum}${dirToGenerateJob}" "$satellite" "$orbitDuration"

python3 plot_hwloop_errors_per_satellite.py "$logErrorString" "$plotDir" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateErrors}"
python3 plot_hwloop_errors_percentage.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationDemo}${dataNum}${dirToGenerateErrorsPercentage}"
python3 plot_hwloop_errors_per_job.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationDemo}${dataNum}${dirToGenerateErrorsPerSat}"

python3 plot_hwloop_total_time.py "$logTimeString" "$plotDir" "$jobs" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateTotalTime}"
#python3 plot_hwloop_total_time.py "$logTimeString" "$plotDir" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateTotalTime}"
python3 plot_hwloop_time_per_job.py "$logTimeString" "$plotDir" "$satellite" "$jobs" "${simulationDemo}${dataNum}${dirToGenerateTimePerJob}"
if [ "$singleJob" -eq 1 ]; then
    python3 plot_hwloop_time_per_task.py "$logTimeString" "$plotDir" "$satellite" "$jobs" "${simulationDemo}${dataNum}${dirToGenerateTimePerTask}"
fi
python3 plot_hwloop_time_per_task_mean.py "$logTimeString" "$plotDir" "$jobs" "$satellite" "${simulationDemo}${dataNum}${dirToGenerateMeanTimePerTask}"

deactivate

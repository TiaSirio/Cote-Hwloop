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
source "../artifacts/hwloopMMul/data/${dataNum}simulation.conf"

logCoverageString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedCoverage}"
logJobCompletedString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedJobsCompleted}"
logStateString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedState}"
logTaskConsumptionString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedTaskConsumption}"
logSatConsumptionString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedSatConsumption}"
logJobString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedJob}"
logErrorString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedErrors}"
logTimeString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${logProcessedTime}"

# logNotProcessedString="${dirSims}${simulationMMul}${logNotProcessed}${dataNum}"
lastRunBackupString="${dirSims}${simulationMMul}${logProcessed}${dataNum}${lastRunBackup}"

plotString="${plotDir}${simulationMMul}${dataNum}"

if [ -d "$plotString" ]; then
    rm -rf "$plotString"/*/
fi
python3 plot_hwloop_coverage.py "$logCoverageString" "$plotDir" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateCoverage}"
python3 plot_hwloop_jobs_completed.py "$logJobCompletedString" "$plotDir" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateJobsCompleted}"
python3 plot_hwloop_state.py "$logStateString" "$plotDir" "$jobs" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateState}" "$lastRunBackupString" "${simulationMMul}${dataNum}${dirToGenerateStatePercentage}"

python3 plot_hwloop_task_consumption.py "$logTaskConsumptionString" "$plotDir" "$jobs" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateTaskConsumption}"
python3 plot_hwloop_sat_consumption.py "$logSatConsumptionString" "$plotDir" "$jobs" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateSatConsumption}"
python3 plot_hwloop_consumption_per_job.py "$logSatConsumptionString" "$plotDir" "$satellite" "$jobs" "${simulationMMul}${dataNum}${dirToGenerateConsumptionPerJob}"
if [ "$singleJob" -eq 1 ]; then
    python3 plot_hwloop_consumption_per_task.py "$logSatConsumptionString" "$plotDir" "$satellite" "$jobs" "${simulationMMul}${dataNum}${dirToGenerateConsumptionPerTask}"
fi

python3 plot_hwloop_job_position.py "$logJobString" "$plotDir" "${simulationMMul}${dataNum}${dirToGenerateJob}" "$satellite" "$orbitDuration"

python3 plot_hwloop_errors_per_satellite.py "$logErrorString" "$plotDir" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateErrors}"
python3 plot_hwloop_errors_percentage.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationMMul}${dataNum}${dirToGenerateErrorsPercentage}"
python3 plot_hwloop_errors_per_job.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationMMul}${dataNum}${dirToGenerateErrorsPerSat}"

python3 plot_hwloop_total_time.py "$logTimeString" "$plotDir" "$jobs" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateTotalTime}"
#python3 plot_hwloop_total_time.py "$logTimeString" "$plotDir" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateTotalTime}"
python3 plot_hwloop_time_per_job.py "$logTimeString" "$plotDir" "$satellite" "$jobs" "${simulationMMul}${dataNum}${dirToGenerateTimePerJob}"
if [ "$singleJob" -eq 1 ]; then
    python3 plot_hwloop_time_per_task.py "$logTimeString" "$plotDir" "$satellite" "$jobs" "${simulationMMul}${dataNum}${dirToGenerateTimePerTask}"
fi
python3 plot_hwloop_time_per_task_mean.py "$logTimeString" "$plotDir" "$jobs" "$satellite" "${simulationMMul}${dataNum}${dirToGenerateMeanTimePerTask}"

deactivate

#!/bin/bash
#
# generate_f8_plots.sh
# A bash script that generates the latency plots

dataNum="$(printf "%03d" $1)/"

source p3-env/bin/activate
source "../artifacts/hwloopM/data/${dataNum}simulation.conf"

logCoverageString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedCoverage}"
logJobCompletedString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedJobsCompleted}"
logStateString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedState}"
logTaskConsumeString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedTaskConsume}"
logSatConsumeString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedSatConsume}"
logJobString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedJob}"
logErrorString="${dirSims}${simulationM}${logProcessed}${dataNum}${logProcessedErrors}"

logNotProcessedString="${dirSims}${simulationM}${logNotProcessed}${dataNum}"

python3 plot_hwloop_coverage.py "$logCoverageString" "$plotDir" "$satellite" "${simulationM}${dataNum}${dirToGenerateCoverage}"
python3 plot_hwloop_jobs_completed.py "$logJobCompletedString" "$plotDir" "$satellite" "${simulationM}${dataNum}${dirToGenerateJobsCompleted}"
python3 plot_hwloop_state.py "$logStateString" "$plotDir" "$jobs" "$satellite" "${simulationM}${dataNum}${dirToGenerateState}" "$logNotProcessedString" "${simulationM}${dataNum}${dirToGenerateStatePercentage}"
python3 plot_hwloop_task_consumption.py "$logTaskConsumeString" "$plotDir" "$jobs" "$satellite" "${simulationM}${dataNum}${dirToGenerateTaskConsume}"
python3 plot_hwloop_sat_consumption.py "$logSatConsumeString" "$plotDir" "$jobs" "$satellite" "${simulationM}${dataNum}${dirToGenerateSatConsume}"
python3 plot_hwloop_job_position.py "$logJobString" "$plotDir" "${simulationM}${dataNum}${dirToGenerateJob}" "$satellite" "$orbitDuration"
python3 plot_hwloop_errors.py "$logErrorString" "$plotDir" "$satellite" "${simulationM}${dataNum}${dirToGenerateErrors}"
python3 plot_hwloop_errors_percentage.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationM}${dataNum}${dirToGenerateErrorsPercentage}"
python3 plot_hwloop_errors_per_satellite.py "$logErrorString" "$plotDir" "$satellite" "$jobs" "${simulationM}${dataNum}${dirToGenerateErrorsPerSat}"

deactivate

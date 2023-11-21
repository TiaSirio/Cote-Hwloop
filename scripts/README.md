# Scripts

This directory contains scripts.

## Directory Contents
* [cube_sat_scripts](cube_sat_scripts/README.md): Artifact program (called HWLoopDAG)
* [evaluation](evaluation/README.md): Destination directory for artifact plots
* [hwloopDAG](hwloopDAG/README.md): Script to start and plots standard HIL simulation.
* [hwloopDemo](hwloopDemo/README.md): Script to start and plots standard HIL simulation deterministic.
* [hwloopMMul](hwloopMMul/README.md): Script to start and plots multithreading HIL simulation.
* [oldFiles](oldFiles/README.md): Files no more used.
### Logs
* [hwloop_consumption.py](hwloop_consumption.py): Process the consumption logs.
* [hwloop_coverage.py](hwloop_coverage.py): Process the coverage logs.
* [hwloop_errors.py](hwloop_errors.py): Process the radiation errors logs.
* [hwloop_job_position.py](hwloop_job_position.py): Process the job logs.
* [hwloop_jobs_completed.py](hwloop_jobs_completed.py): Process the job logs.
* [hwloop_state_cubesat.py](hwloop_state_cubesat.py): Process the state of working of the satellite logs.
* [hwloop_time.py](hwloop_time.py): Process the working time of the satellite logs.
### Plots
* [plot_hwloop_coverage.py](plot_hwloop_coverage.py): Plot coverage of satellites.
* [plot_hwloop_errors_percentage.py](plot_hwloop_errors_percentage.py): Plot radiation errors of satellites (percentage is considered per faulty jobs).
* [plot_hwloop_errors_percentage.py](plot_hwloop_errors_per_job.py): Plot radiation errors for each job of every satellite.
* [plot_hwloop_errors_per_satellite.py](plot_hwloop_errors_per_satellite.py): Plot radiation errors for each satellite.
* [plot_hwloop_job_position.py](plot_hwloop_job_position.py): Plot position in the orbit where the satellite is working or not working.
* [plot_hwloop_jobs_completed.py](plot_hwloop_jobs_completed.py): Plot the jobs completed for each satellite.
* [plot_hwloop_state.py](plot_hwloop_state.py): Plot the state timeline followed by each satellite.
* [plot_hwloop_sat_consumption.py](plot_hwloop_sat_consumption.py): Plot the consumption of each satellite.
* [plot_hwloop_task_consumption.py](plot_hwloop_task_consumption.py): Plot the total and mean task consumption of each satellite.
* [plot_hwloop_consumption_per_job.py](plot_hwloop_consumption_per_job.py): Plot the consumption for each job of each satellite.
* [plot_hwloop_consumption_per_task.py](plot_hwloop_consumption_per_task.py): Plot the task consumption of each job of each satellite.
* [plot_hwloop_time_per_job.py](plot_hwloop_time_per_job.py): Plot the time for each job of each satellite.
* [plot_hwloop_task_consumption.py](plot_hwloop_time_per_task.py): Plot the task time of each job of each satellite.
* [plot_hwloop_task_consumption.py](plot_hwloop_time_per_task_mean.py): Plot the mean time of the task used.
* [plot_hwloop_task_consumption.py](plot_hwloop_total_time.py): Plot the total time of each satellite.
### Setup
* [setup_dependencies.sh](setup_dependencies.sh): Downloads and compiles GCC 8.3.0 to the specified directory for use with the artifact software.
* The script path is expected to be `/home/username/sw`.
* [setup_py_venv.sh](setup_py_venv.sh): Sets up the Python virtual environment for Matplotlib.
* [setup_mqtt.sh](setup_mqtt.sh): Sets up Paho-MQTT for C++, following the guide on Github.
* [setup_simulator.sh](setup_simulator.sh): Sets up the simulator side.
* [README.md](README.md): This document.

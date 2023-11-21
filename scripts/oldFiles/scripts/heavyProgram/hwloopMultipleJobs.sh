#!/bin/bash
#
# A bash scripts that runs the simulation with a defined instances of satellites,
# a defined number of jobs and a maximum number of tasks per job.
# The instances of satellite will always have a different job.
# All the calculation are done at the satellite side and then sent back using mqtt


# Set up simulation parameters and configure physical satellite
cd cube_sat_scripts/sim
./simulation.config
./runMapperGeneratorMultipleJobs.sh
./configureCubeSatSimMultipleJobs.sh

# Run simulation
cd $HOME/git-repos/cote-hwloop/artifacts/hwloop/scripts/
./hwloop.sh
echo "CSFP simulations are running in the background."
echo "It may be awhile before they complete, check with 'top'."

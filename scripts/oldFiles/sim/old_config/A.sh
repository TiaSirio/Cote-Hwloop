#!/bin/bash

source simulation.conf

# Remove previous programs
ssh cubesatsim "rm -v ~/CubeSatSim/simulationFiles/cexec/*"
echo "Deleted previous programs"

# Copy programs
POS=$(pwd)
scp -rv "$POS"/cexec/ cubesatsim:/home/pi/CubeSatSim/simulationFiles
# scp -rv ~/cexec/ cubesatsim:/home/pi/CubeSatSim/simulationFiles
echo "Finish to copy programs"

# Compile programs
ssh cubesatsim 'cd ~/CubeSatSim/simulationFiles/cexec && make'
echo "Programs compiled"

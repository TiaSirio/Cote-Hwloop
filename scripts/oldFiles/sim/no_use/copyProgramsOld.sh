#!/bin/bash

ssh cubesatsim "rm -v ~/CubeSatSim/simulationFiles/cexec/*"

echo "Deleted previous programs"

scp -rv ~/cexec/ cubesatsim:/home/pi/CubeSatSim/simulationFiles

echo "Finish to copy programs"

ssh cubesatsim 'cd ~/CubeSatSim/simulationFiles/cexec && make'

echo "Programs compiled"

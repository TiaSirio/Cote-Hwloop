#!/bin/bash

ssh cubesatsim "rm -v ~/CubeSatSim/cexec/*"

echo "Deleted previous programs"

scp -r3 simulation:/home/ubuntu/cexec/ cubesatsim:/home/pi/CubeSatSim

echo "Finish to copy programs"

ssh cubesatsim 'cd ~/CubeSatSim/cexec && make'

echo "Programs compiled"

#./compileAllScripts.sh

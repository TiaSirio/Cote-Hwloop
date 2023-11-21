#!/bin/bash

cd cube_sat_scripts/sim
source simulation.conf
./DAGMapperGeneratorSingleJob.sh
./configureCubeSatSimDAGSingleJob.sh

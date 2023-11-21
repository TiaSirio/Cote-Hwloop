#!/bin/bash

cd ../..

gcc myTelemTest.c -o myTelemTest

cd ..

for i in {1..10}
do
	CubeSatSim/myTelemTest
	sleep 0.2
done

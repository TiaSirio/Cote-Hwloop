# CMakeLists.txt
# CMakeLists.txt file
#
# Copyright 2019 Bradley Denby
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at <http://www.apache.org/licenses/LICENSE-2.0>.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

cmake_minimum_required(VERSION 3.0)
project(HWLoopDAG)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
include_directories("../../../software/satsim/ilog/include"
                    "../../../software/satsim/isim/include"
                    "../../../software/satsim/iwork/include"
                    "../../../software/satsim/logger/include"
                    "../../../software/satsim/job/include"
                    "../../../software/satsim/energy-harvester/include"
                    "../../../software/satsim/simple-solar-cell/include"
                    "../../../software/satsim/energy-storage/include"
                    "../../../software/satsim/capacitor/include"
                    "../../../software/satsim/energy-consumer/include"
                    "../../../software/satsim/cubesat/include"
                    "../../../software/satsim/eh-system/include"
                    "../../../software/satsim/orbit/include"
                    "../../../software/satsim/satellite/include"
                    "../../../software/satsim/eh-satellite/include"
                    "../../../software/satsim/task/include"
                    "../../../../paho.mqtt.c/src"
                    "../../../../../../../usr/local/include")
add_executable(hwloopDAG hwloopDAG.cpp
               ../../../software/satsim/logger/source/Logger.cpp
               ../../../software/satsim/job/source/Job.cpp
               ../../../software/satsim/energy-harvester/source/EnergyHarvester.cpp
               ../../../software/satsim/simple-solar-cell/source/SimpleSolarCell.cpp
               ../../../software/satsim/energy-storage/source/EnergyStorage.cpp
               ../../../software/satsim/capacitor/source/Capacitor.cpp
               ../../../software/satsim/energy-consumer/source/EnergyConsumer.cpp
               ../../../software/satsim/cubesat/source/CubeSat.cpp
               ../../../software/satsim/eh-system/source/EHSystem.cpp
               ../../../software/satsim/orbit/source/Orbit.cpp
               ../../../software/satsim/satellite/source/Satellite.cpp
               ../../../software/satsim/task/source/Task.cpp
               ../../../software/satsim/eh-satellite/source/EHSatellite.cpp)
target_link_libraries(hwloopDAG paho-mqttpp3 paho-mqtt3as)
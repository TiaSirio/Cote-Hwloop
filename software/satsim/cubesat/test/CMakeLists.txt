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
project(TestCubeSat)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
include_directories("../include"
                    "../../ilog/include"
                    "../../isim/include"
                    "../../iwork/include"
                    "../../logger/include"
                    "../../job/include"
                    "../../energy-consumer/include")
add_executable(test_jetson_tx2 test-cubesat.cpp
               ../source/CubeSat.cpp
               ../../logger/source/Logger.cpp
               ../../job/source/Job.cpp
               ../../energy-consumer/source/EnergyConsumer.cpp)

#!/bin/bash
#
# setup_mqtt.sh
# A bash script that sets up MQTT on the machine

cd ~/

# Download and install C version
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
git checkout v1.3.8
CC=$HOME/sw/gcc-8.3.0-install/bin/gcc LD_LIBRARY_PATH=$HOME/sw/gcc-8.3.0-install/lib64/ \
 cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_BUILD_STATIC=ON -DPAHO_WITH_SSL=ON -DPAHO_HIGH_PERFORMANCE=ON
sudo cmake --build build/ --target install
sudo ldconfig

# Download and install C++ version
git clone https://github.com/eclipse/paho.mqtt.cpp
cd paho.mqtt.cpp
CXX=$HOME/sw/gcc-8.3.0-install/bin/g++ LD_LIBRARY_PATH=$HOME/sw/gcc-8.3.0-install/lib64/ \
 cmake -Bbuild -H. -DPAHO_BUILD_STATIC=ON -DPAHO_BUILD_DOCUMENTATION=TRUE -DPAHO_BUILD_SAMPLES=TRUE
sudo cmake --build build/ --target install
sudo ldconfig
#!/bin/bash
# setup_simulator.sh
# A bash script that runs the instruction on the README

sudo apt install make git build-essential cmake -y
sudo apt install python3-dev python3-pip python3-tk python3-venv -y
pip3 install pyaml
pip3 install networkx

sudo apt-get install cmake-gui cmake-curses-gui -y
sudo apt-get install libssl-dev -y
sudo apt-get install doxygen graphviz -y

./setup_dependencies.sh "$HOME/sw"

./setup_mqtt.sh

echo "The simulator is set, continue following the instruction on the README to finish configuring the HIL simulation."
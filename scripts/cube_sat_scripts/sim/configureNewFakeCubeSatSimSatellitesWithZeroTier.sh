#!/bin/bash

source simulation.conf

if [ "$#" -ne 2 ]; then
    echo "Invalid number of arguments. Usage: $1 <satelliteSSH>, $2 <ZeroTier network>"
    exit 1
fi

cubesatSSH=$1
zerotier_network=$2

# Create satellite dir
if ! ssh "$cubesatSSH" "mkdir satellite/"
then
  echo "Satellite dir creation failed!"
  exit 1
fi

# Copy data scripts
if ! scp fake/* "$cubesatSSH:/home/cubesatsim/satellite/"
then
  echo "SCP for fake satellite failed!"
  exit 1
fi

# Install libraries
if ! ssh "$cubesatSSH" "pip3 install paho-mqtt && pip3 install yaml && cd CubeSatSim/simulationFiles/chaosduck/ && pip3 install -r requirements.txt"
then
  echo "Install libraries failed!"
  exit 1
fi

# Install ZeroTier
if ! ssh "$cubesatSSH" "curl -s https://install.zerotier.com | sudo bash"
then
  echo "ZeroTier installation"
  exit 1
fi

# Join ZeroTier network
if ! ssh "$cubesatSSH" "sudo zerotier-cli join $zerotier_network"
then
  echo "Connected to zerotier"
  exit 1
fi

echo "Cubesat configured"
exit 0


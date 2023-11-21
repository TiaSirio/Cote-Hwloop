HIL Simulation using as basis the "Orbital Edge Computing ASPLOS 2020 Artifact Software"

This software artifact simulates orbital nanosatellites constellations, using as data for the simulation, data coming from a real satellite.

**Current version**: 1.0.0

* This software uses [semantic versioning](http://semver.org).

**Dependencies**

* C++11 and C++17 compilers ([Install script](scripts/setup_dependencies.sh))
* CMake for building Makefiles (user must install separately)
* Standard command line tools (e.g. make, wget)
* Python 3 with the `venv` module (virtual environment used for plotting)
* Paho MQTT C++ Library - https://github.com/eclipse/paho.mqtt.cpp ([Install script](scripts/setup_mqtt.sh))
* PyYAML and networkx - For manage configuration files
* [setup_simulator.py](scripts/setup_simulator.sh): Follow the instructions contained in this readme to setup the simulator.

```bash
sudo apt install make git build-essential cmake
sudo apt install python3-dev python3-pip python3-tk python3-venv
pip3 install pyaml
pip3 install networkx
```

The following are used to install Paho-MQTT from Github: [Paho-MQTT](https://github.com/eclipse/paho.mqtt.cpp)

```bash
sudo apt-get install cmake-gui cmake-curses-gui
sudo apt-get install libssl-dev
sudo apt-get install doxygen graphviz
```

## Directory Contents

* [artifacts](artifacts/README.md): Artifact program (called HWLoopDAG)
* [plots](plots/README.md): Destination directory for artifact plots
* [scripts](scripts/README.md): Useful scripts, e.g. for setting up dependencies
* [software](software/README.md): Classes, utilities, etc.
* [README.md](README.md): This document

## How to Use

Clone the repository into the specified location.

```bash
mkdir $HOME/git-repos
cd $HOME/git-repos
git clone bitbucket.url
```

Change directories to the top-level `scripts` directory:

```bash
cd $HOME/git-repos/cote-hwloop/scripts/
```

Run the dependency setup script. This script downloads GCC 8.3.0 and compiles it
for use. Ensure that the host system has essential build tools installed.

```bash
./setup_dependencies.sh $HOME/sw
```

Run the mqtt script.
This script will install Paho MQTT following the instruction given on Github.

```bash
./setup_mqtt.sh
```


Configure the CubeSatSim nano-satellite, following the next steps:
* Build and install the CubeSatSim satellite, following the instruction provided by the official guide (https://cubesatsim.com/).
* Configure a connection between the computer running the simulation and the satellite, for instance with ZeroTier.
* Run the script to configure the satellite, passing as argument the name of the SSH connection.

```bash
./cube_sat_scripts/sim/configureNewCubeSatSimSatellite.sh <name_of_ssh_connection>
```


Add the desired programs that will run on the satellite inside "cube_sat_scripts/sim/cexec/c_tasks" and fill the
tasksDAG.yaml file present in the "cube_sat_scripts/sim/" directory with the new programs added (following the structure
already described in the YAML).


Configure all the following configuration files:
* [simulation.conf](scripts/cube_sat_scripts/sim/simulation.conf) -> Containing some parameters regarding the simulation, some regarding the satellite and other regarding the directories used.
* [tasksDatasets.conf](scripts/cube_sat_scripts/sim/cexec/tasksDatasets.conf) -> Where we can find the possible inputs needed for a program.
* [tasksResults.conf](scripts/cube_sat_scripts/sim/cexec/tasksResults.conf) -> Where we save the output file if a program needs to output something.
* [tasksTypeOfFile.conf](scripts/cube_sat_scripts/sim/cexec/tasksTypeOfFile.conf) -> Type of input file needed by the program (assumption - only one type of file).
* [phSatToUse.conf](scripts/cube_sat_scripts/sim/phSatToUse.conf) -> Copy here the address of the satellite that will be used in the simulation.


Configure the programs that will run on the satellite and the configuration to be tested.
* Run "[generateYAML.sh](scripts/cube_sat_scripts/sim/generateYAML.sh)", to generate the structure of the YAML.
* Fill the YAML in the configuration needed.

```bash
cd cube_sat_scripts/sim/
./generateYAML.sh
cd ../..
cd hwloopDAG/
```


Launch the HWLoopDAG simulation.

```bash
./hwloopDAG.sh
```

Process the data logs. Data log processing may take some time.

```bash
./process_logs.sh
```

Set up the Python virtual environment used for generating plots.

```bash
./setup_py_venv.sh
```

Generate the plots.

```bash
./generate_plots.sh
```

## License

Copyright 2019 Bradley Denby

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at <http://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

#!/bin/bash

current_dir=$(pwd)

cd ../chaosduck/

nohup python3 chaosduck.py "$1" "../cexec/$2" > /dev/null 2>&1

cd "$current_dir"
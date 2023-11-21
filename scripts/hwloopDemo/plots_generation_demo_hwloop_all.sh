#!/bin/bash
#
# generate_f8_plots.sh
# A bash script that generates the latency plots

cd ../

actual_dir="$(pwd)"

cd "../artifacts/hwloopDemo/data"

directories=$(ls -d */)

cd $actual_dir

# Print each directory separately
for dir in $directories; do
  dir=${dir%/}
  dir=$(echo "$dir" | sed 's/^0*//')
  ./plots_generation_demo_hwloop.sh $dir
done
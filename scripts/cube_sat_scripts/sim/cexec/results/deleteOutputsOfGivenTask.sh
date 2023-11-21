#!/bin/bash

current_dir=$(pwd)

result_dir="$1"

cd "$result_dir"

find . -type f \( -name "*.ppm" -o -name "*.bmp" -o -name "*.pgm" -o -name "*.dat" -o -name "*.dwt" \) -exec rm {} +

cd "$current_dir"
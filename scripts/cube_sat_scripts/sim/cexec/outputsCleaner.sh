#!/bin/bash

# Delete files of specific types in "results/" directory and its subdirectories
find results/ -type f \( -name "*.pgm" -o -name "*.ppm" -o -name "*.dwt" -o -name "*.bmp" -o -name "*.dat" \) -exec rm {} +
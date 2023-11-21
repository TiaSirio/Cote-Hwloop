#!/bin/bash

directory="img"

for file in "$directory"/*.pgm; do
	file_name=$(basename "$file")
	./edge_detector -p "$file" -o "results/$file_name"
done

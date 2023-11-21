#!/bin/bash

directories=(*/)

for dir in "${directories[@]}"; do
	dir=${dir%/}
	echo "$dir"
	if [[ "$dir" != tiff* ]]; then
		make clean -C "$dir"
	fi
done

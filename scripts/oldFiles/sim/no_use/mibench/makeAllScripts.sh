#!/bin/bash

directories=(*/)

for dir in "${directories[@]}"; do
	dir=${dir%/}
	echo "$dir"
	#if [ -e "$dir/Makefile" ]; then
	if [[ "$dir" != tiff* ]]; then
		make -C "$dir"
	fi
done

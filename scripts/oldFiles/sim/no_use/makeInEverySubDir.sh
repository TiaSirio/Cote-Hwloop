#!/bin/bash

function find_makefile_and_make {
  local makefile_found=false

  for dir in "$1"/*; do
    if [[ -f "$dir/Makefile" ]]; then
      echo "Found Makefile in directory: $(basename "$dir")"
      make -C "$dir"
      makefile_found=true
    elif [[ -f "$dir/CMakeLists.txt" ]]; then
      echo "Found CMakeLists.txt in directory: $(basename "$dir")"
      cmake --build "$dir" --target clean
      make -C "$dir"
      cmake_found=true
    fi

    if [[ -d "$dir" && "$makefile_found" == false && "$cmake_found" == false ]]; then
      find_makefile_and_make "$dir"  # Recursive call to search subdirectories
    fi
  done
}

# Start searching from the current directory
find_makefile_and_make "./"
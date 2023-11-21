#!/bin/bash
# Usage: ./hwloopMMul.sh "number of satellites"

logDir="../logs/$(printf "%03d" $1)"

if [ ! -d "$logDir" ]
then
  mkdir "$logDir"
fi


dataDir="../data/$(printf "%03d" $1)"

if [ ! -d "$dataDir" ]
then
  mkdir "$dataDir"
fi


dataLogsDir="../logs/$(printf "%03d" $1)"

if [ -d "$dataLogsDir" ]; then
    rm -f "$dataLogsDir"/*
fi

cd ../build/
CC=$HOME/sw/gcc-8.3.0-install/bin/gcc CXX=$HOME/sw/gcc-8.3.0-install/bin/g++ \
 LD_LIBRARY_PATH=$HOME/sw/gcc-8.3.0-install/lib64/ cmake ../source/
make

# shellcheck disable=SC1037
./hwloopMMul "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}" "${18}" "${19}" "${20}" "${21}" "${22}" "${23}" "${24}"
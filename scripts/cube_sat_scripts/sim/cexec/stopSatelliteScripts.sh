#!/bin/bash

source programsExecuted.conf

kill "$nonFuncPID"
kill "$payloadPID"
kill "$commandReceiverPID"

#!/bin/bash

./evaluate_validation_accuracy.sh
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while validated accuracy!"
  exit 1
fi

./evaluate_all_validation_fidelity.sh
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while validated fidelity!"
  exit 1
fi

./evaluate_all_validation_scalability.sh
result=$?

if [ "$result" -gt 0 ]
then
  echo "Error while validated scalability!"
  exit 1
fi

echo "All evaluation data are validated!"
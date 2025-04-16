#!/bin/bash

echo "Running all tests"

set -e

for test_file in tools/test_*.py; do
    echo "Running $test_file"
    python3 "$test_file"
    echo "-------------------------------------------------------------------"
done

echo "Generating Toyrisc Code"
python3 ./src/Code\ Generation/codegen.py 

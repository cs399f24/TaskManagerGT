#!/bin/bash

# Ensure that the script exits on error
set -e

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is required but not installed. Exiting."
    exit 1
fi

# Run the Python script to create the Cognito resources
echo "Running create_cognito.py..."
python3 ./automation/create_cognito.py

# Check if the Python script ran successfully
if [ $? -eq 0 ]; then
    echo "Cognito resources created successfully."
else
    echo "Error running create_cognito.py"
    exit 1
fi


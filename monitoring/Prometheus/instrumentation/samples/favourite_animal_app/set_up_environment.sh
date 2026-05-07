#!/bin/bash

# Create a virtual environment
python3 -m venv ./env

# Enable the environment
source env/bin/activate

# Install the required Python libraries
python3 -m pip install -r requirements.txt

# Exit the virtual environment
deactivate

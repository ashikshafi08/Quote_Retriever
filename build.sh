#!/bin/bash

# Exit on any error
set -e

# Define the path to the virtual environment
VENV_PATH="./venv"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_PATH" ]; then
    # Define Python version
    PYTHON_VERSION=python3.9

    # Create virtual environment
    echo "Creating virtual environment..."
    $PYTHON_VERSION -m venv $VENV_PATH
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_PATH/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup completed successfully."

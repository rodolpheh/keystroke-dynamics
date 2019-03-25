#! /usr/bin/env bash

# Test requirements
command -v apt >/dev/null 2>&1 || { echo >&2 "I require apt but it's not installed.  Aborting."; exit 1; }

sudo apt update && apt upgrade

sudo apt install -y python3-venv python3-dev make gcc

# Create the needed C library
make dll

# Activate a virtual environment
python3 -m venv .
source ./bin/activate

# Download the needed packages
pip install --upgrade pip
pip install -r requirements.txt

echo "Adding user to input group"

sudo usermod -aG input $USER

echo "Don't forget to source env/bin/activate everytime you need this software !"

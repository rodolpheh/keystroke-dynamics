#! /usr/bin/env bash

# Test requirements
command -v gcc >/dev/null 2>&1 || { echo >&2 "I require gcc but it's not installed.  Aborting."; exit 1; }
command -v make >/dev/null 2>&1 || { echo >&2 "I require make but it's not installed.  Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "I require python3 (ubuntu name) but it's not installed.  Aborting."; exit 1; }

# Create the needed C library
make dll

# Activate a virtual environment
python -m venv env
source env/bin/activate

# Download the needed packages
pip install --upgrade pip
pip install -r requirements.txt

echo "Don't forget to source env/bin/activate everytime you need this software !"
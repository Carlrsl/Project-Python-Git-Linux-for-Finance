#!/bin/bash

echo "[1/4] Updating System Packages..."
# Updates the list of available packages and their versions
sudo apt-get update && sudo apt-get upgrade -y

echo "[2/4] Installing Python Utilities..."
# Installs Python, Pip, Venv module, and Git
sudo apt-get install -y python3 python3-pip python3-venv git

echo "[3/4] Creating Project Directory Structure..."
# Creates folders for data and logs if they don't exist
# We assume we are inside the project folder when running this
mkdir -p data/reports
mkdir -p logs

echo " [4/4] Setting up Virtual Environment (venv)..."
# We create a lightweight virtual environment named 'venv' specific to this server
# This has NOTHING to do with your local 'esilv' conda env.
python3 -m venv venv

echo "Server Setup Complete!"
echo "-----------------------------------------------------"
echo "To start working, activate the environment with:"
echo " source venv/bin/activate"
echo ""
echo "Then install dependencies:"
echo "pip install -r requirements.txt"
echo "-----------------------------------------------------"
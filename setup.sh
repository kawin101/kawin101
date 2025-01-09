#!/bin/bash

# Create virtual environment with Python 3.10
python3.10 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete. Virtual environment created and dependencies installed."
#!/bin/bash

# Set the script directory as the current directory
cd "$(dirname "$0")"

# Check if .venv directory exists
if [ ! -d .venv ]; then
  echo "Creating .venv directory..."
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
fi

# Activate .venv
source .venv/bin/activate

# Delay for 3 seconds
sleep 3

# Start cloudflared
./start-cloudflared.sh &

# Run main.py
python src/main.py

# Deactivate .venv
deactivate
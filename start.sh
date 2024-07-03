#!/bin/bash

VENV=".venv"

cd backend

if [ ! -d "$VENV" ]; then
    echo "virtual environment does not exist, creating it"
    python -m venv .venv
fi

source .venv/scripts/activate
pip install -r requirements.txt
fastapi run app.py
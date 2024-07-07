#!/bin/bash

VENV=".venv"

cd backend

if [ ! -d "$VENV" ]; then
    echo "virtual environment does not exist, performing first time setup"
    chmod -R 777 .
    python -m venv "$VENV" --system-site-packages
fi

source .venv/bin/activate
pip install -r requirements.txt
fastapi run app.py
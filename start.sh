#!/bin/bash

VENV=".venv"

cd backend

if [ ! -d "$VENV" ]; then
    echo "virtual environment does not exist, performing first time setup"
    sudo python -m venv "$VENV"
    sudo chmod -R 777 ../
fi

source .venv/bin/activate
pip install -r requirements.txt
fastapi run app.py
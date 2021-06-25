#!/bin/bash

# Load env variable and activate virtual environnement
source .env
source venv/bin/activate
  
# Start flask server
python3 app.py


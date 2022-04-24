#!/bin/sh

# Please run the below to create virtual environment before
# running this script to avoid cluttering your environment

# sudo apt-get install python3-venv    # If needed
# python3 -m venv .venv
# source .venv/bin/activate


pip3 install -r requirements.txt

cd ./src
uvicorn main:app --reload
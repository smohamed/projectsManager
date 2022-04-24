#!/bin/sh

pip3 install pipenv
pipenv --three
source $(pipenv --venv)/bin/activate
pip3 install -r requirements.txt

cd ./src
uvicorn main:app --reload
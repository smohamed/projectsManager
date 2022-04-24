#!/bin/sh

pip3 install -r requirements.txt

cd ./src
uvicorn main:app --reload
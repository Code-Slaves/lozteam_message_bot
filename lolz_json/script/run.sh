#!/bin/bash

cd ..
if [ ! -f "venv/bin/activate" ]
then
    virtualenv venv
fi
source venv/bin/activate
cd script
pip install -r requirements.txt
python bot.py


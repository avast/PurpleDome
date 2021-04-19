#!/bin/bash

# Init the system

sudo apt-get -y install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
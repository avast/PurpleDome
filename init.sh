#!/bin/bash

# Init the system

# Python basics
sudo apt-get -y install python3-venv

# Virtualisation defaults
sudo apt-get -y install vagrant virtualbox

# For document generation
sudo apt-get -y install latexmk texlive-fonts-recommended texlive-latex-recommended texlive-latex-extra

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Registering argcomplete globally. See README.md
sudo ./venv/bin/activate-global-python-argcomplete
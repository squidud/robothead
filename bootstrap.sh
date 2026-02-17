#!/bin/sh
set -e
sudo apt update
sudo apt install -y pigpio python3-pigpio
pip3 install -r requirements.txt
sudo systemctl enable --now pigpiod
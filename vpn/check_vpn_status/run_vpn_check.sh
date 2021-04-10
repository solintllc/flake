#!/bin/bash

# this script is useful because it sets up the virtual environment for the python script
# it is used by the LaunchAgent

source ~/.bin/check_vpn_status/venv/bin/activate
~/.bin/check_vpn_status/check_vpn_status.py

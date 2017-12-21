#!/bin/bash
if [ ! -f INSTALLED ]; then
    echo "===== Missing dependencies, running install.sh ====="
    sh install.sh && \
    touch INSTALLED
    echo "===== Installation finished! ====="
fi
echo "Flashing Arduino.."
sudo make burn
echo "Starting remote control"
python3 remote_control.py

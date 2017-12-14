#!/bin/bash

echo "Configuring Ground robot"

echo "Stopping any current remote_control process"
sudo systemctl stop remote_control

echo "Register remote control service to systemd"
sudo mv remote_control.service /etc/systemd/system/

echo "Enable remote control (run automatically at boot)"
sudo systemctl enable remote_control

echo "Start remote control"
sudo systemctl start remote_control


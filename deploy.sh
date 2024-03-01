#!/bin/bash

SOURCE_FOLDER="memory_monitor"
UNIT_FILE="memory_monitor.service"
SCRIPT_FOLDER="/home/memory_monitor_scripts"

echo "== Deploying [$UNIT_FILE] service =="

if [ -f "$UNIT_FILE" ]; then

    echo "# Checking script folder"
    if [ ! -d "$SCRIPT_FOLDER" ]; then
        sudo mkdir -p "$SCRIPT_FOLDER"
        echo "-> Created script folder [$SCRIPT_FOLDER]"
    else
        echo "-> Script folder [$SCRIPT_FOLDER] already exists"
    fi

    echo "# Move source folder [$SOURCE_FOLDER] to script folder"
    sudo cp -r "$SOURCE_FOLDER" "$SCRIPT_FOLDER"

    echo "# Move unit file to /etc/systemd/system"
    sudo cp "$UNIT_FILE" /etc/systemd/system

    echo "# Reload daemon"
    sudo systemctl daemon-reload

    echo "# Start sevice"
    sudo systemctl start "$UNIT_FILE"

    echo "# Enable service"
    sudo systemctl enable "$UNIT_FILE"

    echo "[SUCCESS] Service ($UNIT_FILE) started and enabled"
    exit 0
else
    echo "[FAIL] Unit file ($UNIT_FILE) not found!"
    exit 1
fi
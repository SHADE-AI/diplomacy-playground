#!/bin/bash

# Create user
useradd -m diplomacy &&
    usermod -aG docker diplomacy

# Create game data and log directories
mkdir -p /home/diplomacy/data &&
    mkdir -p /home/diplomacy/logs &&
    chown -R diplomacy:diplomacy /home/diplomacy

# Install systemd units
cp docker.diplomacy_server.service /etc/systemd/system &&
    cp docker.diplomacy_webui.service /etc/systemd/system

# Enable servers
systemctl daemon-reload &&
    systemctl enable docker.diplomacy_server &&
    systemctl enable docker.diplomacy_webui

# Logrotate configurations
cp diplomacy_server /etc/logrotate.d/ &&
    cp diplomacy_webui /etc/logrotate.d/

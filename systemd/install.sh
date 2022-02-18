#!/bin/bash

# Create user
useradd -m shade 
usermod -aG docker shade

# Create game data and log directories
mkdir -p /home/shade/data &&
    mkdir -p /shade/diplomacy/logs &&
    chown -R shade:G-824842 /home/shade

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

#!/bin/bash

set -ex

useradd -m diplomacy &&
    usermod -aG docker diplomacy

mkdir -p /home/diplomacy/data &&
    mkdir -p /home/diplomacy/logs &&
    chown -R diplomacy:diplomacy /home/diplomacy

cp docker.diplomacy_server /etc/systemd/system &&
    cp docker.diplomacy_webui /etc/systemd/system

systemctl daemon-reload &&
    systemctl enable docker.diplomacy_server &&
    systemctl enable docker.diplomacy_webui

set +ex

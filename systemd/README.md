# Diplomacy Server Systemd

## Overview

This directory contains support files to install Diplomacy server and 
webUI as services owned by user `diplomacy` and managed by systemd. 
Furthermore, support is included for automated rotation of server and 
webUI logs.

## Requirements

1. Docker CE must be installed and active as a systemd service
2. Logrotate must be installed to handle the server and webui logs
3. Port 8432 and Ports 8434-8700 must be accessible to external connections
4. You must have sudo privileges

## Install

```shell
sudo bash install.sh
```

The game server should now begin starting up. You can check this with:

```shell
% systemctl status docker.diplomacy_server

docker.diplomacy_server.service - Diplomacy Server Service
     Loaded: loaded (/etc/systemd/system/docker.diplomacy_server.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2022-02-07 14:27:58 CST; 1h 4min ago
    Process: 113092 ExecStartPre=/usr/bin/docker exec docker.diplomacy_server.service stop (code=exited, status=1/FAILURE)
    Process: 113112 ExecStartPre=/usr/bin/docker rm docker.diplomacy_server.service (code=exited, status=1/FAILURE)
    Process: 113118 ExecStartPre=/usr/bin/docker pull tacc/diplomacy_server (code=exited, status=0/SUCCESS)
   Main PID: 113130 (docker)
      Tasks: 9 (limit: 4462)
     Memory: 17.0M
     CGroup: /system.slice/docker.diplomacy_server.service
             └─113130 /usr/bin/docker run --rm --name docker.diplomacy_server.service -v /home/diplomacy/data:/data -v /home/diplomacy/logs:/logs -p 8432:8432 -p 8434-8700:8434-8700 ->

Feb 07 14:27:57 hostname systemd[1]: Starting Diplomacy Server Service...
Feb 07 14:27:57 hostname docker[113092]: Error: No such container: docker.diplomacy_server.service
Feb 07 14:27:57 hostname docker[113112]: Error: No such container: docker.diplomacy_server.service
Feb 07 14:27:57 hostname docker[113118]: Using default tag: latest
Feb 07 14:27:58 hostname docker[113118]: latest: Pulling from tacc/diplomacy_server
Feb 07 14:27:58 hostname docker[113118]: Digest: sha256:e7159f0e2f6224099d3f6f9130e5fc648aa2d2987d4f63fec733797c9981a630
Feb 07 14:27:58 hostname docker[113118]: Status: Image is up to date for tacc/diplomacy_server:latest
Feb 07 14:27:58 hostname docker[113118]: docker.io/tacc/diplomacy_server:latest
Feb 07 14:27:58 hostname systemd[1]: Started Diplomacy Server Service.
```

The first time the server runs, it will need to build a cache file, which can take 5-10 minutes. It will not be possible to log into the server until the cache file has been generated. Afterwards, server and game data will be stored on disk at `/home/diplomacy/data` and will not need to be regenerated. When the server has finished launching, it will be possible to connect to it via websockets on port 8432. Each active Diplomacy game will also be assigned a DAIDE server running on a port between 8434 and 8700. 

The web UI should be started up at this point. You can check this with `systemctl status docker.diplomacy_webui`. You can also check it out on the web at http://$hostname:3000. 

## Logs

Logs for the game server and webUI are streamed to `/home/diplomacy/logs`. They will be rotated as per the logrotate configurations bundled in this directory.


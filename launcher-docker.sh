#!/bin/bash

LOCAL_IP=$(ipconfig getifaddr en0)

GAME_ID="$1"
GAME_HOST="${2:-$LOCAL_IP}"
CONTAINER="${3:-randombot}"

for POWER in "AUSTRIA" "ENGLAND" "FRANCE" "GERMANY" "ITALY" "RUSSIA" "TURKEY"; do
    echo "Playing $POWER in $GAME_ID on $GAME_HOST using $CONTAINER"
    docker run -d -e DIPLO_GAMEID=$GAME_ID -e DIPLO_POWER=$POWER -e DIPLO_HOST=$GAME_HOST -it $CONTAINER
    sleep 1
done

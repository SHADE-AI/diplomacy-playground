#!/bin/bash

# Launches 7 Albert bots for head-to-head play
# Note that Albert does not appear to support selection of a specific power

LOCAL_IP=$(ipconfig getifaddr en0)

GAME_ID="$1"
DAIDE_PORT="$2"
GAME_HOST="${3:-$LOCAL_IP}"
BOT_NAME="albert"
#BOT_NAME="dumbbot"
INSTANCES="${5:-1}"

for i in $(seq 1 ${INSTANCES}); do
    echo "Play $POWER in $GAME_ID on $GAME_HOST:$DAIDE_PORT using $BOT_NAME from $CONTAINER"
    docker run -d -it tacc/albert-ai $BOT_NAME $GAME_HOST $DAIDE_PORT
    sleep 10
done

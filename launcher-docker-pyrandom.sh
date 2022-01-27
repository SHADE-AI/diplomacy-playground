#!/bin/bash

LOCAL_IP=$(ipconfig getifaddr en0)

GAME_ID="$1"
GAME_HOST="${2:-$LOCAL_IP}"
GAME_PORT="${3:-8432}"
CONTAINER="${4:-tacc/pyrandom}"
INSTANCES="${5:-7}"

for i in $(seq 1 ${INSTANCES}); do
    # for POWER in "AUSTRIA" "ENGLAND" "FRANCE" "GERMANY" "ITALY" "RUSSIA" "TURKEY"; do
    docker run -d ${CONTAINER} --game-id ${GAME_ID} --username ${CONTAINER} --host ${GAME_HOST} --port ${GAME_PORT}
    sleep 10
done

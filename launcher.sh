#!/bin/bash

GAME_ID="$1"
for POWER in "AUSTRIA" "ENGLAND" "FRANCE" "GERMANY" "ITALY" "RUSSIA" "TURKEY"; do
    echo "$POWER"
    python -m bots.random_bot $GAME_ID $POWER --username $POWER >logs/$GAME_ID.$POWER.log &
    sleep 1
done

#!/bin/bash

GAME_ID="$1"
for POWER in "AUSTRIA" "ENGLAND" "FRANCE" "GERMANY" "ITALY" "RUSSIA" "TURKEY"; do
    python bots/pyrandom/pyrandom.py --game-id $GAME_ID --power-name $POWER --username $POWER >logs/$GAME_ID.$POWER.log &
    sleep 1
done

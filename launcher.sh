#!/bin/bash

GAME_ID="$1"
for POWER in "AUSTRIA" "ENGLAND" "FRANCE" "GERMANY" "ITALY" "RUSSIA" "TURKEY"; do
    echo "$POWER"
    set -ex
    python bots/random/random_bot.py --game-id $GAME_ID --power-name $POWER --username $POWER >logs/$GAME_ID.$POWER.log &
    set +ex
    sleep 1
done

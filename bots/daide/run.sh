#!/bin/bash

export BOT_NAME="$1"
export BOT_HOST="$2"
export BOT_PORT="$3"
export BOT_POWER="$4"
export BOT_PASSCODE="${5:-0}"

echo "----------------------------"
echo "Trying to launch a $BOT_NAME bot that will connect to port $BOT_PORT"
echo "----------------------------"

# Set path
case "$BOT_NAME" in
randbot)
    export BOT_PATH="/code/daide-client/bin/randbot"
    ;;

dumbbot)
    export BOT_PATH="/code/daide-client/bin/dumbbot"
    ;;
holdbot)
    export BOT_PATH="/code/daide-client/bin/holdbot"
    ;;
*)
    echo $"Usage: $0 {dumbbot|holdbot|randbot} {hostname} {port_number} [power] [passcode]"
    exit 1
    ;;
esac

# Optional - specify power to play
if [ -n "${BOT_POWER}" ]; then BOT_POWER="-r${BOT_POWER}:${BOT_PASSCODE}"; fi

# Launching and sleeping forever
echo "Launching bot..."
set -x
$BOT_PATH -i$BOT_HOST -p$BOT_PORT ${BOT_POWER}

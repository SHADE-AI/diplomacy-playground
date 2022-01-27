#!/bin/bash

export BOT_NAME="$1"
export BOT_HOST="$2"
export BOT_PORT="$3"

echo "----------------------------"
echo "Trying to launch a $BOT_NAME bot that will connect to port $BOT_PORT"
echo "----------------------------"

# Detecting display
export DISPLAY=:99
if xhost >&/dev/null; then
    echo "... Successfully detected a display"
else
    echo "... Launching display :99"
    Xvfb :99 -screen 0 1024x768x16 &
fi

# Finding path
case "$BOT_NAME" in
albert)
    export BOT_PATH="/data/albert/Albert.exe"
    ;;

dumbbot)
    export BOT_PATH="/data/dumbbot/DumbBot.exe"
    ;;

*)
    echo $"Usage: $0 {albert|dumbbot} {hostname} {port_number}"
    exit 1
    ;;
esac

# Launching and sleeping forever
echo "Launching bot..."

set -x
wine $BOT_PATH -i$BOT_HOST -p$BOT_PORT -h

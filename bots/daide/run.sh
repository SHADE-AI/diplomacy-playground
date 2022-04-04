#!/bin/bash

#export BOT_NAME="$1"
#export BOT_HOST="$2"
#export BOT_PORT="$3"
#export BOT_POWER="$4"
#export BOT_PASSCODE="${5:-0}"

export BOT_NAME=""
export BOT_HOST=""
export BOT_PORT=""
export BOT_POWER=""
export BOT_PASSCODE=""
CMD=""

#OPTIONS
#--bot_name
#--host [hostname maps to -s]
#--port [daide port]
#--power [power]
#--bot_passcode

while [ $# -gt 0 ]; do
	case "$1" in
		-s | --host)
			BOT_HOST="$2"
			shift 2
			CMD="${CMD} -s${BOT_HOST}"
		;;
		-i)
			BOT_HOST="$2"
			shift 2
			CMD="${CMD} -i${BOT_HOST}"
		;;
		-p | --port)
			BOT_PORT="$2"
			shift 2
			CMD="${CMD} -p${BOT_PORT}"
		;;
		-u | --power)
			BOT_POWER="$2"
			BOT_POWER=`echo ${BOT_POWER} | awk '{print substr($0,0,3)}'`
			shift 2
		;;
		-b | --bot_name)
			BOT_NAME="$2"
			shift 2
		;;
		--bot_passcode)
			BOT_PASSCODE="$2"
			shift 2
		;;
		*)
			echo "Unknown option ${1}"
			exit 1
		;;
	esac

done

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
#echo $BOT_PATH -i$BOT_HOST -p$BOT_PORT ${BOT_POWER}
$BOT_PATH $CMD ${BOT_POWER}

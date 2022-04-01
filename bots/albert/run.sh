#!/bin/bash


HOST=""
DAIDE_PORT=""
POW=""
NEVER_ALLY_MODE=""
TOURNAMENT_MODE=""
GUNBOAT_MODE=""
CMD=""

export BOT_PATH="/data/albert/Albert.exe"

usage() {

	echo "Usage: run.sh [options]"
	echo "   -s | --host	HOSTNAME"
	echo "   -p | --port	DAIDE_PORT"
	echo "   -u | --power	POWER"
	echo "   -i 		IP_ADDRESS"
	echo "   -n		set never ally mode"
	echo "   -g		set gunboat mode"
	echo "   -t		set tournament mode"
}

#OPTS=$(getopt --options s:i:p:u:b:ngt --longoptions 'host:,port:,power:,bot:' -n input -- $@)
#eval set -- "$OPTS"

#echo $OPTS


while [ $# -gt 0 ]
do
	echo $1
	case "$1" in 
		-s | --host)
		   HOST="$2"
		   CMD="${CMD} -s${HOST}"
		   shift 2
		;;

		-i)
		   HOST="$2"
		   CMD="${CMD} -i${HOST}"
		   shift 2
		;;

		-p | --port)
		   DAIDE_PORT="$2"
		   CMD="${CMD} -p${DAIDE_PORT}"
		   shift 2
		;; 

		-u | --power)
                   POW="$2"
                   #CMD="${CMD} -r${POW}"
		   shift 2
		;;

	#	-b | --bot)
	#	   name="$2"
	#	   case "$name" in
	#		albert)
	#			export BOT_PATH="/data/albert/Albert.exe"
	#		;;
	#
	#		dumbbot)
	#			export BOT_PATH="/data/dumbbot/DumbBot.exe"
	#		;;
	#	   esac		
	#	   shift 2
	#	;;

		-n)
		   #-n parameter makes Albert treat all powers as an enemy at all times
                   CMD="${CMD} -n"
		   shift
		;;   


		-g)
		   #-g gunboat game without press, no matter what level the server has set game to
	   	   CMD="${CMD} -g"
		   shift	
		;;

		-t)
		   #-t tournament mode. Parameter disables any delay timers in code
		   CMD="${CMD} -t"
		   shift
		;;

		*)
			echo "Unrecognized option '$1'"
			usage
			exit 1
		;;
		
		:)
			usage
			exit 1
		;;
		   
	esac
done


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

set -x
# Launching and sleeping forever
echo "wine ${BOT_PATH} ${CMD} -h"
wine ${BOT_PATH} ${CMD} -h



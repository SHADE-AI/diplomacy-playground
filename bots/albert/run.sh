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
	echo "   -s	HOSTNAME"
	echo "   -i	IP_ADDRESS"
	echo "   -p	DAIDE_PORT"
	echo "   -u	POWER"
	echo "   -n	set never ally mode"
	echo "   -g     set gunboat mode"
	echo "   -t     set tournament mode"
}

while getopts "s:i:p:u:ngt" options; do
	case "${options}" in
		s)
			#-s option specifies hostname
			HOST=${OPTARG}
			CMD="${CMD} -s${HOST}"
		;;

		i)
			#-i option specifies IP address, use either s or i, not both
			HOST=${OPTARG}
			CMD="${CMD} -i${HOST}"
		;;

		p)
			#-p DAIDE PORT
			DAIDE_PORT=${OPTARG}
			CMD="${CMD} -p${DAIDE_PORT}"
		;;

		u)
			#-u power to play
			POW=${OPTARG}
			CMD="${CMD} -r${POW}"
		;;

		n)
			#-n parameter makes Albert treat all powers as an enemy at all times
			CMD="${CMD} -n"
		;;

		g)
			#-g gunboat game without press, no matter what level the server has set game to
			CMD="${CMD} -g"
		;;

		t)
			#-t tournament mode. Parameter disables any delay timers in code
			CMD="${CMD} -t"
		;;

		*)
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


# Launching and sleeping forever
echo "wine ${BOT_PATH} ${CMD}"

wine $BOT_PATH $CMD -h

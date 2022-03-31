#!/bin/bash

#input specifies where game engine data will be stored

working_dir=$1
diplo_server_path="${working_dir}/diplo_server"
pswd="tacobot"
port=8432
daide_port_range="8434:8700"

echo "Launching game engine locally"
if [ -d $diplo_server_path ]
then
	echo "Server data saving at ${diplo_server_path}"
	if [ ! -d "${diplo_server_path}/data" ]
	then
		echo "${diplo_server_path}/data doesn't exist"
	fi

	if [ ! -d "${diplo_server_path}/logs" ]
	then
		echo "${diplo_server_path}/logs doesn't exist"
	fi
 
	if [ ! -d "${diplo_server_path}/maps" ]
	then
		echo "${diplo_server_path}/maps doesn't exist"
	fi
else
	echo "Creating directory ${diplo_server_path}"
	echo "Creating ${diplo_server_path}/[data,logs,maps]"
	mkdir ${diplo_server_path}
	mkdir "${diplo_server_path}/data"
	mkdir "${diplo_server_path}/logs"
	mkdir "${diplo_server_path}/maps"
fi

singularity run --env DIPLOMACY_ADMIN_PASSWORD=$pswd --env SERVER_PORT=$port --env DAIDE_PORT_RANGE=$daide_port_range --bind "${diplo_server_path}/data":/data --bind "${diplo_server_path}/logs":/logs --bind "${diplo_server_path}/maps":/maps docker://tacc/diplomacy_server

The Albert bot is capable of advanced Diplomacy play, 
including the ability to do press up to DAIDE level 30. 

It is distributed as a set of Windows installers (as 
it is a Windows executable), but Phil Paquette packaged 
up the Albert executable inside a Singularity container 
for use on Linux HPC systems. 

This container has been exported to a Docker container using the 
following commands using the `Dockerfile` and `run.sh` files 
included in this directory.

```shell
% curl -skL -O "https://f002.backblazeb2.com/file/ppaquette-public/containers/albert_ai/albert_dumbbot-1.2.sif"
% singularity sif list albert_dumbbot-1.2.sif
% singularity sif dump 2 albert_dumbbot-1.2.sif > data.squash
% unsquashfs -dest data data.squash
% echo "data.squash" > .dockerignore
% echo "*.sif" >> .dockerignore
% docker build -t albert-ai .
```

Usage:

```shell
# Get usage
% docker run -it albert-ai --help

Usage: run.sh [options]
   -s | --host	HOSTNAME
   -p | --port	DAIDE_PORT
   -u | --power	POWER
   -i 		IP_ADDRESS
   -n		set never ally mode
   -g		set gunboat mode
   -t		set tournament mode
```
Note 1: for consistency, we have included --power [POWER] as an option. However, as this implementation
is based on that of Paquette et al., it does not appear possible to set the power for Albert. The 
run.sh script that is executed on container launch will ignore the power option. --host OR -i AND -p
are required. 

Note 2: if you are running the diplomacy game engine server locally (i.e. localhost) you must use
the following alias: --host host.docker.internal

```shell
# Run bot in background
% docker run -d albert-ai --host host.docker.internal -p 8436
ca9cf81b69e1b073d00c3f43d66cd9f368ce40a17af968a748fc838b810766f

# Get logs
% docker logs -f ca9cf81b69e1b073d00c3f43d66cd9f368ce40a17af968a748fc838b810766f
----------------------------
Trying to launch a  bot that will connect to port
----------------------------
... Launching display :99
+ echo 'wine /data/albert/Albert.exe  -shost.docker.internal -p8436 -h'
+ wine /data/albert/Albert.exe -shost.docker.internal -p8436 -h
wine /data/albert/Albert.exe  -shost.docker.internal -p8436 -h
0010:err:ole:marshal_object couldn't get IPSFactory buffer for interface {00000131-0000-0000-c000-000000000046}
0010:err:ole:marshal_object couldn't get IPSFactory buffer for interface {6d5140c1-7436-11ce-8034-00aa006009fa}
0010:err:ole:StdMarshalImpl_MarshalInterface Failed to create ifstub, hres=0x80004002
0010:err:ole:CoMarshalInterface Failed to marshal the interface {6d5140c1-7436-11ce-8034-00aa006009fa}, 80004002
0010:err:ole:get_local_server_stream Failed: 80004002
0009:fixme:event:wait_for_withdrawn_state window 0x10052/a00001 wait timed out

# Note that the errors beginning with 0010:err:ole are from the WINE emulator and are harmless.
```
To confirm that the Albert bot successfully connected to the game engine server, you can view
the server log (if running locally) file. The following message indicates that Albert connected 
to the game engine:

```shell
2022-04-13 14:17:19 diplomacy.daide.server[89761] INFO Connection from client [('127.0.0.1', 60437)]
2022-04-13 14:17:19 diplomacy.daide.connection_handler[89761] INFO [11] initial message
2022-04-13 14:17:19 diplomacy.daide.connection_handler[89761] INFO [11] request:[NME ( A l b e r t ) ( v 6 . 0 . 1 )]
2022-04-13 14:17:20 diplomacy.daide.connection_handler[89761] INFO [11] response:[YES ( NME ( A l b e r t ) ( v 6 . 0 . 1 ) )]
2022-04-13 14:17:20 diplomacy.daide.connection_handler[89761] INFO [11] response:[MAP ( s t a n d a r d )]
2022-04-13 14:17:20 diplomacy.daide.connection_handler[89761] INFO [11] request:[MDF]
```

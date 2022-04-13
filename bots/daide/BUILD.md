# DAIDE implementation: dumbbot|holdbot|randbot 

Containerized version of the bots implemented in the DAIDE client at https://github.com/diplomacy/daide-client.git.

Build:
```
$ docker build -t daide-bots .
```

Usage:
```shell
$ docker run -it daide-bots --help
Usage: run.sh [options]
--bot_name 	[dumbbot|holdbot|randbot]
--host 		[hostname]
--port		[daide port]
--power		[power name]
--bot_passcode	[unused]
```

Note 1: right now --power and --bot_passcode options are ignored. The engine daide server code
needs to be modified to accept daide power assignments.

Connect to existing game on remote engine:
```shell
$ docker run -it daide-bots --bot_name dumbbot --host 129.114.99.77 --port 8496
----------------------------
Trying to launch a dumbbot bot that will connect to port 8496
----------------------------
Launching bot...
+ /code/daide-client/bin/dumbbot -s129.114.99.77 -p8496
```

Note 2: it appears that --host will only take IP_ADDRESS

Game engine server output:
```
2022-04-13 20:42:15 diplomacy.daide.server[6] INFO Connection from client [('70.123.34.230', 61031)]
2022-04-13 20:42:15 diplomacy.daide.connection_handler[6] INFO [18] initial message
2022-04-13 20:42:15 diplomacy.daide.connection_handler[6] INFO [18] request:[NME ( D u m b B o t ) ( 8 ~ 3 )]
2022-04-13 20:42:16 diplomacy.daide.connection_handler[6] INFO [18] response:[YES ( NME ( D u m b B o t ) ( 8 ~ 3 ) )]
2022-04-13 20:42:16 diplomacy.daide.connection_handler[6] INFO [18] response:[MAP ( s t a n d a r d )]
2022-04-13 20:42:16 diplomacy.daide.connection_handler[6] INFO [18] request:[MDF]
```

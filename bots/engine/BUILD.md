# Diplomacy game server

This containerized version of Paquette's game server has been modified to launch rapidly by injecting pre-computed data into the image. When first launching the diplomacy server (e.g., `python -m diplomacy.server.run`), possible convoys for all maps in diplomacy/maps are computed and cached either in ~/.cache/diplomacy or [working-dir]/maps as convoy_paths_cache.pkl. Calculating these convoy paths is time consuming. Subsequent launches of the server will load this file and the engine will not re-compute convoy paths. convoy_paths_cache.pkl is copied into the container in Dockerfile. Additional processing of each map file also occurs and these data (e.g., abuts) are stored in server.json. On first launch, server.json does not exist so processing occurs, thereby slowing initial launch. We have initialized a server.json (no games, or users) and copied it into the container. By including the above-mentioned files, the game server launches very quickly. 

Build:
```shell
$ docker build -t diplomacy-engine .
```

Usage:
```
$ docker run -e [optional vars] -it diplomacy-engine
optional environment variables
  DAIDE_PORT_RANGE	[default 8434:8600]
  SERVER_PORT		[default 8432]
  SERVER_DIR		[default /code]
  LOGFILE		[default diplomacy.server.log]
  
  NOTE: when running with Singularity, SERVER_DIR/data and SERVER_DIR/logs will need to be bound to host filesystem.
 
```

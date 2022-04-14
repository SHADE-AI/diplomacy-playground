# DipNetSL

This is a docker implementation of Paquette et al. DipNetSL agent. The model parameters are imbedded and 
the TF model server is run within the container along with a python script to instantiate a DipNetSLPlayer
and facilitate game play. This is intended to assist in development. It is more computationally efficient to run a single TF server and connect multiple agents to it, rather than having one TF server per DipNetSL
player.

Build:
```shell
$ wget https://f002.backblazeb2.com/file/ppaquette-public/benchmarks/neurips2019-sl_model.zip
$ mkdir bot_neurips2019-sl_model
$ unzip neurips2019-sl_model.zip -d bot_neurips2019-sl_model/
$ docker build -t dipnet_sl . 
```

Usage:
```shell
$ docker run -it dipnet_sl --help
--host 		HOST [default localhost]
--port 		PORT [default 8432]
--game_id 	GAME_ID
--power		POWER

#connect to remote game engine
$ docker run -it dipnet_sl --game_id test_game --host shade.tacc.utexas.edu --power TURKEY
```


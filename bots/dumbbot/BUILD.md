# Dumbbot: containerized, python implementation

This implementation of David Norman's [dumbbot]<http://www.daide.org.uk/s0003.html> uses the RuleBasedPlayer class from diplomacy_research.players attributed to Paquette et al. 

Build:
```shell
$ docker build -t dumbbot-python .
```

Usage:
```
$ docker run -it dumbbot-python --help
arguments
  --game_id GAME_ID
  --power POWER
  --host HOST [default localhost]
  --port PORT [default 8432]
  --ruleset RULESET [(default) dumbbot | easy]
  
 #connect to game server running on local host
 docker run -it dumbbot-python --game_id test_game --power AUSTRIA --host host.docker.internal --port 8432 --ruleset dumbbot
 
```

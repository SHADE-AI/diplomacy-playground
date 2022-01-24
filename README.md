# DIPLOMACY PLAYGROUND

This is an experimental repository for scripted launching of 
Diplomacy games and having them be joined and played by bots. The objective to to define a lightweight set of interfaces that 
can be used by any performer in the SHADE program to run 
automated games. 

## GAME SERVERS

The game server and UI front end are Dockerized and can be 
launched together using Docker Compose. 

```shell
docker-compose up -d
```

The Diplomacy server will be available at `localhost:8432` while the 
WebUI is at `http://localhost:3000`. 

The compose configuration the local `./data` directory as the `data` volume 
for the Diplomacy server. This allows the server and game files to be accessed 
persistently outside of the containerized environment. 


Notes:
1. The administrator credentials are currently admin/password but we will be changing the server code to accept these via environment variable to that new server instances do not launch with an insecure password
2. Per-game DAIDE servers run on ports 8000-8999. This may change in the future. 

## SCRIPTS

### Create a Game

It is possible to programatically create a game tailored to automated gameplay.

```shell
% python -m scripts.create_game -h
usage: create_game.py [-h] [--game-id GAME_ID] [--rules RULES [RULES ...]] [--deadline DEADLINE]
                      [--daide-port DAIDE_PORT] [--host HOST] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --game-id GAME_ID     Game ID
  --rules RULES [RULES ...]
                        Game rules
  --deadline DEADLINE   Game deadline
  --daide-port DAIDE_PORT
                        Game DAIDE Port
  --host HOST           Server Host
  --port PORT           Server Port
  ```

Here's an example:

```shell
% python -m scripts.create_game --deadline 2
2022-01-24 11:45:23 diplomacy.client.connection[45360] INFO Trying to connect.
2022-01-24 11:45:23 diplomacy.client.connection[45360] INFO Connection succeeds.
{
    "id": "mWxKLdRxp0mk9",
    "deadline": 2,
    "map_name": "standard",
    "registration_password": null,
    "rules": [
        "POWER_CHOICE",
        "REAL_TIME"
    ],
    "status": "forming",
    "daide_port": 8886
}
```

### Launch a single bot

TBD. See contents of `launcher.sh`

### Launch an ensemble of random bots to play a game

```shell
% bash launcher.sh mWxKLdRxp0mk9
```

Go to the web UI, log in as administrator, find the same game ID, and join as an Omniscient observer to watch the game play out. Game logs will for each bot process will be stored under `logs/GAMEID.POWER.log`.

Notes: The multi-launch interface is definitely going to change to accept a structured configuration that might look something like this:

```json
{
    "game_id": "mWxKLdRxp0mk9",
    "powers": {
        "AUSTRIA": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"},
        "ENGLAND": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"},
        "FRANCE": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"},
        "GERMANY": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"},
        "ITALY": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"},
        "RUSSIA": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"},
        "TURKEY": {"container": "<container_name>", "command": "<command> (overrides ENTRYPOINT)"}
    }
}
```

Containers will run processes that accept a core configuration via form of environment variables. Examples might include `HOST`, `PORT`, `POWER`, `DAIDE_PORT`, and so on. 

Realistically, this is too simplistic an approach, as we will need to allow for bots that are an ensemble of containers (i.e. bot process, database process, message queue, model server, etc.) but the core concept is that the bot process will be containerized and be parameterized via environment variables.

## BOTS

We have a handful of demonstration bots that show the basics of connecting to a server and playing autonomously. 

### Random Bot


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

### Launch the same ensemble, but containerized

Build container `randombot` from `./bots/random`

```shell
% ./build_random.sh
...
[+] Building 0.1s (10/10) FINISHED

Run an ensemble of randombots to play a random Diplomacy game

```shell
% ./launcher-docker.sh AWo33q4X0W60J
[Several containers will launch and attach to your game server]
```

You can see that both the game server and the bots are running containerized now.

```shell
% docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                    NAMES
1cfe5eefcbc0   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             amazing_elbakyan
ab0570d0d133   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             epic_jennings
717449f46fc4   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             sharp_cori
8c1438845a79   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             priceless_mirzakhani
3179b8c9f2f6   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             flamboyant_jemison
44ccc6f8c5a6   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             admiring_perlman
e19a097f7fdc   randombot                     "python /code/random…"   3 minutes ago    Up 3 minutes                             agitated_montalcini
34f693f0f978   diplomacy-playground_server   "python -m diplomacy…"   49 minutes ago   Up 49 minutes   0.0.0.0:8432->8432/tcp   diplomacy-playground_server_1
2455369a16d6   diplomacy-playground_webui    "npm start"              49 minutes ago   Up 49 minutes   0.0.0.0:3000->3000/tcp   diplomacy-playground_webui_1
```

## BOTS

We have a handful of demonstration bots that show the basics of connecting to a server and playing autonomously. 

### Random Bot

There is a bot that performs random play in bots/random. It can be run directly or containerized.


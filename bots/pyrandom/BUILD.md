Build a containerized version of the pyrandom bot:

```shell
% docker build -t pyrandom .
```
Get usage information:

```shell
% docker run -it pyrandom -h
usage: pyrandom.py [-h] [--game-id GAME_ID]
                   [--power-name {AUSTRIA,ENGLAND,FRANCE,GERMANY,ITALY,RUSSIA,TURKEY}]
                   [--username USERNAME] [--password PASSWORD] [--host HOST]
                   [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --game-id GAME_ID     Game Id
  --power-name {AUSTRIA,ENGLAND,FRANCE,GERMANY,ITALY,RUSSIA,TURKEY}
                        Power Name
  --username USERNAME   Client Name
  --password PASSWORD   Client Name
  --host HOST           Game Host
  --port PORT           Game Port
```

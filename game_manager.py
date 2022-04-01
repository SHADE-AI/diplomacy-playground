import logging
import json
import sys
import asyncio
import time
import random
import uuid

from hashids import Hashids
from diplomacy.client.connection import connect
from scripts.create_game import create_game


#LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]
HASHID_SALT = "4srNxD5jXDwfCvgEQ92x8L7x"


def new_hashid(salt=None):
    """Return a new, randomly-generated hashid"""
    if salt is None:
        salt = HASHID_SALT
    hashids = Hashids(salt=salt)
    _uuid = uuid.uuid1().int >> 64
    return hashids.encode(_uuid)


class Bot():

    def __init__(self, power, host, port, name, container, opts, type='bot', use_daide_port=False):
        self.type = type   #future options for human
        self.power = power
        self.host = host
        self.port = port
        self.daide_port = None
        self.name = name
        self.container = container
        self.use_daide_port = use_daide_port
        self.opts = opts

    def launch(self):

        if self.use_daide_port:
            self.port = self.daide_port

        command = ['singularity','run',self.container,
                   "--host %s" % self.host,
                   "--port %d" % self.port,
                   "--power %s" % self.power,
                   self.opts
                ]
        print(command)




class Game():

    #required: host, port, game_id, powers
    #optional: deadline, n_controls, rules, password
    def __init__(self, host, port, game):

        #set by user
        self.host = host
        self.port = port
        self.game_id = new_hashid()
        self.powers = list()

        self.deadline = 0
        self.n_controls = 7
        self.rules = None
        self.registration_password = None


        self.status = ""
        self.daide_port = None

        if "game_id" in game:
            self.game_id = game['game_id']
        else:
            print("Using generated game id " + self.game_id)
        if "deadline" in game:
            self.deadline = int(game['deadline'])
        if "n_controls" in game:
            self.n_controls = int(game['n_controls'])
        if "rules" in game:
            self.rules = game['rules']
        if "password" in game:
            self.registration_password = game['password']

        if "powers" in game:
            pows = game['powers']

            if len(pows.keys()) != 7:
                logging.error("Number of specified powers must be 7")
                sys.exit(1)

            for p in pows:
                if p not in POWERS:
                    logging.error("Invalid power name: " + p)
                    sys.exit(1)
                temp_p = pows[p]
                type = temp_p['type']
                name = temp_p['name']
                container = temp_p['container']
                opts = temp_p['options']

                use_daide_port = False
                if 'use_daide_port' in temp_p:
                    use_daide_port = True

                self.powers.append(Bot(p, self.host, self.port, name, container, opts, type, use_daide_port=use_daide_port))
        else:
            logging.error("No powers specified in config")
            sys.exit(1)

    def _set_daide_port(self, daide_port):

        #set daide port for game object then each bot object
        self.daide_port = daide_port
        for p in self.powers:
            p.daide_port = daide_port

    def _launch_game(self):

        #loop over bots and launch
        for p in self.powers:
            p.launch()


class GameManager():

    def __init__(self):

        self.working_dir = ""
        self.host = 'localhost'
        self.port = 8432
        self.game_list = list()

        self.loop = asyncio.get_event_loop()



    def create_games(self):

        for game in self.game_list:
            response = self.loop.run_until_complete(
                create_game(
                    game_id=game.game_id,
                    rules=game.rules,
                    deadline=game.deadline,
                    password=game.registration_password,
                    n_controls=game.n_controls,
                    hostname=game.host,
                    port=game.port
                  )
            )
            game._set_daide_port(response['daide_port'])

            game.status = response['status']

    def launch_games(self):

        for game in self.game_list:
            game._launch_game()

    def loadConfig(self,configFile):

        print("Loading config file: " + configFile)
        with open(configFile,"r") as f:
            config = json.load(f)

            if "working_dir" in config:
                self.working_dir = config['working_dir']

            if "game_engine" in config:
                self.host = config['game_engine']['host']
                self.port = config['game_engine']['port']
            else:
                logging.error("Game engine information not provided")
                sys.exit(1)

            if "games" in config:
                games = config["games"]
                n_games = len(games)
                print("Initializing %d games" % (n_games))

                #loop over games array and instantiate new game objects for each element
                for g in games:
                    self.game_list.append(Game(self.host, self.port, g))

            else:
                logging.error("Missing game configurations")
                sys.exit()








if __name__ == "__main__":

    configFile = "config.json"
    manager = GameManager()
    manager.loadConfig(configFile)
    manager.create_games()
    manager.launch_games()

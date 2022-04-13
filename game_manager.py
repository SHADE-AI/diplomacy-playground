import logging
import json
import sys
import asyncio
import time
import random
import uuid
import subprocess
import ray
import copy
import os

from tabulate import tabulate
import argparse
from hashids import Hashids
from diplomacy.client.connection import connect
from scripts.create_game import create_game
from diplomacy.utils.export import to_saved_game_format



#LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]
HASHID_SALT = "4srNxD5jXDwfCvgEQ92x8L7x"

POWERS = ['AUSTRIA', 'ENGLAND', 'FRANCE', 'GERMANY', 'ITALY', 'RUSSIA', 'TURKEY']


def new_hashid(salt=None):
    """Return a new, randomly-generated hashid"""
    if salt is None:
        salt = HASHID_SALT
    hashids = Hashids(salt=salt)
    _uuid = uuid.uuid1().int >> 64
    return hashids.encode(_uuid)

@ray.remote
class Bot():

    def __init__(self, power, game_id, host, port, container_launcher, name, container, opts, type='bot', use_daide_port=False):
        self.type = type   #future options for human
        self.game_id = game_id
        self.power = power
        self.host = host
        self.port = port
        self.daide_port = None
        self.name = name
        self.container = container
        self.use_daide_port = use_daide_port
        self.is_running = False
        self.opts = opts
        self.pid = None
        self.container_launcher = container_launcher

    def launch(self):

        command = list()
        if self.use_daide_port:
            self.port = self.daide_port

        #command = ['singularity','run',self.container,
        #           "--host %s" % self.host,
        #           "--port %d" % self.port,
        #           "--power %s" % self.power,
        #           "--game_id %s" % self.game_id,
        #           self.opts
        #        ]

        if self.container_launcher == 'docker':
            command = ['docker','run','-d',self.container,
            "--host","host.docker.internal",
            "--port", str(self.port),
            "--power", self.power,
            "--game_id", self.game_id,
            self.opts
            ]
        if self.container_launcher == 'singularity':
            command = ['singularity', 'run', self.container,
                       "--host", self.host,
                       "--port", str(self.port),
                       "--power", self.power,
                       "--game_id", self.game_id,
                       self.opts
            ]
        print(command)
        if "albert" in self.name:
            #sleep for 20 seconds
            print(self.name + " sleeping")
            time.sleep(20)
        res = subprocess.Popen(command)
        self.pid = res.pid

    def _set_daide_port(self, daide_port):
        self.daide_port = daide_port
        print(self.daide_port)
        return(True)

@ray.remote
class Observer2():

    def __init__(self, host, port, game_id):
        self.host = host
        self.port = port
        self.game_id = game_id
        self.logFile = ""
        self.header = list()
        self.header = copy.deepcopy(POWERS)
        self.header.insert(0, "init")
        print("Observer initialized for game: " + game_id)

    async def observe(self):
        connection = await connect(self.host, self.port)
        channel = await connection.authenticate("observer", 'password')
        game = await channel.join_game(game_id=self.game_id)

        print("Initializing observer for game: " + self.game_id)
        while not game.is_game_done:
            current_phase = game.get_current_phase()

            self.header[0] = current_phase
            num_units = ["n_units"]
            num_sc = ["n_sc"]
            num_home_sc = ["n_home_sc"]
            vote = ["vote"]
            goner = ["goner"]

            for p in POWERS:
                pow = game.get_power(p)
                num_units.append(len(pow.units))
                num_sc.append(len(pow.centers))
                num_home_sc.append(len(pow.homes))
                vote.append(pow.vote)
                goner.append(pow.goner)

            print(tabulate([num_units, num_sc, num_home_sc, goner, vote], headers=self.header))
            while current_phase == game.get_current_phase():
                # print(power + "\t" + "Local state:"+current_phase + "\t" + "Remote:" + game.get_current_phase())
                await asyncio.sleep(0.5)
        return(True)


@ray.remote
class Game():

    #required: host, port, game_id, powers
    #optional: deadline, n_controls, rules, password
    def __init__(self, host, port, working_dir, container_launcher, game):

        #set by user
        self.host = host
        self.port = port
        self.game_id = new_hashid()
        self.powers = list()
        self.working_dir = working_dir
        self.container_launcher = container_launcher

        self.deadline = 0
        self.n_controls = 7
        self.rules = None
        self.registration_password = None

        self.status = ""
        self.daide_port = None
        #self.observer = Observer.remote(self.host, self.port, self.game_id)

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

                self.powers.append(Bot.remote(p, self.game_id, self.host, self.port, self.container_launcher, name, container, opts, type, use_daide_port=use_daide_port))
        else:
            logging.error("No powers specified in config")
            sys.exit(1)


    def _get_config(self):

        conf = { 'game_id': self.game_id,
            'rules': self.rules,
            'deadline' : self.deadline,
            'registration_password' : self.registration_password,
            'n_controls' : self.n_controls,
            'hostname' : self.host,
            'port' : self.port
        }
        return(conf)

    def _set_daide_port(self, daide_port):

        #set daide port for game object then each bot object
        self.daide_port = daide_port
        print("Setting DAIDE Port: " + str(self.daide_port))
        for p in self.powers:
            p._set_daide_port.remote(daide_port)

    def format_observer_output(self, header, game):
        header[0] = game.get_current_phase()
        num_units = ["n_units"]
        num_sc = ["n_sc"]
        num_home_sc = ["n_home_sc"]
        vote = ["vote"]
        goner = ["goner"]

        for p in POWERS:
            pow = game.get_power(p)
            num_units.append(len(pow.units))
            num_sc.append(len(pow.centers))
            num_home_sc.append(len(pow.homes))
            vote.append(pow.vote)

        print(tabulate([num_units, num_sc, num_home_sc, vote], headers=header))
        print('')

    async def observe(self):
        connection = await connect(self.host, self.port)
        channel = await connection.authenticate("observer", 'password')
        game = await channel.join_game(game_id=self.game_id)

        header = list()
        header = copy.deepcopy(POWERS)
        header.insert(0, "init")


        print("Initializing observer for game: " + self.game_id)
        while not game.is_game_done:
            current_phase = game.get_current_phase()

            self.format_observer_output(header, game)

            while current_phase == game.get_current_phase():
                # print(power + "\t" + "Local state:"+current_phase + "\t" + "Remote:" + game.get_current_phase())
                await asyncio.sleep(0.5)

       
        self.format_observer_output(header, game)
        print(game.note)
        print(game.outcome)
        #write game state file to working_dir/game_state/game_id.json

        outDir = self.working_dir + "/game_state/"
        if not os.path.isdir(outDir):
            os.mkdir(outDir)
            print("Created output directory " + outDir)
        with open(outDir + self.game_id + ".json","w") as file:
            file.write(json.dumps(to_saved_game_format(game)))
        return(True)

    def _launch_game(self):


        #loop over bots and launch
        print("Launching game: " + self.game_id)
        for p in self.powers:
            p.launch.remote()


class GameManager():

    def __init__(self):

        self.working_dir = ""
        self.container_launcher = ""
        self.host = 'localhost'
        self.port = 8432
        self.game_list = list()
        self.games_to_init = list()

        self.loop = asyncio.get_event_loop()



    def create_games(self):

        # loop over games array and instantiate new game objects for each element

        for game in self.game_list:
            conf = ray.get(game._get_config.remote())
            response = self.loop.run_until_complete(
                create_game(
                    game_id=conf['game_id'],
                    rules=conf['rules'],
                    deadline=conf['deadline'],
                    password=conf['registration_password'],
                    n_controls=conf['n_controls'],
                    hostname=conf['hostname'],
                    port=conf['port']
                )
            )
            ray.get(game._set_daide_port.remote(daide_port=response['daide_port']))




    def launch_games(self):

        ray.get([game._launch_game.remote() for game in self.game_list])



    def loadConfig(self,configFile):

        print("Loading config file: " + configFile)
        with open(configFile,"r") as f:
            config = json.load(f)

            if "working_dir" in config:
                self.working_dir = config['working_dir']
                os.environ["WORKING_DIR"] = self.working_dir

            if "container_launcher" in config:
                self.container_launcher = config['container_launcher']
            else:
                #default to docker
                self.container_launcher = 'docker'

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

                for g in games:
                    self.game_list.append(Game.remote(self.host, self.port, self.working_dir, self.container_launcher, g))


            else:
                logging.error("Missing game configurations")
                sys.exit()








if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--redis", type=str, help="Redis password")
    parser.add_argument("--config", type=str, help="Game config file")
    args = vars(parser.parse_args())

    if args['redis'] is not None:
        ray.init(address='auto', _redis_password=args['redis'])
    else:
        ray.init()

    configFile = ""
    if args["config"] is None:
        #default
        configFile = "config2.json"
    else:
        configFile = args["config"]

    manager = GameManager()
    manager.loadConfig(configFile)
    manager.create_games()


    manager.launch_games()
    ray.get([game.observe.remote() for game in manager.game_list])



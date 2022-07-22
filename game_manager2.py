import logging
import json
import sys
import asyncio
import time
import random
import uuid
import subprocess
import copy
import os

from tabulate import tabulate
import argparse
from hashids import Hashids
from diplomacy.client.connection import connect
from scripts.create_game import create_game
from diplomacy.utils.export import to_saved_game_format

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



class GameManager():

    def __init__(self, args):

        #input options
        self.working_dir = ""
        self.host = "localhost"
        self.port = 8432
        self.game_id = new_hashid()
        self.deadline = 0
        self.n_controls = 7
        self.rules = None
        self.registration_password = None
        self.daide_port = None
        self.outfile = None
        self.status = ""
        self.connection = None
        self.channel = None
        self.game = None

        self.loop = asyncio.get_event_loop()

        if args['host'] is not None:
            self.host = args['host']
        if args['port'] is not None:
            self.port = args['port']
        if args['game_id'] is not None:
            self.game_id = args['game_id']
        if args['deadline'] is not None:
            self.deadline = args['deadline']
        if args['ncontrols'] is not None:
            self.n_controls = args['ncontrols']
        if args['rules'] is not None:
            self.rules = args['rules']
        if args['password'] is not None:
            self.registration_password = args['password']
        if args['daide_port'] is not None:
            self.daide_port = args['daide_port']
        if args['outdir'] is not None:
            self.outfile = args['outdir'] + "/" + self.game_id + ".json"
        else:
            self.outfile = self.game_id + ".json"

        self.loop.run_until_complete(self._connect())

    async def _connect(self):
        logging.info("Connecting to server")
        self.connection = await connect(self.host, self.port)
        self.channel = await self.connection.authenticate("manager", 'password')


    async def _create_game(self):
        self.game = await self.channel.create_game(
            game_id=self.game_id,
            rules=self.rules,
            deadline=self.deadline,
            n_controls=self.n_controls,
            registration_password=self.registration_password,
            daide_port=self.daide_port
        )
        game_data = {
            "id": self.game.game_id,
            "deadline": self.game.deadline,
            "map_name": self.game.map_name,
            "registration_password": self.game.registration_password,
            "rules": self.game.rules,
            "n_controls": self.game.n_controls,
            "status": self.game.status,
            "daide_port": self.game.daide_port
        }
        print(json.dumps(game_data, indent=4))

    def create_game(self):
        self.loop.run_until_complete(self._create_game())


    def format_observer_output(self):

        header = [self.game.get_current_phase()]

        num_units = ["n_units"]
        num_sc = ["n_sc"]
        num_home_sc = ["n_home_sc"]
        vote = ["vote"]
        goner = ["goner"]

        for p in POWERS:
            pow = self.game.get_power(p)
            num_units.append(len(pow.units))
            num_sc.append(len(pow.centers))
            num_home_sc.append(len(pow.homes))
            vote.append(pow.vote)
            header.append(p)

        tab = tabulate([num_units, num_sc, num_home_sc, vote], headers=header)
        return(tab)

    async def _observe(self):

        while not self.game.is_game_done:
            current_phase = self.game.get_current_phase()

            print(self.format_observer_output())
            print("\n\n")

            while current_phase == self.game.get_current_phase():
                #print("Local state:"+current_phase + "\t" + "Remote:" + self.game.get_current_phase())
                await asyncio.sleep(1)

        print("Game completed")
        print(self.game.note)
        print(self.game.outcome)

        if self.outfile is not None:
            print("Writing game data to " + self.outfile)
            to_saved_game_format(self.game, self.outfile)

    def observe(self):
        self.loop.run_until_complete(self._observe())


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='localhost', help="Game engine host")
    parser.add_argument("--port", type=int, default=8432, help="Port to connect to game engine host")
    parser.add_argument("--game_id", type=str, help="ID to assign game")
    parser.add_argument("--daide_port", type=int, help="Optional argument to assign specific port to game. If left blank a random port will be assigned")

    parser.add_argument("--ncontrols", type=int, help="Number of controllable powers. Default is 7")
    parser.add_argument("--deadline", type=int, help="Deadline (sec) for each round. Default is no deadline")
    parser.add_argument("--outdir", type=str, help="Directory with which to save game data.")
    parser.add_argument("--rules", nargs='*', type=str, help="Optional rules to set for the game.",default=['REAL_TIME', 'POWER_CHOICE'])
    parser.add_argument("--password", type=str, help="Password required to join game. Default None")

    args = vars(parser.parse_args())

    manager = GameManager(args)
    manager.create_game()
    manager.observe()



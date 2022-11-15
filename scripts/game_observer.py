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

class Observer():

    def __init__(self, args):

        #input options
        self.working_dir = ""
        self.host = "localhost"
        self.port = 8432
        self.game_id = ""
        self.poll_fq = 10
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
        if args['poll_fq'] is not None:
            self.poll_fq = args['poll_fq']
        if args['outdir'] is not None:
            self.outfile = args['outdir'] + "/" + self.game_id + ".json"
        else:
            self.outfile = self.game_id + ".json"

        self.loop.run_until_complete(self._connect())

    async def _connect(self):
        logging.info("Connecting to server")
        self.connection = await connect(self.host, self.port)
        self.channel = await self.connection.authenticate("observer", 'password')
        self.game = await self.channel.join_game(game_id=self.game_id)

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

        #print('HELLO"')
        #obsOut = args['outdir'] + "/" + "observer_" + self.game_id + ".log"
        #f = open(obsOut,"w")

        t1 = time.perf_counter()
        poll_counter = 0
        while not self.game.is_game_done:
            current_phase = self.game.get_current_phase()

            t2 = time.perf_counter()
            dt = t2 - t1

            logging.info(f"POLL: {poll_counter}   ELAPSED TIME: {dt:2.2f}")
            logging.info("\n"  + self.format_observer_output())
            logging.info("\n")
            #await asyncio.sleep(self.poll_fq)
            while current_phase == self.game.get_current_phase():
            #    #print("Local state:"+current_phase + "\t" + "Remote:" + self.game.get_current_phase())
                await asyncio.sleep(5)

        logging.info("Game completed")
        logging.info(self.game.note)
        logging.info(self.game.outcome)

        if self.outfile is not None:
            logging.info("Writing game data to " + self.outfile)
            to_saved_game_format(self.game, self.outfile)


    def observe(self):
        self.loop.run_until_complete(self._observe())


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='localhost', help="Game engine host")
    parser.add_argument("--port", type=int, default=8432, help="Port to connect to game engine host")
    parser.add_argument("--game_id", type=str, help="ID to assign game")
    parser.add_argument("--poll_fq", type=int, help="Frequency to poll the game state")

    parser.add_argument("--outdir", type=str, help="Directory with which to save game data.")

    args = vars(parser.parse_args())

    observer = Observer(args)
    observer.observe()


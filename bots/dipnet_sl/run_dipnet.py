import sys, os
sys.path.append("..") # Adds higher directory to python modules path.
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#os.environ['WORKING_DIR'] = "/work2/01262/jadrake/ls6/shade/research/dipnet_v_albert/"
#inside container
os.environ['WORKING_DIR'] = "/model/src/model_server/research"
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'cpp'

import argparse
import random
import time
import asyncio
import ujson as json
from tornado import gen
from diplomacy import Game, connect
from diplomacy.utils.export import to_saved_game_format

import diplomacy_research

from diplomacy_research.players.benchmark_player import DipNetSLPlayer
from diplomacy_research.utils.cluster import start_io_loop, stop_io_loop, is_port_opened

POWERS = ['AUSTRIA', 'ENGLAND', 'FRANCE', 'GERMANY', 'ITALY', 'RUSSIA', 'TURKEY']


#@gen.coroutine

async def test(hostname='localhost', port=8432):
    connection = await connect(hostname, port)
    channel = await connection.authenticate('random_user', 'password')
    games = await channel.list_games()
    for game in games:
        game_info = {
            "game_id":game.game_id,
            "phase":game.phase,
            "timestamp":game.timestamp,
            "timestamp_created":game.timestamp_created,
            "map_name":game.map_name,
            "observer_level":game.observer_level,
            "controlled_powers":game.controlled_powers,
            "rules":game.rules,
            "status":game.status,
            "n_players":game.n_players,
            "n_controls":game.n_controls,
            "deadline":game.deadline,
            "registration_password":game.registration_password
        }
        print(game_info)
    print(games)

async def launch(hostname, port, game_id, power_name, outdir):
    print("Waiting for tensorflow server to come online")
    serving_flag = False
    while not serving_flag:
        serving_flag = is_port_opened(9501)
        print("+")
        await asyncio.sleep(1)
    print("tensorflow server online")
    
    await play(hostname, port, game_id, power_name, outdir)

async def play(hostname, port, game_id,power_name, outdir):

    print("DipNetSL joining game: " + game_id + " as " + power_name)
    connection = await connect(hostname, port)
    channel = await connection.authenticate('dipnet_' + power_name, 'password')
    game = await channel.join_game(game_id=game_id, power_name=power_name)


    dipnet_player = DipNetSLPlayer()


    t1 = time.perf_counter()
    i = 0

    # Playing game
    while not game.is_game_done:

        current_phase = game.get_current_phase()

        dipnet_orders = await dipnet_player.get_orders(game, power_name)
        print("Phase: " + current_phase)
        print("Orders: ")
        print(dipnet_orders)
        await game.set_orders(power_name = power_name, orders = dipnet_orders, wait=False)

        while current_phase == game.get_current_phase():
            await asyncio.sleep(2)

    # Saving to disk
    #outfile = outdir + "/" + game_id + ".json"
    #with open(outfile, 'w') as file:
        #file.write(json.dumps(to_saved_game_format(game)))
    #    game_data = to_saved_game_format(game)
        #game_data['players'] = {'dipnetsl':dipnet_power, 'dumbbots':other_powers}
    #    file.write(json.dumps(game_data))

    t2 = time.perf_counter()
    print(f"TIMING: {t2-t1}:0.4")
    print('-'*30 + 'GAME COMPLETE' + '-'*30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--game_id', type=str)
    parser.add_argument("--power", type=str)
    parser.add_argument('--outdir', type=str)
    args = parser.parse_args()
    host = args.host
    port = args.port
    game_id = args.game_id
    outdir = args.outdir
    power = args.power

    #default
    if host == None:
        host = 'localhost'
    if port == None:
        port = 8432
    if game_id == None:
        print("Game ID required")
        sys.exit(1)

    #start_io_loop(main)
    asyncio.run(launch(hostname=host, port=port, game_id=game_id,power_name=power, outdir=outdir))
    #asyncio.run(create_game(game_id))
    #asyncio.run(test())

import sys


import argparse

import time
import asyncio
from diplomacy import Game, connect
from diplomacy_research.players import RuleBasedPlayer
from diplomacy_research.players.rulesets import easy_ruleset, dumbbot_ruleset

POWERS = ['AUSTRIA', 'ENGLAND', 'FRANCE', 'GERMANY', 'ITALY', 'RUSSIA', 'TURKEY']


#@gen.coroutine
async def play(game_id, power, host, port, ruleset):


    bot = ""
    if ruleset == 'dumbbot':
        bot = RuleBasedPlayer(dumbbot_ruleset)
        print("Initializing dumbbot player")
    elif ruleset == 'easy':
        bot = RuleBasedPlayer(easy_ruleset)
        print("Initializing easy ruleset player")
    else:
        print("Ruleset not found. Must be dumbbot or easy")
        sys.exit(1)

    connection = await connect(host, port)
    channel = await connection.authenticate(ruleset + "_" + power, 'password')
    game = await channel.join_game(game_id=game_id, power_name=power)


    t1 = time.perf_counter()
    i = 0

    while not game.is_game_done:
        current_phase = game.get_current_phase()
        orders = await bot.get_orders(game, power)
        print("Power: " + power + "\t"  "Phase" + current_phase)
        print("Orders: ")
        print(orders)
        await game.set_orders(power_name=power, orders=orders, wait=False)

        while current_phase == game.get_current_phase():
            #print(power + "\t" + "Local state:"+current_phase + "\t" + "Remote:" + game.get_current_phase())
            await asyncio.sleep(0.1)


    t2 = time.perf_counter()
    print(f"TIMING: {t2-t1}")
    #stop_io_loop()

async def launch(game_id, power, host, port, ruleset):
    await asyncio.gather(*[play(game_id, power, host, port, ruleset) for power in POWERS])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game_id', type=str)
    parser.add_argument('--power', type=str)
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--ruleset', type=str)
    args = parser.parse_args()
    game_id = args.game_id
    power = args.power
    host = args.host
    port = args.port
    ruleset = args.ruleset


    #game_id = "dumb101"

    if host == None:
        host = 'localhost'
    if port == None:
        port = 8432
    if game_id == None:
        print("Game ID required")
        sys.exit(1)
    if ruleset == None:
        print("Using default ruleset: dumbbot")
        ruleset = 'dumbbot'


    asyncio.run(play(game_id, power, host, port, ruleset))
    #asyncio.run(launch(game_id, power, host, port, ruleset))

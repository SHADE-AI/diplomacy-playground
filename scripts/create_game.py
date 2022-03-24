import argparse
import asyncio
import json
import random
import uuid
from diplomacy.client.connection import connect
from diplomacy.utils import exceptions
from hashids import Hashids

POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]
RULES = ["REAL_TIME", "POWER_CHOICE"]

HASHID_SALT = "4srNxD5jXDwfCvgEQ92x8L7x"


def new_hashid(salt=None):
    """Return a new, randomly-generated hashid"""
    if salt is None:
        salt = HASHID_SALT
    hashids = Hashids(salt=salt)
    _uuid = uuid.uuid1().int >> 64
    return hashids.encode(_uuid)


async def create_game(
    game_id=None,
    rules=None,
    deadline=None,
    password='',
    n_controls = 7,
    hostname="localhost",
    port=8432,
):
    """Creates a game on the Diplomacy server"""
    connection = await connect(hostname, port)
    channel = await connection.authenticate("random_user", "password")
    if game_id is None:
        game_id = new_hashid()

    game = await channel.create_game(
        game_id=game_id,
        rules=rules,
        deadline=deadline,
        n_controls = n_controls,
        registration_password=password,
    )
    game_data = {
        "id": game.game_id,
        "deadline": game.deadline,
        "map_name": game.map_name,
        "registration_password": game.registration_password,
        "rules": game.rules,
        "n_controls": n_controls,
        "status": game.status,
        "daide_port":game.daide_port
    }
    print(json.dumps(game_data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--game_id", type=str, help="Game ID")
    parser.add_argument("--rules", nargs="+", default=RULES, help="Game rules")
    parser.add_argument("--deadline", type=int, default=0, help="Game deadline")
    parser.add_argument("--n_controls", type=int, default=7, help="Num. of controlled powers (default 7)")
    parser.add_argument("--password", type=str, help="Optional game password")
    #parser.add_argument(
    #    "--daide-port",
    #    type=int,
    #    help="Game DAIDE Port",
    #)

    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Server Host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8432,
        help="Server Port",
    )

    args = vars(parser.parse_args())
    asyncio.run(
        create_game(
            game_id=args["game_id"],
            rules=args["rules"],
            deadline=args["deadline"],
            password=args["password"],
            hostname=args["host"],
            port=args["port"],
            n_controls = args["n_controls"],
            #daide_port=args["daide_port"],
        )
    )

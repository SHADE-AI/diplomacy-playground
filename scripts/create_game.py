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
    password=None,
    daide_port=None,
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
        # registration_password=password,
        daide_port=daide_port,
    )
    game_data = {
        "id": game.game_id,
        "deadline": game.deadline,
        "map_name": game.map_name,
        "registration_password": game.registration_password,
        "rules": game.rules,
        "status": game.status,
        "daide_port": game.daide_port,
    }
    print(json.dumps(game_data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--game-id", type=str, help="Game ID")
    parser.add_argument("--rules", nargs="+", default=RULES, help="Game rules")
    parser.add_argument("--deadline", type=int, default=1, help="Game deadline")
    # parser.add_argument("--password", type=str, help="Optional game password")
    parser.add_argument(
        "--daide-port",
        type=int,
        help="Game DAIDE Port",
    )

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
            # password=args["password"],
            hostname=args["host"],
            port=args["port"],
            daide_port=args["daide_port"],
        )
    )

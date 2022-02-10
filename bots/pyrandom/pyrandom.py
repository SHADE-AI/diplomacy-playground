#
import argparse
import asyncio
import copy
import hashlib
import lorem
import os
import random
import uuid
from diplomacy.client.connection import connect
from diplomacy.communication.requests import Vote
from diplomacy.utils import exceptions, strings

PASSWORD_SALT = os.environ.get("PASSWORD_SALT", "6kVL6Xw38QxBVx5DDuKuybucXbBRAz6R")
POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]
RESPONSES = {
    "AUSTRIA": "Ich habe Ihre Nachricht erhalten",
    "ENGLAND": "I received your message",
    "FRANCE": "J'ai reçu ton message",
    "GERMANY": "Ich habe Ihre Nachricht erhalten",
    "ITALY": "Ho ricevuto il tuo messaggio",
    "RUSSIA": "Я получил ваше сообщение",
    "TURKEY": "Mesajını aldım",
}

# (yes, no, neutral)
DRAW_VOTE_PROBS = {
    "AUSTRIA": (0.33, 0.33, 0.33),
    "ENGLAND": (0.25, 0.5, 0.25),
    "FRANCE": (0.5, 0.1, 0.4),
    "GERMANY": (0.1, 0.8, 0.1),
    "ITALY": (0.33, 0.33, 0.33),
    "RUSSIA": (0.33, 0.66, 0.00),
    "TURKEY": (0.33, 0.33, 0.33),
}


def message_id():
    return uuid.uuid4().hex[0:8]


def validate_username(username: str):
    return True


def get_password(username: str, salt: str = None):
    if salt is None:
        salt = PASSWORD_SALT
    return hashlib.pbkdf2_hmac(
        "sha256", username.encode("utf-8"), salt.encode("utf-8"), 10000
    ).hex()


async def play(game_id, power_name, username, hostname="localhost", port=8432):
    """Play as the specified power"""
    connection = await connect(hostname, port)
    admin_channel = await connection.authenticate("bot", "bot")

    # Waiting for the game, then joining it
    while not (await admin_channel.list_games(game_id=game_id)):
        await asyncio.sleep(1.0)
    # Join game as observer to get list of uncontrolled games
    admin_game = await admin_channel.join_game(game_id=game_id)
    power_name = admin_game.get_random_power_name()

    # Join game as selected power to play
    username = "{0}.{1}".format(username, power_name)
    channel = await connection.authenticate(username, get_password(username))
    game = await channel.join_game(game_id=game_id, power_name=power_name)

    # Playing game
    while not game.is_game_done:
        current_phase = game.get_current_phase()

        # Submitting orders
        if game.get_orderable_locations(power_name):
            possible_orders = game.get_all_possible_orders()
            orders = [
                random.choice(possible_orders[loc])
                for loc in game.get_orderable_locations(power_name)
                if possible_orders[loc]
            ]
            print(
                "[%s/%s] - Submitted: %s"
                % (power_name, game.get_current_phase(), orders)
            )
            await game.set_orders(power_name=power_name, orders=orders, wait=True)

        # Implement random voting
        try:
            vote = Vote(
                power_name=power_name, vote=random.choice(strings.ALL_VOTE_DECISIONS)
            )
            print("{0} vote for draw: {1}".format(power_name, vote.vote))
            await game.vote(vote)
        except Exception:
            pass

        # Get extant messages for reply
        # Messages are formatted Type:Id:Message for the purposes of debugging

        destinations = copy.copy(POWERS)
        message_queue = []
        # game.messages.items is the list of messages that the current power
        # can see - it includes messages originated by other powers, global
        # messages, and messages sent by other powers in reply to a message
        # the current power sent
        for k, v in game.messages.items():
            print(v.sender, v.recipient, v.phase, v.message)
            if v.recipient != "GLOBAL":
                if not v.message.startswith("REPLY:"):
                    fields = v.message.split(":")
                    msg_id = fields[1]
                    # The message ID is extracted from the greeting and included
                    # in the reply so we can verify whether the bot is correctly answering a greeting
                    response = "REPLY:{0}:{1} {2}".format(
                        msg_id, RESPONSES[power_name], v.sender
                    )
                    message_queue.append((v.sender, response))
                    try:
                        destinations.remove(v.sender)
                    except Exception:
                        pass

        # Send an outbound message to one of the remaining powers we have not replied to
        try:
            destinations.remove(power_name)
        except Exception:
            pass
        destination_power = random.choice(destinations)
        # Send a greeting one out every 10 iterations
        if random.randrange(1, 10) == 5:
            message_queue.append(
                (
                    destination_power,
                    "HELLO:{0}:Greetings to {1} from {2}".format(
                        message_id(), power_name, destination_power
                    ),
                )
            )

        # Send power messages that are queued up
        for msg in message_queue:
            try:
                power_message = game.new_power_message(msg[0], msg[1])
                await game.send_game_message(message=power_message)
            except exceptions.GameNotPlayingException:
                pass

        # Send a GLOBAL message
        try:
            # Don't do it evert turn
            if random.randrange(1, 10) == 5:
                # For fun, use a lorem ipsum generator to make the press release!
                global_message = game.new_global_message(
                    "PRESS:{0}:{1}:{2}".format(
                        message_id(), power_name, lorem.get_paragraph(1)
                    ),
                )
                await game.send_game_message(message=global_message)
        except exceptions.GameNotPlayingException:
            # I might be able to avoid this by checking some game state variable
            pass

        # Waiting for game to be processed
        while current_phase == game.get_current_phase():
            await asyncio.sleep(0.1)

    # A local copy of the game can be saved with to_saved_game_format
    # To download a copy of the game with messages from all powers, you need to export the game as an admin
    # by logging in as 'admin' / 'password'


async def launch(game_id, power_name, username, hostname, port):
    """Creates and plays a network game"""
    # await create_game(game_id)
    await play(game_id, power_name, username, hostname, port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-id",
        type=str,
        default=os.environ.get("DIPLO_GAMEID"),
        help="Game Id",
    )
    parser.add_argument(
        "--power-name",
        type=str,
        default=os.environ.get("DIPLO_POWER"),
        choices=POWERS,
        help="Power Name",
    )
    parser.add_argument(
        "--username",
        type=str,
        default=os.environ.get("DIPLO_USERNAME"),
        help="Client Name",
    )
    parser.add_argument(
        "--password",
        type=str,
        default=os.environ.get("DIPLO_PASSWORD"),
        help="Client Name",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.environ.get("DIPLO_HOST", "0.0.0.0"),
        help="Game Host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=os.environ.get("DIPLO_PORT", "8432"),
        help="Game Port",
    )
    args = vars(parser.parse_args())

    asyncio.run(
        launch(
            game_id=args["game_id"],
            power_name=args["power_name"],
            username=args["username"],
            hostname=args["host"],
            port=args["port"],
        )
    )

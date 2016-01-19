#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import random
import argparse
import signal
import time

# Add source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from lib.environment import TrainingEnvironment, ArenaEnvironment
from lib.models import Action
import lib.bots as bots
import lib.heuristics as heuristics
from lib.logging import Logger
from lib.utility import hero_utility


def sigint_handler(signal, frame):
    """Signal handler for ctrl-c

    It sets shutdown_requested to true when ctrl-c is pressed.
    If shutdown_requested is already true, it exits directly.
    """
    global shutdown_requested
    if shutdown_requested:
        print("/!\ Aborting.")
        sys.exit(1)
    else:
        print("(*) Shutdown requested. Please wait the end of the game...")
        print("(i) Press ctrl-c again to exit immediately, losing the game.")
        shutdown_requested = True

# Define the command line arguments
parser = argparse.ArgumentParser(
    description="Run a bot."
)
parser.add_argument(
    "-k", "--key",
    required=True,
    help="the bot key used to connect to the server"
)
parser.add_argument(
    "-b", "--bot",
    default="MaxnBot",
    help="the bot to use in the game",
)
parser.add_argument(
    "-e", "--heuristic",
    default="EloGoldHeuristic",
    help="the heuristic to use in the bot",
)
parser.add_argument(
    "-m", "--mode",
    default="training",
    choices=["training", "arena"],
    help="the mode to use in the game",
)
parser.add_argument(
    "-n", "--number",
    default=1,
    type=int,
    help="the number of games to play",
)

#
# Main
#
args = parser.parse_args()
project_dir = os.path.join(os.path.dirname(__file__), "..")

# We don't want to discover that the bot class does not exist when the game
# already started.
bot_class = getattr(bots, args.bot)
heuristic_class = getattr(heuristics, args.heuristic)

print("(*) Game mode: {}".format(args.mode))
print("(*) Bot: {}".format(args.bot))
print("(*) Number of games to play: {}".format(args.number))

# Setup a signal handler to catch ctrl-c signal
shutdown_requested = False
signal.signal(signal.SIGINT, sigint_handler)

# Main loop of the script
for game_number in range(1, args.number + 1):
    # Check if the user pressed ctrl-c
    if shutdown_requested:
        break

    logger = Logger(project_dir + "/run")
    try:
        print("=== Starting game {} (of {})".format(
            game_number,
            args.number
        ))

        if args.mode == "arena":
            print("(*) Waiting for opponents...")
            print("/!\ If you exit now we will lose the game")
            env = ArenaEnvironment(args.key)
        else:
            env = TrainingEnvironment(args.key)

        heurisitc = heuristic_class()
        bot = bot_class(env.hero_id, heurisitc)

        # Store bot settings
        logger.set_game_id(env.get_status().id)
        logger.set_header(timestamp=True)
        logger.set_header(bot=args.bot)
        logger.set_header(heuristic=args.heuristic)
        logger.set_header(mode=args.mode)
        logger.set_header(max_game_number=args.number)
        logger.set_header(game_number=game_number)
        logger.set_header(hero_id=env.hero_id)
        logger.set_header(elo=env.get_status().heroes[env.hero_id].elo)

        # Main loop of the game
        while not env.get_status().finished:
            print("(*) Game {}/{}".format(game_number, args.number))
            print("(*) View url:", env.view_url)
            status = env.get_status()
            logger.store_status(status.turn, env.get_status_text())
            print("(*) Status:\n", status, sep="")
            action = bot.think(status)
            print("(*) Action:", action)
            env.send_action(action)

        print("(*) Game over.")
        hero = status.heroes[env.hero_id]
        elo_diff = int(hero_utility(status, hero.id))
        print("(*) Elo: {} {:+}".format(hero.elo, elo_diff))

        # Log result
        logger.set_header(finished=True)
        logger.set_header(elo_diff=elo_diff)
        logger.write_data()

        print("(*) Wait a couple of seconds...")
        time.sleep(3)

    except Exception as e:
        print("/!\ Uncaught exception:", e)

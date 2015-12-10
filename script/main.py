#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import random
import argparse
import math

# Add source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from lib.environment import TrainingEnvironment, ArenaEnvironment
from lib.models import Action
import lib.bots as bots
from lib.logging import Logger
from lib.utility import hero_utility

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
    "-m", "--mode",
    default="training",
    choices=["training", "arena"],
    help="the mode to use in the game",
)

#
# Main
#
args = parser.parse_args()

# We don't want to discover that the bot class does not exist when the game
# already started.
bot_class = getattr(bots, args.bot)

print("(*) Game mode: {0}".format(args.mode))
print("(*) Bot: {0}".format(args.bot))

if args.mode == "arena":
    print("(*) Waiting for opponents...")
    print("/!\ If you exit now, technically we will lose the game")
    env = ArenaEnvironment(args.key)
else:
    env = TrainingEnvironment(args.key)

bot = bot_class(env.hero_id)
project_dir = os.path.join(os.path.dirname(__file__), "..")
logger = Logger(project_dir + "/run", env.get_status().id)

while not env.get_status().finished:
    print("(*) View url:", env.view_url)
    status = env.get_status()
    logger.store_status(status.turn, env.get_status_text())
    print("(*) Status:\n", status, sep="")
    action = bot.think(status)
    print("(*) Action:", action)
    env.send_action(action)

print("(*) Game over.")
hero = status.heroes[env.hero_id]
elo_diff = math.floor(hero_utility(status, hero.id))
print("(*) Elo: {0} {1:+}".format(hero.elo, elo_diff))

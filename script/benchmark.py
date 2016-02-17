#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import random
from timeit import Timer

# Add source directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../test"))

from status_samples import get_status_samples
from lib.environment import TrainingEnvironment
from lib.models import Action, Map, Status
from lib.simulator import simulate
import lib.bots as bots
import lib.heuristics as heuristics


def report(measurements):
    return "    min: {min:.3}, max: {max:.3}".format(
        min=min(measurements),
        max=max(measurements)
    )

# Build sample models
samples_status = []
game_maps = {}
for status_dict in get_status_samples():
    game_id = status_dict["game"]["id"]
    if game_id not in game_maps:
        game_maps[game_id] = Map(status_dict["game"]["board"]["tiles"])
    status = Status(status_dict["game"], game_maps[game_id])
    samples_status.append(status)

#
# 1. Measure simulation speed
#
print("(*) Client simulation speed")
t = Timer(
    lambda: simulate(
        # a random state
        random.choice(samples_status),
        # a random action
        random.choice(list(Action))
    )
)
measurements = t.repeat(repeat=5000, number=1)
print(report(measurements))

#
# 2. Measure Bot speed
#
bots = [
    (bots.RandomBot, None),
    (bots.SimpleGoalBot, None),
    (bots.MaxnBot, heuristics.GoldHeuristic),
    (bots.MaxnBot, heuristics.EloGoldHeuristic),
    (bots.MaxnBot, heuristics.MineGoldHeuristic),
    (bots.ParanoidBot, heuristics.GoldHeuristic),
    (bots.ParanoidBot, heuristics.EloGoldHeuristic),
    (bots.ParanoidBot, heuristics.MineGoldHeuristic),
]
for bot_class, heuristic_class in bots:
    if heuristic_class is None:
        print("(*) {} speed".format(bot_class.__name__))
        bot = bot_class(0)
    else:
        print("(*) {} + {} speed".format(
            bot_class.__name__,
            heuristic_class.__name__
        ))
        bot = bot_class(0, heuristic_class())
    t = Timer(
        lambda: bot.think(random.choice(samples_status))  # a random state
    )
    measurements = t.repeat(repeat=30, number=1)
    print(report(measurements))

#
# 3. Measure server response time
#
if len(sys.argv) < 2:
    print("/!\ No bot key in arguments, "
          "skipping server response time benchmark.")
else:
    print("(*) Server response time")
    bot_key = sys.argv[1]
    env = TrainingEnvironment(bot_key)
    t = Timer(lambda: env.send_action(Action.stay))
    # Don't repeat too much, we don't want to overload the server
    measurements = t.repeat(repeat=3, number=1)
    print(report(measurements))

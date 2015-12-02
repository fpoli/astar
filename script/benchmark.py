#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import random
from timeit import Timer

# Add source directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../test"))

from status_samples import get_status_samples
from lib.environment import TrainingEnvironment
from lib.models import Action, Map, Status
from lib.simulator import simulate
import lib.bots as bots

def report(measurements):
    return "    min: {min:.3}, max: {max:.3}".format(
        min=min(measurements),
        max=max(measurements)
    )

bots = [
    bots.RandomBot,
    bots.MaxnBot,
    bots.ParanoidBot
]

# Ensure that this script is being executed (not imported)
if __name__ == "__main__":

    # Build sample models
    samples_status = []
    for status_dict in get_status_samples():
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)
        samples_status.append(status)

    #
    # 1. Measure simulation speed
    #
    print("(*) Client simulation speed")
    t = Timer(
        lambda: simulate(
            # a random state
            random.choice(samples_status),
            # 4 random actions
            [random.choice(list(Action)) for i in range(4)]
        )
    )
    measurements = t.repeat(repeat=5000, number=1)
    print(report(measurements))

    #
    # 2. Measure Bot speed
    #
    for bot_class in bots:
        print("(*) {0} speed".format(bot_class.__name__))
        bot = bot_class(0)
        t = Timer(
            lambda: bot.think(random.choice(samples_status))  # a random state
        )
        measurements = t.repeat(repeat=30, number=1)
        print(report(measurements))

    #
    # 2. Measure server response time
    #
    print("(*) Server response time")
    if len(sys.argv) < 2:
        print("No bot key in arguments, skipping benchmark.")
    else:
        bot_key = sys.argv[1]
        env = TrainingEnvironment(bot_key)
        t = Timer(lambda: env.send_action(Action.stay))
        # Don't repeat too much, we don't want to overload the server
        measurements = t.repeat(repeat=3, number=1)
        print(report(measurements))

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
from lib.environment import TrainingEnvironment
from lib.models import Action
import lib.bots as bots
import random

# Ensure that this script is being executed (not imported)
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: {0} <key>".format(sys.argv[0]))
        exit(0)

    else:
        key = sys.argv[1]
        env = TrainingEnvironment(key)
        bot = bots.MaxnBot(env.hero_id)

        while True:
            print("Status:\n", status, sep="")
            action = bot.think(status)
            print("Action:", action)
            env.send_action(action)

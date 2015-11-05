# -*- coding: UTF-8 -*-

from enum import Enum

Action = Enum("Action", "north south west east stay")


def str_to_action(s):
    conversion = {
        "North": Action.north,
        "South": Action.south,
        "East": Action.west,
        "West": Action.east,
        "Stay": Action.stay
    }
    assert(s in conversion)
    return conversion[s]

# -*- coding: UTF-8 -*-

from enum import Enum

Action = Enum("Action", "north south west east stay")


def str_to_action(s):
    conversion = {
        "North": Action.north,
        "South": Action.south,
        "East": Action.east,
        "West": Action.west,
        "Stay": Action.stay
    }
    assert(s in conversion)
    return conversion[s]


def action_to_dir(a):
    conversion = {
        Action.north: (0, -1),
        Action.south: (0, 1),
        Action.west: (-1, 0),
        Action.east: (1, 0),
        Action.stay: (0, 0)
    }
    assert(a in conversion)
    return conversion[a]

# -*- coding: UTF-8 -*-

from enum import Enum

Action = Enum("Action", "north south west east stay")

__str_to_action_conversion = {
    "North": Action.north,
    "South": Action.south,
    "East": Action.east,
    "West": Action.west,
    "Stay": Action.stay
}

__action_to_dir_conversion = {
    Action.north: (0, -1),
    Action.south: (0, 1),
    Action.west: (-1, 0),
    Action.east: (1, 0),
    Action.stay: (0, 0)
}


def str_to_action(s):
    assert(s in __str_to_action_conversion)
    return __str_to_action_conversion[s]


def action_to_dir(a):
    assert(a in __action_to_dir_conversion)
    return __action_to_dir_conversion[a]

# -*- coding: UTF-8 -*-

import ujson as json
import os


def get_status_samples_dict():
    """Loads status samples files.

    Returns:
        {game_id, {turn, status_dict}}: a dictionary with all the status
           samples stored by game and turn.
    """
    status_samples = {}

    # Load sample status json files
    for basepath, _, files in os.walk("status_samples"):
        for file in files:
            if file.endswith(".json"):
                with open(basepath + "/" + file, "r") as infile:
                    game_id, end = file.split("_")
                    turn, _ = end.split(".")
                    if game_id not in status_samples:
                        status_samples[game_id] = {}
                    status_samples[game_id][int(turn)] = json.load(infile)

    return status_samples


def get_status_samples_pairs():
    """Loads status samples files.

    Returns:
        [(status_dict, status_dict)]: a list of pairs of status samples
          representing consecutive turns.
    """
    status_pairs = []
    status_samples = get_status_samples_dict()

    for game_id, turns in status_samples.items():
        for turn, status_before in turns.items():
            turn_after = turn + 4
            status_after = turns.get(turn_after, None)
            if status_after is not None:
                status_pairs.append(
                    (status_before, status_after)
                )

    return status_pairs

def get_status_samples():
    """Loads status samples files.

    Returns:
        [status_dict]: a list of status samples.
    """
    return [
        item
        for game in get_status_samples_dict().values()
        for item in game.values()
    ]

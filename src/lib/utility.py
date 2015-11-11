# -*- coding: UTF-8 -*-

import math


def calculate_elo_diff(player_elo, opponent_elo, player_score):
    """Elo points earned (or lost) by the player against an opponent.

    Arguments:
        player_elo (int): the elo of the player.
        opponent_elo (int): the elo of the opponent.
        player_score (float): the players score against opponent:
          - 1   if player defeated opponent
          - 0.5 in case of draw
          - 0   if opponent defeated player

    Returns:
        int: the elo points earned (or lost, if negative) by the player
          against an opponent.
    """
    expected = 1 / (1 + math.pow(10, (opponent_elo - player_elo) / 400))
    k_factor = 16
    diff = k_factor * (player_score - expected)
    return int(diff)


def hero_utility(status, hero_id):
    """ Computes the utility function for a hero.

    The utility is the number of points earned in the global rank.

    Note: this is a zero sum utility.

    Arguments:
        status (Status): the final status of a game.
        hero_id (int): the id of the hero.

    Returns:
        int: the hero utility value.
    """

    diff = 0
    default_elo = 1200
    hero = status.heroes[hero_id - 1]

    if hero.elo is None:
        hero_elo = default_elo
    else:
        hero_elo = hero.elo

    for opponent_id in range(4):
        if opponent_id == hero_id:
            continue

        opponent = status.heroes[opponent_id - 1]

        if hero.gold > opponent.gold:
            hero_score = 1
        elif hero.gold < opponent.gold:
            hero_score = 0
        else:
            hero_score = 0.5

        if opponent.elo is None:
            opponent_elo = default_elo
        else:
            opponent_elo = opponent.elo

        diff += calculate_elo_diff(hero_elo, opponent_elo, hero_score)

    return diff


def utility(status):
    """ Computes the utility function (zero sum) for each hero.

    Note: this is a zero sum utility.

    Arguments:
        status (Status): the final status of a game.

    Returns:
        (int, int, int, int): the hero utility value for each hero.
    """
    return tuple([
        hero_utility(status, i)
        for i in range(4)
    ])

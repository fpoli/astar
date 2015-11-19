# -*- coding: UTF-8 -*-

import math


def calculate_elo_diff(hero_elo, opponent_elo, hero_score):
    """Elo points earned (or lost) by the hero against an opponent.

    Arguments:
        hero_elo (int): the hero's elo.
        opponent_elo (int): the opponent's elo.
        hero_score (float): the hero's score against opponent:
          * 1   if hero won
          * 0.5 in case of draw
          * 0   if opponent won

    Returns:
        float: the elo points earned (or lost, if negative) by the hero
          against an opponent.
    """
    expected = 1 / (1 + math.pow(10, (opponent_elo - hero_elo) / 400))
    k_factor = 16
    diff = k_factor * (hero_score - expected)
    return diff


def calculate_score(status, hero_id, opponent_id):
    """Calculate the score of hero against opponent.

    Note: the score is not the utiliy.

    Arguments:
        status (Status): the game status.
        hero_id (int): the hero's id.
        opponent_id (int): the opponent's id.

    Returns:
        float: the hero's score against opponent:
          * 1   if hero won
          * 0.5 in case of draw
          * 0   if opponent won
    """
    hero = status.heroes[hero_id - 1]
    opponent = status.heroes[opponent_id - 1]

    if hero.gold > opponent.gold:
        return 1
    elif hero.gold < opponent.gold:
        return 0
    else:
        return 0.5


def hero_utility(status, hero_id, scoring_function=calculate_score):
    """Computes the utility function for a hero.

    The utility is the number of points earned in the global rank.

    Note: this is a zero sum utility.

    Arguments:
        status (Status): the final status of a game.
        hero_id (int): the id of the hero.
        scoring_function: the function that calculates the score between two
            heroes. (default: calculate_score).

    Returns:
        float: the hero utility value.
    """

    diff = 0
    default_elo = 1200
    hero = status.heroes[hero_id - 1]

    if hero.elo is None:
        hero_elo = default_elo
    else:
        hero_elo = hero.elo

    for opponent_id in range(1, 5):
        if opponent_id == hero_id:
            continue

        opponent = status.heroes[opponent_id - 1]

        hero_score = scoring_function(status, hero_id, opponent_id)

        if opponent.elo is None:
            opponent_elo = default_elo
        else:
            opponent_elo = opponent.elo

        diff += calculate_elo_diff(hero_elo, opponent_elo, hero_score)

    return diff


def utility(status, scoring_function=calculate_score):
    """ Computes the utility function (zero sum) for each hero.

    Note: this is a zero sum utility.

    Arguments:
        status (Status): the final status of a game.
        scoring_function: the function that calculates the score between two
            heroes. (default: calculate_score).

    Returns:
        (float, float, float, float): the hero utility value for each hero.
    """
    return tuple([
        hero_utility(status, hero_id, scoring_function)
        for hero_id in range(1, 5)
    ])

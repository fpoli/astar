# -*- coding: UTF-8 -*-

from lib.utility import hero_utility, utility


def gold_score(status, hero_id, opponent_id):
    """ Calculate the score of hero against opponent, considering gold only.

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
    hero = status.heroes[hero_id]
    opponent = status.heroes[opponent_id]

    # Calculate the gold at the end of the game
    hero_turns = status.remaining_turns_of_hero(hero_id)
    opponent_turns = status.remaining_turns_of_hero(opponent_id)

    hero_gold = hero.gold + hero_turns * hero.mine_count
    opponent_gold = opponent.gold + opponent_turns * opponent.mine_count

    gold_diff = hero_gold - opponent_gold

    # the game just started --> game_progress = ~0
    # the game is about to finish --> game_progress = ~1
    game_progress = status.turn / status.max_turns

    # Sigmoid function with codomain (0, 1)
    # This is a good heuristic if the game just started
    smoothed_value = (gold_diff / (1 + abs(gold_diff)) + 1) / 2

    # Step function
    # This is a good heuristic if the game is about to finish
    if gold_diff > 0:
        step_value = 1
    elif gold_diff < 0:
        step_value = 0
    else:
        step_value = 0.5

    # Linear combination of the two values, depending on game_progress
    return smoothed_value * (1 - game_progress) + step_value * game_progress


def hero_heuristic(status, hero_id):
    """ Heuristic that estimates the utility for a hero, considering gold
    only.

    Arguments:
        status (Status): the game status.
        hero_id (int): the hero's id.

    Returns:
        float: the estimated utility for the hero.
    """
    return hero_utility(status, hero_id, gold_score)


def heuristic(status):
    """ Heuristic that estimates the utility for each hero, considering gold
    only.

    Arguments:
        status (Status): the game status.

    Returns:
        (float, float, float, float): the estimated utility for each hero.
    """
    return utility(status, gold_score)

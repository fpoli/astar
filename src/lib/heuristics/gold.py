# -*- coding: UTF-8 -*-

from lib.utility import utility


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

    # Sigmoid function with codomain (0, 1)
    return (gold_diff / (1 + abs(gold_diff)) + 1) / 2


def heuristic(status):
    """ Heuristic that estimates the utility for each hero, considering gold
    only.

    Returns:
        (float, float, float, float): the estimated utility for each hero.
    """
    return utility(status, gold_score)

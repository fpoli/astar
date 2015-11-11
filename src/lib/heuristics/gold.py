# -*- coding: UTF-8 -*-

from lib.utility import utility


def gold_score(status, hero_id, opponent_id):
    hero = status.heroes[hero_id - 1]
    opponent = status.heroes[opponent_id - 1]

    # Calculate the gold at the end of the game
    hero_turns = status.remaining_turns_of_hero(hero_id)
    opponent_turns = status.remaining_turns_of_hero(opponent_id)

    hero_gold = hero.gold + hero_turns * hero.mine_count
    opponent_gold = opponent.gold + opponent_turns * opponent.mine_count

    gold_diff = hero_gold - opponent_gold

    # Sigmoid function with codomain (0, 1)
    return gold_diff / (1 + abs(gold_diff))


def heuristic(status):
    return utility(status, gold_score)

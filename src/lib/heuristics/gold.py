# -*- coding: UTF-8 -*-

from .abstract_heurisitc import AbstractHeuristic


class GoldHeuristic(AbstractHeuristic):
    def hero_heuristic(self, status, hero_id):
        """ Heuristic that estimates the gold of a hero at the end of the game,
        assuming that the mines will not change owner.

        Arguments:
            status (Status): the game status.
            hero_id (int): the hero's id.

        Returns:
            float: the estimated utility for the hero.
        """
        hero = status.heroes[hero_id]
        remaining_turns = status.remaining_turns_of_hero(hero_id)
        hero_gold = hero.gold + remaining_turns * hero.mine_count
        return hero_gold

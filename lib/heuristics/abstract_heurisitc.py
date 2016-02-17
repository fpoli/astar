# -*- coding: UTF-8 -*-

from lib.utility import hero_utility, utility


class AbstractHeuristic:
    """Abstract heuristic class, superclass of all the actual heuristics.
    """

    def hero_heuristic(self, status, hero_id):
        """ Heuristic that estimates the utility for a single hero.

        Arguments:
            status (Status): the game status.
            hero_id (int): the hero's id.

        Returns:
            float: the estimated utility for the hero.
        """
        raise NotImplementedError

    def heuristic(self, status):
        """ Heuristic that estimates the utility for each hero.

        Arguments:
            status (Status): the game status.

        Returns:
            (float, float, float, float): the estimated utility for each hero.
        """
        return tuple([
            self.hero_heuristic(status, hero_id)
            for hero_id in range(4)
        ])

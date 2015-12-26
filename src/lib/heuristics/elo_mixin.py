# -*- coding: UTF-8 -*-

from lib.utility import hero_utility


class EloHeuristicMixin:
    """Mixin class that implements an heuristic based on elo outcome.

    Requires the implementation of a hero_score() method, to determine for
    each pair of heroes who is winning.
    """

    def hero_score(self, status, hero_id, opponent_id):
        """ Calculate the score of a hero against an opponent only.

        The sum of the scores of the two heroes should be 1:
        hero_score(status, x, y) + hero_score(status, y, x) = 1

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
        raise NotImplementedError

    def hero_heuristic(self, status, hero_id):
        """ Heuristic that estimates the elo utility for a single hero.

        Arguments:
            status (Status): the game status.
            hero_id (int): the hero's id.

        Returns:
            float: the estimated utility for the hero.
        """
        return hero_utility(status, hero_id, self.hero_score)


def score_by_gold_diff(gold_diff, sharpness):
    """ Useful method to get a good score from a gold difference.

    Arguments:
        gold_diff (int): the gold difference.
        sharpness (float): the sharpness of the score function.

    Returns:
        float: the score for a hero that has gold_diff more gold than
            the opponent.
    """
    # Sigmoid function with codomain (0, 1)
    # This is a good heuristic if the game just started
    smoothed_value = (gold_diff / (1 + abs(gold_diff)) + 1) / 2

    # Step function
    # This is a good heuristic if the game is about to finish
    if gold_diff > 0:
        sharp_value = 1
    elif gold_diff < 0:
        sharp_value = 0
    else:
        sharp_value = 0.5

    # Linear combination of the two values, depending on sharpness
    return sharp_value * sharpness + smoothed_value * (1 - sharpness)

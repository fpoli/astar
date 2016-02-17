# -*- coding: UTF-8 -*-

from lib.heuristics.abstract_heurisitc import AbstractHeuristic
from lib.heuristics.elo_mixin import EloHeuristicMixin, score_by_gold_diff


class EloGoldHeuristic(EloHeuristicMixin, AbstractHeuristic):
    def hero_score(self, status, hero_id, opponent_id):
        """ Calculate the score of a hero against an opponent only.

        The score is based on the amount of gold owned by the two heroes at
        the end of the game, assuming that the mines will not change owner:
        score = function_of(difference of gold at the end of the game)

        An interpolation factor, game_progress, is used to change the
        "sharpness" of the function because
        - during the game a smooth function should be used.
        - at the end of the game a step function should be used.

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
        # Calculate the gold at the end of the game
        hero = status.heroes[hero_id]
        hero_turns = status.remaining_turns_of_hero(hero_id)
        hero_gold = hero.gold + hero_turns * hero.mine_count

        opponent = status.heroes[opponent_id]
        opponent_turns = status.remaining_turns_of_hero(opponent_id)
        opponent_gold = opponent.gold + opponent_turns * opponent.mine_count

        gold_diff = hero_gold - opponent_gold

        # the game just started --> game_progress near 0
        # the game is about to finish --> game_progress near 1
        game_progress = status.turn / status.max_turns

        return score_by_gold_diff(gold_diff, game_progress)

# -*- coding: UTF-8 -*-

from random import shuffle
from lib.bots.base import BaseBot
from lib.algorithms.maxn import maxn
from lib.models.action import Action
from lib.simulator import simulate
from lib.heuristics import EloGoldHeuristic


class MaxnBot(BaseBot):
    def __init__(self, hero_id, heuristic=None):
        if heuristic is None:
            heuristic = EloGoldHeuristic()
        super().__init__(hero_id, heuristic)

    def think(self, status):
        """Chooses an action, using maxn.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """

        turn_limit = min(status.turn + 4, status.max_turns)

        def successor(status):
            children = []

            if status.turn >= turn_limit:
                return children

            actions = list(Action)
            shuffle(actions)
            for action in actions:
                next_status = simulate(status, action)
                children.append((next_status, action))
            return children

        happyness, actions = maxn(
            status,
            successor,
            self.heuristic.heuristic,
            self.hero_id,
            4
        )

        action = actions[0]

        return action

# -*- coding: UTF-8 -*-

from random import shuffle
from .base import BaseBot
from lib.algorithms.maxn import maxn
from lib.heuristics.gold import heuristic
from lib.models.action import Action
from lib.simulator import simulate


class MaxnBot(BaseBot):
    def think(self, status):
        """Chooses an action, using maxn.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """

        turn_limit = status.turn + 4

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
            heuristic,
            0,
            4
        )

        action = actions[self.hero_id]

        return action

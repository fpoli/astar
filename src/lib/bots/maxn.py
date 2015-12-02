# -*- coding: UTF-8 -*-

from random import shuffle
from .base import BaseBot
from lib.algorithms.maxn import maxn
from lib.heuristics.gold import heuristic
from lib.models.action import Action
from lib.partial_status import PartialStatus


class MaxnBot(BaseBot):
    def think(self, status):
        """Chooses an action, using maxn.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """

        turn_limit = status.turn + 4

        def successor(partial_status):
            children = []

            if partial_status.status.turn >= turn_limit:
                return children

            actions = list(Action)
            shuffle(actions)
            for action in actions:
                next_status = partial_status.evolve(action)
                children.append((next_status, action))
            return children

        def payoff(partial_status):
            return heuristic(partial_status.status)

        happyness, actions = maxn(
            PartialStatus(status),
            successor,
            payoff,
            0,
            4
        )

        action = actions[self.hero_id]

        return action

# -*- coding: UTF-8 -*-

from random import shuffle
from .base import BaseBot
from lib.algorithms.paranoid import paranoid
from lib.heuristics.gold import hero_heuristic
from lib.models.action import Action
from lib.partial_status import PartialStatus


class ParanoidBot(BaseBot):
    def think(self, status):
        """Chooses an action, using paranoid.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """

        def successor(partial_status):
            actions = list(Action)
            shuffle(actions)
            children = []
            for action in actions:
                next_status = partial_status.evolve(action)
                children.append((next_status, action))
            return children

        def payoff(partial_status):
            return hero_heuristic(partial_status.status, self.hero_id)

        happyness, actions = paranoid(
            PartialStatus(status),
            successor,
            payoff,
            4,
            self.hero_id,
            0,
            4
        )

        action = actions[self.hero_id]

        return action

# -*- coding: UTF-8 -*-

from random import shuffle
from lib.bots.base import BaseBot
from lib.algorithms.paranoid import paranoid
from lib.models.action import Action
from lib.simulator import simulate
from lib.heuristics import EloGoldHeuristic


class ParanoidBot(BaseBot):
    def __init__(self, hero_id, heuristic=None):
        if heuristic is None:
            heuristic = EloGoldHeuristic()
        super().__init__(hero_id, heuristic)

    def think(self, status):
        """Chooses an action, using paranoid.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """

        def successor(status):
            actions = list(Action)
            shuffle(actions)
            children = []
            for action in actions:
                next_status = simulate(status, action)
                children.append((next_status, action))
            return children

        def payoff(status):
            return self.heuristic.hero_heuristic(status, self.hero_id)

        happyness, actions = paranoid(
            status,
            successor,
            payoff,
            5,  # max_depth
            self.hero_id,
            self.hero_id,
            4
        )

        action = actions[0]

        return action

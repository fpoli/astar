# -*- coding: UTF-8 -*-

import random
from .base import BaseBot


class RandomBot(BaseBot):
    def think(self, actions):
        """Chooses a random action.

        Arguments:
            actions ([Action]): the actions among which the bot can choose.

        Returns:
            Action: the randomly chosen action.
        """
        return random.choice(actions)

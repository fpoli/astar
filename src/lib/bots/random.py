# -*- coding: UTF-8 -*-

import random
from .base import BaseBot


class RandomBot(BaseBot):
    def think(self, status):
        """Chooses a random action.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the randomly chosen action.
        """
        actions = self.possible_actions(status)
        return random.choice(actions)

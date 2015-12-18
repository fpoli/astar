# -*- coding: UTF-8 -*-

from .goal import Goal
from lib.models.tile import Tile
from lib.models.action import action_to_dir


class TavernGoal(Goal):
    def is_reached(status, action):
        """Test if the hero goes to the tavern.

        Arguments:
            status (Status): the initial game status.
            action (Action): the action.

        Returns:
            bool: true iff this goal has been reached from the initial status
              using the given action.
        """
        hero = status.heroes[self.hero_id]

        direction = action_to_dir(action)
        dst_pos = hero.pos + direction
        dst_tile = status.map[dst_pos]

        return dst_tile == Tile.tavern

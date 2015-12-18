# -*- coding: UTF-8 -*-

from .goal import Goal
from lib.models.tile import Tile


class MineGoal(Goal):
    def is_reached(status, action):
        """Test if the hero conquers a new mine.

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

        if dst_tile == Tile.mine:
            mine_owner = status.mine_owner[dst_pos]

            if mine_owner != hero.id and hero.life > 20:
                # The hero steps over an opponent mine with enough life
                return True

        return False

# -*- coding: UTF-8 -*-


class Goal:
    def __init__(self, hero_id=None):
        """ Constructor.

        Arguments:
            hero_id (int): the hero that owns this goal.
        """
        self.hero_id = hero_id

    def is_reached(status, action):
        """Test if the goal is reached from a given status with a given action.

        Arguments:
            status (Status): the initial game status.
            action (Action): the action.

        Returns:
            bool: true iff this goal has been reached from the initial status
              using the given action.
        """
        raise NotImplementedError

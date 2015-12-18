# -*- coding: UTF-8 -*-

from .base import BaseBot


class AbstractGoalBot(BaseBot):
    def think(self, status):
        """Chooses an action for the given status.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """
        goal = self.choose_goal(status)
        action = self.action_for_goal(status, goal)
        return action

    def choose_goal(self, status):
        """Chooses a goal for the given status.

        Arguments:
            status (Status): the game status.

        Returns:
            Goal: the chosen goal.
        """
        raise NotImplementedError

    def action_for_goal(self, status, goal):
        """Chooses an action to reach a goal.

        Arguments:
            status (Status): the game status.
            goal (Goal): the goal.

        Returns:
            Action: an action to reach the goal.
        """
        raise NotImplementedError

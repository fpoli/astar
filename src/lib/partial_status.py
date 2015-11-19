# -*- coding: UTF-8 -*-

from lib.models.status import Status
from lib.simulator import simulate


class PartialStatus(object):
    """Represents a partial game status.

    A partial game status holds information about the status and the actions
    "declared" by the first k players (0 <= k < 4).
    When every player has declared her action, the partial status evolves
    to a new status.
    This class follows the Decorator Design Pattern (acting as a decorator
    for the Status class).

    Attributes:
        status (Status): current game status
        actions ([Action]): actions declared by players
    """

    def __init__(self, status, action_list=None):
        """Constructor.

        Args:
            status (Status): current status
            action_list ([Action]): declared actions
        """
        self.status  = status
        self.actions = action_list if action_list is not None else []

    def evolve(self, action):
        """Declares a move for a player.

        Args:
            action (Action): declared action

        Returns:
            PartialStatus: Partial status where player declared an action
        """
        new_actions = self.actions + [action]
        if len(new_actions) == len(self.status.heroes):
            return PartialStatus(simulate(self.status, new_actions))
        else:
            return PartialStatus(self.status, new_actions)

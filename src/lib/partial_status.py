# -*- coding: UTF-8 -*-

from lib.models.status import Status


class PartialStatus(object):
    """Represents a partial game status.

    A partial game status holds information about the status and the actions
    "declared" by some players.
    When every player has declared her action, the partial status evolves
    to a new status.

    Attributes:
        status (Status): current game status
        actions ([dict]): actions declared by players
    """

    def __init__(status, action_dict):
        """Constructor.

        Args:
            status (Status): current status
            action_dict (dict): declared actions
        """
        self.status  = status
        self.actions = actions_dict

    def evolve(player_id, action):
        """Declares a move for a player.
        If player has already declared a move, that move is overwritten.

        Args:
            player_id (int): identifier of the player
            action (Action): declared action

        Returns:
            PartialStatus: Partial status where player declared an action
        """
        self.actions[player_id] = action
        if len(self.action) == len(self.status.heroes):
            return PartialStatus(simulator(self.status, self.actions), {})
        else:
            return PartialStatus(self.status, self.actions)

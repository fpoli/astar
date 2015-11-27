# -*- coding: UTF-8 -*-

from lib.models.action import Action


class BaseBot(object):
    """Abstract bot class, superclass of all the actual bots.
    """

    def __init__(self, hero_id):
        """Constructor of the abstract bot.

        Arguments:
            hero_id (int): the bot's hero id.
        """
        self.hero_id = hero_id

    def possible_actions(self, status):
        """Returns the list of possible actions in game status.

        Arguments:
            status (Status): the game status.

        Returns:
            [Action]: the list of possible actions.
        """
        return list(Action)

    def think(self, status):
        """Chooses the action to perform.

        Arguments:
            status (Status): the game status.

        Returns:
            Action: the chosen action.
        """
        raise NotImplementedError
